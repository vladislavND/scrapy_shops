import os

from requests import request


def create_path(file_name: str, path: str, shop_id: int):
    data = {
        'file_name': file_name,
        'path': path,
        'shop_id': shop_id,
    }
    return request(
        method='POST', url=f"{os.getenv('BACKEND_URL')}/api/add_file_shop", json=data
    )