import enum
from typing import List, Literal

import fastapi
from fastapi import Response
from fastapi.params import Body, Path, Header
from pydantic import BaseModel, constr

router = fastapi.APIRouter(prefix='/keys')

# Wird vom Test automatisch befüllt. Nicht ändern!
# Einträge sind Dicts in der Form {id: '<hexstring:32>', origin: '<DE|NL|GB>', timestamp: float}
all_keys = []

# Wird vom Test automatisch befüllt. Nicht ändern!
# Einträge sind str in der Form '<hexstring:4>'
tans = []

COUNTRY_VALIDATION_REGEX = '^(DE|NL|GB)$'
TAN_VALIDATION_REGEX = '^[0-9A-Fa-f]{4}$'
ID_VALIDATION_REGEX = '^[0-9A-Fa-f]{32}$'


# TODO: Pydantic Model erstellen
#  Erstelle ein Pydantic Model für einen Key

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


# TODO: POST-Request auf Pydantic Model mappen
#  Nimm auf dem Pfad '/bundle' eine Liste von Keys entgegen. Füge die Keys aus der Liste 'all_keys' hinzu.
#  Nutze für das Mapping das Pydantic Model von oben.
#  Prüfe weiterhin den 'X-Tan' header analog zu 'upload_keys'
