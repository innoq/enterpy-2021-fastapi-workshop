import fastapi
import uvicorn

from pct.keys import keys

app = fastapi.FastAPI()
app.include_router(keys.router)

@app.get('/welcome')
async def index():
    return 'Hello enterPY!'

if __name__ == '__main__':
    uvicorn.run('main:app', port=10000, reload=True)