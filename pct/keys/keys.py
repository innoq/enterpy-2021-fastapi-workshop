import fastapi
from fastapi.params import Body, Path

router = fastapi.APIRouter(prefix='/keys')

# Wird vom Test automatisch befüllt. Nicht ändern!
# Einträge sind Dicts in der Form {id: '<hexstring:32>', origin: '<DE|NL|GB>', timestamp: float}
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

# TODO: POST-Request annehmen
#  Nimm auf dem Pfad '/' des APIRouters eines Datensatz entgegen und füge ihn 'all_keys' in der
#  oben beschriebenen Form hinzu. Gib den status code 201 zurück.
#  Der Datensatz wird als JSON im Body geliefert. Invalide Datensätze werden verworfen. In dem Fall muss der
#  status code 422 zurück geliefert werden (standard status code wenn FastAPI nicht validieren kann).
