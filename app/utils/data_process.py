import hashlib
import typing as tp

from settings import SECRET_KEY


type_model_data = tp.Tuple[tp.Union[tp.List[tp.Dict[str, tp.Union[str, bool]]], tp.Dict[str, tp.Union[str, bool]]], int]


def make_password(password: str) -> str:
    """
    Hashing password
    Args:
         password: password
    Returns:
        hex of hashing password
    """

    hash_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SECRET_KEY.encode('utf-8'), 100000)
    return hash_password.hex()


def return_data_serializer(schema: tp.Any,
                           model_objects: tp.Any,
                           many: bool = False) -> tp.Union[tp.List[tp.Dict[str, tp.Union[str, bool]]],
                                                           tp.Dict[str, tp.Union[str, bool]]]:
    """
    Serializer for account
    Args:
      schema: current schema
      model_objects: current Model
      many: if many models
    Returns:
      dict or list with dicts with user data
    """

    if not many:
        if model_objects is not None:
            object_id = model_objects.id
            object_data: tp.Dict[str, tp.Union[str, bool]] = schema(**model_objects.__dict__).__dict__
            object_data.update({'id': object_id})
            return object_data
        return {}
    else:
        model_objects_data = []
        for model_object in model_objects:
            object_data = schema(**model_object.__dict__).__dict__
            object_data.update({'id': model_object.id})
            model_objects_data.append(object_data)
        return model_objects_data


def validate_data_for_create_or_update(
        schema: tp.Any,
        request: tp.Any,
        read_only_fields: tp.Optional[tp.List[str]] = None) -> tp.Dict[str, tp.Union[str, int, bool]]:
    """
    Validate data for create or update model
    Args:
        schema: current schema
        request: current request
        data: validated data from body
        read_only_fields: fields which are will not be updated in model
    Returns:
        Clear data
    """

    if request.method in ['PATCH', 'POST']:
        data: tp.Dict[str, tp.Union[str, int]] = schema(**request.json).__dict__
        for key in data.copy().keys():
            if data[key] == '' or (read_only_fields is not None and key in read_only_fields):
                del data[key]
        return data
    return {}
