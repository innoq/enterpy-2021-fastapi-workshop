import enum
from typing import List, Literal

import fastapi
from fastapi import Response
from fastapi.params import Body, Path, Header
from pydantic import BaseModel, constr

router = fastapi.APIRouter(prefix='/keys')

all_keys = []

tans = []

COUNTRY_VALIDATION_REGEX = '^(DE|NL|GB)$'
TAN_VALIDATION_REGEX = '^[0-9A-Fa-f]{4}$'
ID_VALIDATION_REGEX = '^[0-9A-Fa-f]{32}$'


class CountryEnum(str, enum.Enum):
    DE = 'DE'
    NL = 'NL'
    GB = 'GB'

class Key(BaseModel):
    id: constr(regex=ID_VALIDATION_REGEX)
    # origin: constr(regex=COUNTRY_VALIDATION_REGEX)
    # origin: CountryEnum
    origin: Literal['DE', 'NL', 'GB']
    timestamp: float


@router.get('/')
async def download_all_keys(limit: int = 0):
    if 0 < limit < len(all_keys):
        return all_keys[:limit]
    return all_keys


@router.get('/{country}')
async def download_country_keys(country: str = Path(..., regex=COUNTRY_VALIDATION_REGEX)):
    keys = []
    for key in all_keys:
        if key['origin'] == country:
            keys.append(key)
    return keys


@router.post('/', status_code=201)
async def upload_key(res: Response,
                     id: str = Body(..., regex=ID_VALIDATION_REGEX),
                     origin: str = Body(..., regex=COUNTRY_VALIDATION_REGEX),
                     timestamp: float = Body(...),
                     x_tan: str = Header(None, regex=TAN_VALIDATION_REGEX)):
    if x_tan not in tans:
        res.status_code = 401
        return
    else:
        key = { 'id': id, 'origin': origin, 'timestamp': timestamp}
        tans.remove(x_tan)
        all_keys.append(key)


@router.post('/bundle', status_code=201)
async def upload_key_bundle(res: Response,
                     keys: List[Key],
                     x_tan: str = Header(None, regex=TAN_VALIDATION_REGEX)):
    if x_tan not in tans:
        res.status_code = 401
        return
    else:
        for key in keys:
            all_keys.append(key)
    tans.remove(x_tan)

