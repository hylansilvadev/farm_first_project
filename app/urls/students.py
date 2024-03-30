from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Response, status
from pymongo import ReturnDocument

from app.core.database import db
from app.models import StudentCollection, StudentModel, UpdateStudentModel

router = APIRouter(prefix='/students', tags=['Students'])

student_collection = db.get_collection('students')


@router.post(
    '/',
    response_description='Adicionar novo estudante',
    response_model=StudentModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_student(student: StudentModel = Body(...)):
    new_student = await student_collection.insert_one(
        student.model_dump(by_alias=True, exclude=['id'])
    )

    created_student = await student_collection.find_one(
        {'_id': new_student.inserted_id}
    )

    return created_student


@router.get(
    '/',
    response_description='Listagem de estudantes',
    response_model=StudentCollection,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def get_all_students():
    return StudentCollection(
        students=await student_collection.find().to_list(1000)
    )


@router.get(
    '/{id}',
    response_description='Buscar um estudante',
    response_model=StudentModel,
    response_model_by_alias=False,
)
async def get_user_by_id(id: str):
    if (
        student := await student_collection.find_one({'_id': ObjectId(id)})
    ) is not None:
        return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'o estudante {id} nao foi encontrado!',
    )


@router.put(
    '/{id}',
    response_description='Atualizar os dados de um estudante',
    response_model=UpdateStudentModel,
    response_model_by_alias=False,
)
async def update_student():
    student = {
        k: v
        for k, v in student.model_dump(by_alias=True).items()
        if v is not None
    }

    if len(student) >= 1:
        update_result = await student_collection.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': student},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(
                status_code=404, detail=f'Student {id} not found'
            )

    if (
        existing_student := await student_collection.find_one({'_id': id})
    ) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f'Student {id} not found')


@router.delete('/{id}', response_description='Delete a student')
async def delete_student(id: str):
    delete_result = await student_collection.delete_one({'_id': ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f'Student {id} not found')
