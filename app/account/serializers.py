import typing as tp

from account.schemas import AccountData


def account_serializer(model_objects: tp.Any,
                       many: bool = False) -> tp.Union[tp.List[tp.Dict[str, tp.Union[str, bool]]],
                                                       tp.Dict[str, tp.Union[str, bool]]]:
    """
    Serializer for account
    Args:
      model_objects: current Model
      many: if many models
    Returns:
      dict with user data
    """

    schema = AccountData

    if not many:
        if model_objects is not None:
            return schema(**model_objects.__dict__).__dict__
        return {}
    else:
        model_objects_data = []
        for model_object in model_objects:
            model_objects_data.append(schema(**model_object.__dict__).__dict__)
        return model_objects_data
