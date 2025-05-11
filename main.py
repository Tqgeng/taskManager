# точка входа в приложение

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import models
from database import Base, engine
from routers import tasks
from routers import tasks_jwt_auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(tasks.router)
app.include_router(tasks.router_auth)
app.include_router(tasks_jwt_auth.router)


app.mount('/front', StaticFiles(directory='front'))


@app.get('/', tags=['Root'], summary='Тест апишки')
def read_root():
    return FileResponse('front/login.html')
    # return {'message': 'привет, все работает)'}

if __name__ == '__main__':
    # uvicorn.run('main:app', reload=True)
    uvicorn.run(app, host='0.0.0.0', port=8000)