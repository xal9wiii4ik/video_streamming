import typing as tp

from flask import Response, jsonify

from account.serializers import account_serializer
from utils import type_model_data


def func_rud_mixin(schema: tp.Any, model: tp.Any,
                   request: tp.Any, pk: tp.Any, serializer: tp.Any) -> tp.Tuple[Response, int]:
    """
    Function mixin for read; update; delete
    Args:
        schema: current schema for url
        model: current model
        request: current request
        pk: current object pk
        serializer: current serializer for model
    Return:
        Response with status code
    """

    model_data, status_code = get_model_object_from_pk(model=model, pk=pk, serializer=serializer)
    if status_code == 404:
        return jsonify(model_data), status_code

    if request.method == 'PATCH':
        data = schema(**request.json).__dict__
        for key in data.copy().keys():
            if data[key] == '':
                del data[key]
        update_model_object(model=model, pk=pk, data=data)
        # TODO check
    elif request.method == 'DELETE':
        remove_model_object(model=model, pk=pk)
        return jsonify({}), 204
    elif request.method == 'GET':
        return jsonify(model_data), status_code

    # means that model was update
    model_data, status_code = get_model_object_from_pk(model=model, pk=pk, serializer=serializer)
    return jsonify(model_data), status_code


def func_cr_mixin(schema: tp.Any, model: tp.Any, request: tp.Any, serializer: tp.Any) -> tp.Tuple[Response, int]:
    """
    Function mixin for read; create
    Args:
        schema: current schema for url
        model: current model
        request: current request
        serializer: current serializer for model
    Return:
        Response with status code
    """

    if request.method == 'GET':
        model_data, status_code = get_model_objects(model=model, serializer=serializer)
    else:
        data = schema(**request.json).__dict__
        for key in data.copy().keys():
            if data[key] == '':
                del data[key]
        model_data, status_code = create_model_object(model=model, data=data, serializer=serializer)
    return jsonify(model_data), status_code


def create_model_object(model: tp.Any, data: tp.Any, serializer: tp.Any) -> type_model_data:
    """
    Create model object
    Args:
        model: current model
        data: create data
        serializer: current serializer
    Returns:
        dict or list with dicts with user data
    """

    from main import db

    new_object = model(**data)
    db.session.add(new_object)
    db.session.commit()
    return serializer(model_objects=new_object)  # type: ignore


def get_model_objects(model: tp.Any, serializer: tp.Any) -> type_model_data:
    """
    Get all model objects
    Args:
        model: current model
        serializer: current serializer
    Returns:
        dict or list with dicts with user data
    """

    account = model.query.all()
    return serializer(model_objects=account, many=True)  # type: ignore


def get_model_object_from_pk(model: tp.Any, pk: tp.Any, serializer: tp.Any) -> type_model_data:
    """
    Get model object from pk
    Args:
        model: current model
        pk: current model pk
        serializer: current serializer
    Returns:
        dict or list with dicts with user data
    """

    account = model.query.get(pk)
    return serializer(model_objects=account)  # type: ignore


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
