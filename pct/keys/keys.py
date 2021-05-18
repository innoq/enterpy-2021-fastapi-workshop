import fastapi
from fastapi.params import Body, Path

router = fastapi.APIRouter(prefix='/keys')

all_keys = []


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
async def upload_key(id: str = Body(..., regex='^[0-9A-Fa-f]{32}$'), origin: str = Body(..., regex='^(DE|NL|GB)$'), timestamp: float = Body(...)):
    key = { 'id': id, 'origin': origin, 'timestamp': timestamp}
    all_keys.append(key)
