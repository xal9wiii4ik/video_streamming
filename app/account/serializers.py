import typing as tp

from account.schemas import AccountData
from utils import type_model_data


def account_serializer(model_objects: tp.Any,
                       many: bool = False) -> type_model_data:
    """
    Serializer for account
    Args:
      model_objects: current Model
      many: if many models
    Returns:
      dict or list with dicts with user data
    """

    schema = AccountData

    if not many:
        if model_objects is not None:
            object_data = schema(**model_objects.__dict__).__dict__
            object_data.update({'id': model_objects.id})
            return object_data, 200
        return {}, 404
    else:
        model_objects_data = []
        for model_object in model_objects:
            object_data = schema(**model_object.__dict__).__dict__
            object_data.update({'id': model_object.id})
            model_objects_data.append(object_data)
        return model_objects_data, 200
