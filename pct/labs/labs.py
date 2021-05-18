import base64
import json
from typing import List

import fastapi
from pydantic import BaseModel, constr

from pct.keys.keys import TAN_VALIDATION_REGEX
from pct.keys import keys

router = fastapi.APIRouter()


class TanList(BaseModel):
    tans: List[constr(regex=TAN_VALIDATION_REGEX)]


def check_role(given_roles: List[str], *allowed_roles):
    for role in allowed_roles:
        if role in given_roles:
            break
    else:
        raise fastapi.HTTPException(fastapi.status.HTTP_401_UNAUTHORIZED,
                                    detail='you are missing the required permission')


def decode_token(token = fastapi.Cookie(...)):
    return base64.b64decode(token).decode('UTF-8')


def extract_roles(decode_token = fastapi.Depends(decode_token)):
    return json.loads(decode_token)


@router.get('/tan', status_code=200)
async def download_tans(roles : List[str] = fastapi.Depends(extract_roles)):
    check_role(roles, 'user', 'admin')
    return TanList(tans=keys.tans)


@router.post('/tan', status_code=201)
async def upload_tans(tanlist: TanList, roles: List[str] = fastapi.Depends(extract_roles)):
    check_role(roles, 'admin')
    keys.tans += tanlist.tans
