import random
import secrets
import time
import typing

import pytest
from fastapi import APIRouter, Request
from fastapi.testclient import TestClient

from pct.main import app

client = TestClient(app)


def create_upload_router():
    upload_router = APIRouter()

    @upload_router.post('/')
    async def upload_test_data(req: Request):
        from pct.keys import keys
        keys.all_keys.append(await req.json())
    @upload_router.delete('/')
    async def delete_test_data(req: Request):
        from pct.keys import keys
        keys.all_keys.clear()
    return upload_router


def create_key(id_length = 16, origins = ['DE', 'GB', 'NL'], timestamp = time.time()):
    return {
        'id': secrets.token_hex(id_length),
        'origin': random.choice(origins),
        'timestamp': timestamp
    }


def create_test_keys(n: int) -> typing.List[typing.Dict]:
    keys = []
    for i in range(n):
        keys.append(create_key())
    return keys


@pytest.fixture(scope='function')
def testdata():
    TEST_UPLOAD_PREFIX = '/test-upload'
    app.include_router(create_upload_router(), prefix=(TEST_UPLOAD_PREFIX))
    keys = create_test_keys(25)
    for key in keys:
        client.post(f'{TEST_UPLOAD_PREFIX}/', json=key)
    yield keys
    client.delete(f'{TEST_UPLOAD_PREFIX}/')


@pytest.mark.helloenterpy
def test_hello_enterpy():
    r = client.get('/welcome')
    assert r.json() == "Hello enterPY!"


@pytest.mark.downloadkeys
def test_download_keys(testdata):
    r = client.get('/keys')
    assert r.status_code == 200
    keys = r.json()
    assert keys == testdata


@pytest.mark.queryparams
def test_download_keys_limit(testdata):
    r = client.get('/keys?limit=12')
    assert r.status_code == 200
    keys = r.json()
    assert len(keys) == 12
    for key in keys:
        assert key in testdata


@pytest.mark.pathparams
def test_download_keys_country(testdata):
    COUNTRY = 'DE'
    r = client.get(f'/keys/{COUNTRY}')
    assert r.status_code == 200
    keys = r.json()
    for key in keys:
        assert key in testdata
        assert key['origin'] == COUNTRY
