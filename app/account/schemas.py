from pydantic import BaseModel, constr


class RegisterUser(BaseModel):
    """ Schema for post base """

    username: constr(max_length=100)  # type: ignore
    password: constr(max_length=500)  # type: ignore
    repeat_password: constr(max_length=500)  # type: ignore
    email: constr(max_length=100)  # type: ignore
    first_name: constr(max_length=100)  # type: ignore
    last_name: constr(max_length=100)  # type: ignore


class AccountData(BaseModel):
    """ Schema for account """

    username: str = ''
    email: str = ''
    first_name: str = ''
    last_name: str = ''


class AccessToken(BaseModel):
    """ Schema for getting access token """

    username: str
    password: str


class RefreshToken(BaseModel):
    """ Schema for getting refresh token """

    refresh_token: str
