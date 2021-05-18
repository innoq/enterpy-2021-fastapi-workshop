from fastapi.testclient import TestClient

from pct.main import app

import pytest

client = TestClient(app)

@pytest.mark.helloenterpy
def test_hello_enterpy():
    r = client.get('/welcome')
    assert r.status_code == 200
    assert r.json() == "Hello enterPY!"