import time
import typing

import fastapi
import uvicorn

from pct.keys import keys
from pct.labs import labs

app = fastapi.FastAPI()
app.include_router(keys.router)
app.include_router(labs.router, prefix='/labs')


@app.get('/welcome')
async def index():
    return 'Hello enterPY!'


# TODO: Eine Middleware erstellen
#  Implementiere eine middleware die jedem Response einen 'Server-Timing'-Header hinzufügt
#  Der Inhalt des 'Server-Timing'-Header sollte die Zeit sein, die für die Bearbeitung des
#  Request benötigt wurde.



if __name__ == '__main__':
    uvicorn.run('main:app', port=10000, reload=True)