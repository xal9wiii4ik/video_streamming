from pydantic import BaseModel, constr


class RegisterUser(BaseModel):
    """ Schema for post base """

    username: constr(max_length=100)  # type: ignore
    password: constr(max_length=500)  # type: ignore
    repeat_password: constr(max_length=500)  # type: ignore
    email: constr(max_length=100)  # type: ignore
    first_name: constr(max_length=100)  # type: ignore
    last_name: constr(max_length=100)  # type: ignore
