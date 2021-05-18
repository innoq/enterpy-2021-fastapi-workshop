import fastapi
from fastapi import Response
from fastapi.params import Body, Path, Header

router = fastapi.APIRouter(prefix='/keys')

all_keys = []

tans = []

@router.get('/')
async def download_all_keys(limit: int = 0):
    if 0 < limit < len(all_keys):
        return all_keys[:limit]
    return all_keys


@router.get('/{country}')
async def download_country_keys(country: str = Path(..., regex='^(DE|NL|GB)$')):
    keys = []
    for key in all_keys:
        if key['origin'] == country:
            keys.append(key)
    return keys


@router.post('/', status_code=201)
async def upload_key(res: Response,
                     id: str = Body(..., regex='^[0-9A-Fa-f]{32}$'),
                     origin: str = Body(..., regex='^(DE|NL|GB)$'),
                     timestamp: float = Body(...),
                     x_tan: str = Header(None, regex='^[0-9A-Fa-f]{4}$')):
    if x_tan not in tans:
        res.status_code = 401
        return
    else:
        key = { 'id': id, 'origin': origin, 'timestamp': timestamp}
        tans.remove(x_tan)
        all_keys.append(key)
