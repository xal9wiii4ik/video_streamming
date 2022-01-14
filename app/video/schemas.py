import typing as tp

from pydantic import BaseModel, constr


class VideoDataCreate(BaseModel):
    """ Schema for create video """

    title: constr(max_length=50)  # type: ignore
    description: constr(max_length=50)  # type: ignore


class VideoDataUpdateView(BaseModel):
    """ Schema for view or update video """

    title: tp.Optional[str] = None
    description: tp.Optional[str] = None
    account_id: tp.Optional[int] = None
    bucket_path: tp.Optional[str] = None
