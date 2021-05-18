# TODO: auf Pfad '/welcome' reagieren
# TODO: 'Hello enterPY!' zurückgeben

import fastapi
import uvicorn

app = fastapi.FastAPI()

@app.get('/')
async def index():
    return 'Hello World'

if __name__ == '__main__':
    uvicorn.run('main:app', port=10000, reload=True)