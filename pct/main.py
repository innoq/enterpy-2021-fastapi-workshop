# TODO: Einen zusätzlichen APIRouter einbinden
#  Binde den APIRouter aus keys.py ein

import fastapi
import uvicorn

app = fastapi.FastAPI()

@app.get('/welcome')
async def index():
    return 'Hello enterPY!'

if __name__ == '__main__':
    uvicorn.run('main:app', port=10000, reload=True)