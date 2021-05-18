import random
import secrets
import time
import typing

import pytest
from fastapi import APIRouter, Request
from fastapi.testclient import TestClient

from pct.main import app

KEYS_PREFIX = '/keys'

client = TestClient(app)


def create_upload_router():
    upload_router = APIRouter()

    @upload_router.post('/')
    async def upload_test_data(req: Request):
        from pct.keys import keys
        keys.all_keys.append(await req.json())
    @upload_router.delete('/')
    async def delete_test_data():
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
        client.post(TEST_UPLOAD_PREFIX, json=key, allow_redirects=True)
    yield keys
    client.delete(TEST_UPLOAD_PREFIX, allow_redirects=True)


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
    r = client.get(f'{KEYS_PREFIX}?limit=12')
    assert r.status_code == 200
    keys = r.json()
    assert len(keys) == 12
    for key in keys:
        assert key in testdata

@pytest.mark.queryparams
def test_download_keys_invalid_limit():
    r = client.get(f'{KEYS_PREFIX}?limit=foo')
    assert r.status_code == 422


@pytest.mark.pathparams
def test_download_keys_country(testdata):
    COUNTRY = 'DE'
    r = client.get(f'{KEYS_PREFIX}/{COUNTRY}')
    assert r.status_code == 200
    keys = r.json()
    for key in keys:
        assert key in testdata
        assert key['origin'] == COUNTRY


@pytest.mark.pathparams
def test_download_keys_invalid_country():
    COUNTRY = 'FOO'
    r = client.get(f'{KEYS_PREFIX}/{COUNTRY}')
    assert r.status_code == 422


@pytest.mark.bodyparams
def test_upload_key():
    key1 = create_key(id_length=16)
    key2 = create_key(id_length=16)
    r = client.post(KEYS_PREFIX, json=key1, allow_redirects=True)
    assert r.status_code == 201
    r = client.post(KEYS_PREFIX, json=key2, allow_redirects=True)
    assert r.status_code == 201
    r = client.get(KEYS_PREFIX)
    assert r.status_code == 200
    keys = r.json()
    for key in keys:
        key in [key1, key2]


@pytest.mark.bodyparams
def test_upload_inalvid_key():
    key1 = create_key(id_length=15)
    key2 = create_key(16, origins=['DEE'])
    key3 = create_key(16, origins=['DE'])
    key3.pop('timestamp')
    r = client.post(KEYS_PREFIX, json=key1, allow_redirects=True)
    assert r.status_code == 422
    r = client.post(KEYS_PREFIX, json=key2, allow_redirects=True)
    assert r.status_code == 422
    r = client.post(KEYS_PREFIX, json=key3, allow_redirects=True)
    assert r.status_code == 422
