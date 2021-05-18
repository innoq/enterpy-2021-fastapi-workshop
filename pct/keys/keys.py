import fastapi
from fastapi import Response
from fastapi.params import Body, Path, Header

router = fastapi.APIRouter(prefix='/keys')

# Wird vom Test automatisch befüllt. Nicht ändern!
# Einträge sind Dicts in der Form {id: '<hexstring:32>', origin: '<DE|NL|GB>', timestamp: float}
all_keys = []

# Wird vom Test automatisch befüllt. Nicht ändern!
# Einträge sind str in der Form '<hexstring:4>'
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


# TODO: Header-Parameter auswerten
#  Prüfe ob der Wert des 'X-Tan' in 'tans' vorhanden ist. Wenn ja, füge den empfangen 'key' wie gewohnt zu
#  'all_keys' hinzu. Entferne danach den Wert von 'X-Tan' aus 'tans' (einmalig).
#  Wenn nein, dann gebe den status_code 401 zurück und füge den empfangenen 'key' nicht 'all_keys' hinzu.
@router.post('/', status_code=201)
async def upload_key(res: Response,
                     id: str = Body(..., regex='^[0-9A-Fa-f]{32}$'),
                     origin: str = Body(..., regex='^(DE|NL|GB)$'),
                     timestamp: float = Body(...)):
    key = { 'id': id, 'origin': origin, 'timestamp': timestamp}
    all_keys.append(key)
