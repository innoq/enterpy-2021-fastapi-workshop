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


# TODO: Eine Dependency implementieren
#  Implementiere 'extract_roles' die aus des dem Cookie 'token' die Rollen des Users extrahiert und als
#  Liste von Strings zurück gibt. Binde 'extract_roles' als Dependency ein.
#  Das Cookie 'token' enthält eine eine base64 kodierte JSON-Liste.
@router.get('/tan', status_code=200)
async def download_tans(roles: List[str]):
    check_role(roles, 'user', 'admin')
    return TanList(tans=keys.tans)


# TODO: Eine Dependency implementieren
#  Binde auch hier 'extract_roles' als Dependecy ein
@router.post('/tan', status_code=201)
async def upload_tans(tanlist: TanList, roles: List[str]):
    check_role(roles, 'admin')
    keys.tans += tanlist.tans
