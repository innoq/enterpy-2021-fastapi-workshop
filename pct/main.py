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


@app.middleware('http')
async def middleware(r: fastapi.Request, call_next: typing.Callable):
    start: float = time.time()
    res: fastapi.Response = await call_next(r)
    end: float = time.time()
    res.headers['Server-Timing'] = f'cpu;dur={end-start}'
    return res


if __name__ == '__main__':
    uvicorn.run('main:app', port=10000, reload=True)