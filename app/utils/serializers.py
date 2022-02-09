import typing as tp
import sqlalchemy
import decimal
import datetime

from flask_sqlalchemy import DefaultMeta

from pydantic import BaseModel, constr, root_validator
from pydantic.fields import ModelField

SQLALCHEMY_TYPE_TRANSLATE = {
    sqlalchemy.sql.sqltypes.BigInteger: int,
    sqlalchemy.sql.sqltypes.Unicode: str,
    sqlalchemy.sql.sqltypes.Integer: int,
    sqlalchemy.sql.sqltypes.String: str,
    sqlalchemy.sql.sqltypes.Float: float,
    sqlalchemy.sql.sqltypes.Numeric: decimal.Decimal,
    sqlalchemy.sql.sqltypes.DateTime: tp.Optional[datetime.datetime],
    sqlalchemy.sql.sqltypes.LargeBinary: bytes,
    sqlalchemy.sql.sqltypes.Boolean: bool,
    sqlalchemy.sql.sqltypes.BOOLEAN: bool,
    sqlalchemy.sql.sqltypes.Date: tp.Optional[datetime.date],
    sqlalchemy.sql.sqltypes.Time: tp.Optional[datetime.time],
    sqlalchemy.sql.sqltypes.Interval: tp.Optional[datetime.timedelta],
    sqlalchemy.sql.sqltypes.ARRAY: list,
    sqlalchemy.sql.sqltypes.JSON: dict
}

serializer_data_type = tp.Dict[str, tp.Union[str, int, bool]]


class BaseSerializer(BaseModel):
    """
    Base serializer
    """

    remove_fields: tp.List[str] = ['read_only_fields', 'multiple_data', 'many',
                                   'write_only_fields', 'method', 'remove_fields', '_sa_instance_state',
                                   'data', 'is_annotate', 'exclude_fields']
    read_only_fields = []  # type: ignore
    exclude_fields = []  # type: ignore
    write_only_fields = []  # type: ignore

    def update_remove_fields(self, fields: tp.List[str]) -> None:
        """
        Update remove fields
        Args:
            fields: fields which will be append to remove fields
        """

        for field in fields:
            self.remove_fields.append(field)

    def validate_data_before_create(self) -> serializer_data_type:
        """
        Validate data before create
        Return:
            dict with data
        """

        data = self.__dict__.copy()
        for key in self.__dict__:
            is_key_in = bool(
                key in self.read_only_fields or key in self.remove_fields or key in self.exclude_fields
            )
            if data[key] == '' or data[key] is None or is_key_in:
                del data[key]
        return data

    def validate_data_before_get(self) -> serializer_data_type:
        data = self.__dict__.copy()
        for key in self.__dict__:
            if key in self.remove_fields or key in self.write_only_fields:
                del data[key]
        return data


class BaseModelSerializer(BaseSerializer):
    """
    Base Model serializer
    """

    def __init__(self, *args: tp.Any, **kwargs: tp.Any) -> None:
        for column in self.model.__table__.columns:  # type: ignore
            column_type = type(column.__dict__['type'])
            if column_type in SQLALCHEMY_TYPE_TRANSLATE:
                column_translate_type = SQLALCHEMY_TYPE_TRANSLATE[column_type]
                if column_translate_type == str:
                    column_translate_type = constr(max_length=column.__dict__['type'].length)
            else:
                column_translate_type = None

            self.__fields__.update(
                {column.name: ModelField.infer(name=column.name,
                                               value='',
                                               annotation=column_translate_type,
                                               class_validators=None,
                                               config=self.__config__)
                 })

        self.__fields__.update(
            {'many': ModelField.infer(name='many',
                                      value=True if kwargs.get('many') else False,
                                      annotation=bool,
                                      class_validators=None,
                                      config=self.__config__)
             })
        self.__fields__.update(
            {'method': ModelField.infer(name='method',
                                        value=kwargs.get('method') if kwargs.get('method') else 'GET',
                                        annotation=str,
                                        class_validators=None,
                                        config=self.__config__)
             })
        self.__fields__.update(
            {'is_annotate': ModelField.infer(name='is_annotate',
                                             value=True if kwargs.get('is_annotate') else False,
                                             annotation=bool,
                                             class_validators=None,
                                             config=self.__config__)
             })

        if kwargs.get('many'):
            self.__fields__.update(
                {'multiple_data': ModelField.infer(name='multiple_data',
                                                   value=args,
                                                   annotation=tp.List[tp.Any],
                                                   class_validators=None,
                                                   config=self.__config__)
                 })
        if kwargs.get('is_annotate'):
            self.__fields__.update(
                {'data': ModelField.infer(name='data',
                                          value=args,
                                          annotation=serializer_data_type,
                                          class_validators=None,
                                          config=self.__config__)
                 })
        else:
            self.__fields__.update(
                {'data': ModelField.infer(name='data',
                                          value=kwargs,
                                          annotation=serializer_data_type,
                                          class_validators=None,
                                          config=self.__config__)
                 })
        super().__init__(**kwargs)

    @root_validator
    def validate(cls, values: serializer_data_type) -> serializer_data_type:  # type: ignore
        if values.get('method') in ['POST', 'PATCH', 'PUT']:
            for value in values:
                if values.get('method') == 'PATCH' and (values[value] is None or values[value] == ''):
                    continue
                try:
                    values[value] = getattr(cls, f'validate_{value}')(cls, values[value])
                except AttributeError:
                    continue
        return values

    def get_model_objects_data(self) -> tp.Any:
        """
        Get model objects data
        Return:
            dict with data or list with dicts
        """

        if not self.many:  # type: ignore
            object_data = self.validate_data_before_get()
            return object_data
        else:
            model_objects_data = []
            cls = self.__class__

            for data in self.multiple_data:  # type: ignore
                serializer_object = cls(**data.__dict__)
                object_data = serializer_object.validate_data_before_get()
                model_objects_data.append(object_data)

            return model_objects_data

    def get_annotate_model_objects_data(self,
                                        annotate_fields: tp.List[str]) -> tp.Any:
        """
        Get model data if used annotated query
        Args:
            annotate_fields: list with annotate fields
        Return:
            dict with data or list with dicts
        """

        cls = self.__class__

        if not self.many:  # type: ignore
            serializer_object = cls(**self.data[0].__dict__)  # type: ignore
            object_data = serializer_object.validate_data_before_get()

            for index, annotate_field in enumerate(annotate_fields):
                object_data.update({annotate_field: self.data[index + 1]})  # type: ignore
            return object_data
        else:
            model_objects_data = []

            for data in self.multiple_data:  # type: ignore
                serializer_object = cls(**data[0].__dict__)
                object_data = serializer_object.validate_data_before_get()

                for index, annotate_field in enumerate(annotate_fields):
                    object_data.update({annotate_field: data[index + 1]})
                model_objects_data.append(object_data)

            return model_objects_data
