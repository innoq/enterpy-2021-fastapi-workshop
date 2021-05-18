import fastapi

router = fastapi.APIRouter(prefix='/keys')

all_keys = []

@router.get('/')
async def download_all_keys(limit: int = 0):
    if 0 < limit < len(all_keys):
        return all_keys[:limit]
    return all_keys

@router.get('/{country}')
async def download_country_keys(country: str):
    keys = []
    for key in all_keys:
        if key['origin'] == country:
            keys.append(key)
    return keys
