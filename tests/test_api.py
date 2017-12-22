import requests

from src import env_config


def test_api():
    url = env_config.HTTP_HOST + '/api/v1/resource/detail?res_id=8727736998690816&res_type=7'
    req = requests.get(
        url=url
    )

    assert req.json()['status'] == 200

    url = env_config.HTTP_HOST + '/api/v1/user/create/anonymous'

    req = requests.post(url)

    assert req.json()['status'] == 200

    url = env_config.HTTP_HOST + '/api/v1/user/signin'

    req = requests.post(
        url=url,
        data={"mobile": "11011233501", "code": "0000"},
        headers={"Content-Type": "application/json"}
    )
    assert req.json()['status'] == 200
