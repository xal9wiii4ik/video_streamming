import typing as tp
import boto3
import fleep

from utils.exceptions import SerializerValidationError

from settings import VIDEOS_BUCKET, BUCKET_REGION


def process_data_to_create_video(request: tp.Any) -> str:
    """
    Process data to create and upload video to bucket
    Args:
        data: current data
        request: current request
    """

    file_bytes = request.files.get('file').read()
    file_info = fleep.get(file_bytes)

    if not any(file_info.mime) or file_info.mime[0].split('/')[0] != 'video':
        raise SerializerValidationError({'file': 'File must be of the video type'})

    bucket_path = upload_video_to_bucket(username=request.user.username,
                                         file_bytes=file_bytes,
                                         file_content_type=file_info.mime)
    return bucket_path


def upload_video_to_bucket(username: str, file_bytes: bytes, file_content_type: tp.List[str]) -> str:
    """
    Generate bucket path and upload new video
    Args:
        username: username
        file_bytes: file bytes
        file_content_type: list with file extension
    Returns:
        bucket path for new video according with user
    """

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(VIDEOS_BUCKET)
    count_files = len(list(bucket.objects.filter(Prefix=username)))
    file_path = f'{username}/{count_files}.{file_content_type[0].split("/")[-1]}'
    file = bucket.put_object(Key=file_path,
                             Body=file_bytes,
                             ContentType=file_content_type[0])

    bucket_path = f'https://s3-{BUCKET_REGION}.amazonaws.com/{VIDEOS_BUCKET}/{file.key}'
    return bucket_path
