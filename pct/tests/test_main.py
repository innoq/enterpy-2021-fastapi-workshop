import random
import secrets
import time
import typing

import pytest
from fastapi.testclient import TestClient

from pct.main import app

KEYS_PREFIX = '/keys'

client = TestClient(app)


def create_key(id_length = 16, origins = ['DE', 'GB', 'NL'], timestamp = time.time()):
    return {
        'id': secrets.token_hex(id_length),
        'origin': random.choice(origins),
        'timestamp': timestamp
    }


def create_test_keys(n: int) -> typing.List[typing.Dict]:
    return [create_key() for _ in range(n)]


def inject_test_keys(test_keys):
    from pct.keys import keys
    keys.all_keys += test_keys


def delete_injected_test_keys():
    from pct.keys import keys
    keys.all_keys.clear()


def create_test_tans(n: int) -> typing.List[str]:
    return [secrets.token_hex(2) for _ in range(n)]


def inject_test_tans(test_tans):
    from pct.keys import keys
    keys.tans += test_tans


def delete_injected_test_tans():
    from pct.keys import keys
    keys.tans.clear()


@pytest.fixture(scope='function')
def testdata():
    N = 25
    test_tans = create_test_tans(N)
    inject_test_tans(test_tans)
    test_keys = create_test_keys(N)
    inject_test_keys(test_keys)
    yield test_keys, test_tans
    delete_injected_test_keys()
    delete_injected_test_tans()


@pytest.mark.helloenterpy
def test_hello_enterpy():
    r = client.get('/welcome')
    assert r.json() == "Hello enterPY!"


@pytest.mark.downloadkeys
def test_download_keys(testdata):
    r = client.get(KEYS_PREFIX)
    assert r.status_code == 200
    keys = r.json()
    test_keys, _ = testdata
    assert keys == test_keys


@pytest.mark.queryparams
def test_download_keys_limit(testdata):
    keys, _ = testdata
    r = client.get(f'{KEYS_PREFIX}?limit=12')
    assert r.status_code == 200
    downloaded_keys = r.json()
    assert len(downloaded_keys) == 12
    for key in downloaded_keys:
        assert key in keys

@pytest.mark.queryparams
def test_download_keys_invalid_limit():
    r = client.get(f'{KEYS_PREFIX}?limit=foo')
    assert r.status_code == 422


@pytest.mark.pathparams
def test_download_keys_country(testdata):
    keys, _ = testdata
    COUNTRY = 'DE'
    r = client.get(f'{KEYS_PREFIX}/{COUNTRY}')
    assert r.status_code == 200
    downloaded_keys = r.json()
    for key in downloaded_keys:
        assert key in keys
        assert key['origin'] == COUNTRY


@pytest.mark.pathparams
def test_download_keys_invalid_country():
    COUNTRY = 'DEE'
    r = client.get(f'{KEYS_PREFIX}/{COUNTRY}')
    assert r.status_code == 422


@pytest.mark.bodyparams
def test_upload_key():
    tans = create_test_tans(2)
    inject_test_tans(tans)
    key1 = create_key(id_length=16)
    key2 = create_key(id_length=16)
    r = client.post(KEYS_PREFIX, json=key1, headers={ 'X-Tan': tans.pop()}, allow_redirects=True)
    assert r.status_code == 201
    r = client.post(KEYS_PREFIX, json=key2, headers={ 'X-Tan': tans.pop()}, allow_redirects=True)
    assert r.status_code == 201
    r = client.get(KEYS_PREFIX)
    assert r.status_code == 200
    keys = r.json()
    for key in keys:
        assert key in [key1, key2]


@pytest.mark.bodyparams
def test_upload_invalid_key():
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


@pytest.mark.headerparams
def test_upload_tan(testdata: typing.List):
    keys, tans = testdata
    for key in keys:
        r = client.post(KEYS_PREFIX, json=key, headers={'X-Tan': tans.pop()}, allow_redirects=True)
        assert r.status_code == 201


@pytest.mark.headerparams
def test_upload_without_tan(testdata: typing.List):
    keys, tans = testdata
    for key in keys:
        r = client.post(KEYS_PREFIX, json=key, allow_redirects=True)
        assert r.status_code == 401


@pytest.mark.headerparams
def test_upload_with_unknown_tan(testdata: typing.List):
    keys, tans = testdata
    while True:
        tan = create_test_tans(1).pop()
        if tan not in tans:
            break
    for key in keys:
        r = client.post(KEYS_PREFIX, json=key, headers={'X-Tan': tan}, allow_redirects=True)
        assert r.status_code == 401


@pytest.mark.headerparams
def test_upload_with_invalid_tan(testdata: typing.List):
    keys, _ = testdata
    for key in keys:
        r = client.post(KEYS_PREFIX, json=key, headers={'X-Tan': 'foo'}, allow_redirects=True)
        assert r.status_code == 422
