import typing as tp

from flask.views import MethodView
from flask import jsonify, Response
from flask_sqlalchemy import DefaultMeta

from sqlalchemy import asc, desc, or_
from sqlalchemy.sql.elements import BinaryExpression

from models import db

from utils.exceptions import LimitOffsetError, SortException
from utils.serializers import serializer_data_type


class BaseMixinsMethodView(MethodView):
    """
    Base class for mixins
    """

    # main required fields
    request: tp.Any
    model: tp.Any
    serializer: tp.Any

    # additional queries Optional
    filter_query: tp.List[BinaryExpression] = []
    annotate_data: tp.Optional[tp.List[tp.Dict[str, tp.Union[DefaultMeta, tp.List[str]]]]] = None

    # query field which not required(added in the process)
    query: tp.Any

    # permission classes not required
    permission_classes: tp.List[tp.Any] = []

    # optional fields which getting from url, but can be overridden in code
    limit: tp.Optional[int] = None
    offset: tp.Optional[int] = None
    sort: tp.Optional[str] = None
    sort_type: tp.Optional[str] = None
    search_value: tp.Optional[str] = None
    search_fields: tp.Optional[tp.List[str]] = None

    _model_object: tp.Any = None
    _annotate_fields: tp.Optional[tp.List[str]] = None

    def __init__(self, *args: tp.Any, **kwargs: tp.Any) -> None:
        super().__init__(*args, **kwargs)
        # getting search query
        self.search_query = self.filter_query.copy()
        self.update_search_query()
        # parse args for url
        self.parse_url_args()
        # set default query
        self.query = db.session.query(self.model).filter(*self.search_query)

    def update_search_query(self) -> None:
        """
        Ability to update search query in view
        """

        pass

    def parse_url_args(self) -> None:
        """
        Parse arguments which in the url
        """

        self.limit = self.request.args.get('limit')
        self.offset = self.request.args.get('offset')
        self.sort = self.request.args.get('sort')
        self.sort_type = self.request.args.get('sort_type')
        self.search_value = self.request.args.get('search')

        search_query = []

        if self.search_fields is not None and self.search_value is not None:
            for column in self.model.__table__.columns:
                if column.name in self.search_fields:
                    search_query.append(column.contains(self.search_value))
            self.search_query.append(or_(*search_query))

        if self.limit is not None and not self.limit.isnumeric():  # type: ignore
            raise LimitOffsetError('Limit must be numeric')
        if self.offset is not None and not self.offset.isnumeric():  # type: ignore
            raise LimitOffsetError('Offset must be numeric')

        if self.sort is not None:
            self.update_sort_value()
        else:
            self.sort = desc(self.model.id)

    def update_sort_value(self) -> None:
        """
        Set column according with sort field
        """

        column_names = [column.name for column in self.model.__table__.columns]

        if self.sort not in column_names:
            raise SortException(f'Sort should be one of {column_names} values')

        for column in self.model.__table__.columns:
            if self.sort == column.name:
                self.sort = column

        self.sort = asc(self.sort) if self.sort_type == 'asc' else desc(self.sort)

    def annotate_query(self) -> tp.List[str]:
        """
        Get annotate query
        Returns:
            list with annotate_fields
        """

        annotate_fields = []
        for data in self.annotate_data:  # type: ignore
            for column in data['model'].__table__.columns:  # type: ignore
                if column.name in data['annotate_fields']:
                    # annotate query
                    self.query = self.query.add_columns(column.label(column.name))
                    annotate_fields.append(column.name)
            # join tebles in query
            self.query = self.query.join(data['model'])
        return annotate_fields

    def paginate_query_set(self) -> None:
        """
        Make paginate queryset
        """

        if self.limit is None or self.offset is None:
            self.query = self.query.order_by(self.sort)
        else:
            self.query = self.query.limit(self.limit).offset(self.offset)

    def perform_create_update(self, serializer_data: serializer_data_type) -> serializer_data_type:
        """
        Perform create or update func(possibility to override creation data)
        Args:
            serializer_data: current data before creating
        Returns:
            current data before creating
        """

        return serializer_data

    def perform_validate(self, data: serializer_data_type) -> serializer_data_type:
        """
        Perform validate data for creating or updating
        """

        return data


class ListCreateViewMixin(BaseMixinsMethodView):
    """
    Mixin for list or create
    """

    # optional field for serializer
    read_only_fields: tp.Optional[tp.List[str]] = None

    # optional field for searching query
    search_fields: tp.Optional[tp.List[str]] = None

    def get(self) -> tp.Tuple[Response, int]:
        # annotate query and get annotate fields
        annotate_fields = self.annotate_query() if self.annotate_data is not None else None

        # paginate
        self.paginate_query_set()

        # get objects
        model_objects = self.query.all()
        serializer = self.serializer(many=True, *model_objects)

        # update data if query is annotate
        if annotate_fields is not None:
            data = serializer.get_annotate_model_objects_data(annotate_fields=annotate_fields)
        else:
            data = serializer.get_model_objects_data()

        return jsonify(data), 200

    def post(self) -> tp.Tuple[Response, int]:
        # validate data for creating new object
        data = self.request.json if self.request.json is not None else self.request.form.copy()
        data = self.perform_validate(data=data)

        # get data for creating new object
        serializer = self.serializer(method='POST', **data)
        serializer_data = serializer.validate_data_before_create()

        # update data if this needed
        serializer_data = self.perform_create_update(serializer_data=serializer_data)

        # create model object
        model_data = self.create_model_object(data=serializer_data)
        return jsonify(model_data), 201

    def create_model_object(self, data: serializer_data_type) -> tp.Any:
        """
        Create model object
            data: create data
        Returns:
            dict or list with dicts with user data
        """

        new_object = self.model(**data)

        serializer = self.serializer(**new_object.__dict__)

        db.session.add(new_object)
        db.session.commit()
        db.session.refresh(new_object)

        model_data = serializer.validate_data_before_get(model_data=new_object.__dict__)
        return model_data
