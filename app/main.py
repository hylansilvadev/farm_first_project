import uvicorn
from fastapi import FastAPI

from app.core.database import db
from app.urls.students import router as students_router


def create_aplication() -> FastAPI:
    try:
        db.create_collection('students')
    except Exception as e:
        print(e)
    app = FastAPI(
        docs_url='/', title='FARM Backend in FastApi', version='0.0.1'
    )
    app.include_router(students_router)
    return app


app = create_aplication()


@app.get('/root')
async def Root():
    return {'message': 'Hello World!'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
