from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyobjectId = Annotated[str, BeforeValidator(str)]


class StudentModel(BaseModel):
    id: Optional[PyobjectId] = Field(alias='_id', default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    course: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            'example': {
                'name': 'Hylan Silva',
                'email': 'hylansilva@hylansilva.dev',
                'course': 'Internet Systems',
            }
        },
    )


class UpdateStudentModel(BaseModel):

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    course: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            'example': {
                'name': 'Hylan Silva',
                'email': 'hylansilva@hylansilva.dev',
                'course': 'Internet Systems',
            }
        },
    )


class StudentCollection(BaseModel):
    students: List[StudentModel]
