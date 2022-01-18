import typing as tp

from flask import Response, jsonify

from utils.data_process import type_model_data, return_data_serializer


def list_endpoint_mixin(schema: tp.Any,
                        model: tp.Any,
                        request: tp.Any,
                        data: tp.Any = None,
                        search_fields: tp.Optional[tp.List[str]] = None,
                        search_value: tp.Optional[str] = None) -> tp.Tuple[Response, int]:
    """
    Function mixin for read; create
    Args:
        schema: current schema for url
        model: current model
        request: current request
        data: current data for creating new object
        search_fields: fields that will be searched for
        search_value: search value
    Return:
        Response with status code
    """

    if request.method == 'GET':
        model_data, status_code = get_model_objects(model=model,
                                                    schema=schema,
                                                    search_fields=search_fields,
                                                    search_value=search_value)
    else:
        model_data, status_code = create_model_object(model=model, data=data, schema=schema)
    return jsonify(model_data), status_code


def get_model_objects(model: tp.Any,
                      schema: tp.Any,
                      search_fields: tp.Optional[tp.List[str]] = None,
                      search_value: tp.Optional[str] = None) -> type_model_data:
    """
    Get all model objects
    Args:
        schema: current schema
        model: current model
        search_fields: fields that will be searched for
        search_value: search value
    Returns:
        dict or list with dicts with user data
    """

    model_objects = []

    if search_fields is not None and search_value is not None:
        for column in model.__table__.columns:
            if column.name in search_fields:
                model_objects = model.query.filter(column.contains(search_value)).all()
            if any(model_objects):
                break
    else:
        model_objects = model.query.all()

    serializer_data = return_data_serializer(schema=schema, model_objects=model_objects, many=True)
    if not any(serializer_data):
        return serializer_data, 404
    return serializer_data, 200


def create_model_object(model: tp.Any, data: tp.Dict[str, tp.Union[str, bool]], schema: tp.Any) -> type_model_data:
    """
    Create model object
    Args:
        model: current model
        data: create data
        schema: current serializer
    Returns:
        dict or list with dicts with user data
    """

    from main import db

    new_object = model(**data)
    db.session.add(new_object)
    db.session.commit()
    serializer_data = return_data_serializer(schema=schema, model_objects=new_object)
    if not any(serializer_data):
        return serializer_data, 404
    return serializer_data, 201


def detail_endpoint_mixin(schema: tp.Any,
                          model: tp.Any,
                          request: tp.Any,
                          pk: int,
                          data: tp.Dict[str, tp.Union[str, int, bool]],
                          permissions: tp.Optional[tp.List[tp.Any]] = None) -> tp.Tuple[Response, int]:
    """
    Function mixin for read; update; delete
    Args:
        schema: current schema for url
        model: current model
        request: current request
        pk: current object pk
        data: current serializer for model
        permissions: list with permissions for this view if needed
    Return:
        Response with status code
    """

    model_data, status_code = get_model_object_from_pk(model=model, pk=pk, schema=schema)
    if status_code == 404:
        return jsonify(model_data), status_code

    if permissions is not None:
        for permission in permissions:
            if not permission(request=request, pk=pk):
                return jsonify({'Error': 'You has not permissions to perform this action'}), 401

    if request.method == 'PATCH':
        update_model_object(model=model, pk=pk, data=data)
    elif request.method == 'DELETE':
        remove_model_object(model=model, pk=pk)
        return jsonify({}), 204
    elif request.method == 'GET':
        return jsonify(model_data), status_code

    # means that model was update
    model_data, status_code = get_model_object_from_pk(model=model, pk=pk, schema=schema)
    return jsonify(model_data), status_code


def get_model_object_from_pk(model: tp.Any, pk: tp.Any, schema: tp.Any) -> type_model_data:
    """
    Get model object from pk
    Args:
        model: current model
        pk: current model pk
        schema: current serializer
    Returns:
        dict or list with dicts with user data
    """

    account = model.query.get(pk)
    serializer_data = return_data_serializer(schema=schema, model_objects=account)
    if not any(serializer_data):
        return serializer_data, 404
    return serializer_data, 200


def update_model_object(model: tp.Any, pk: tp.Any, data: tp.Any) -> None:
    """
    Update model object
    Args:
        model: current model
        pk: current model pk
        data: update data
    """

    from main import db

    model.query.filter_by(id=pk).update(data)
    db.session.commit()


def remove_model_object(model: tp.Any, pk: tp.Any) -> None:
    """
    Remove model object
    Args:
        model: current model
        pk: current model pk
    """

    from main import db

    account = model.query.get(pk)
    db.session.delete(account)
    db.session.commit()
