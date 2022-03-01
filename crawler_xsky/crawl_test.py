import pytest
import requests

from main import send_requests


def get_cookie(x):
    resp = requests.get(x)
    print(resp.cookies)
    for k, v in resp.cookies.items():
        print(k + "=" + v)
    return x + 1


def test_answer():
    curPage = 0
    list_post = []
    result = send_requests(curPage, list_post)
    assert len(result) > 0


if __name__ == '__main__':
    pytest.main()
