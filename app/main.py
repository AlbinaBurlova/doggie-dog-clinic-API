from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', summary='Root')
def root():
    return {'Welcome to Doggie Dog Clinic Microservice!'}


@app.get('/post', summary='Get Post')
def get_post():
    return post_db


@app.get('/dog', response_model=List[Dog], summary='Get Dogs')
def get_dogs(kind: DogType = None) -> List[Dog]:
    if kind is not None:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    else:
        return list(dogs_db.values())


@app.get('/dog', summary='Create Dog')
def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=409, detail="Dog already exists")
    dogs_db[dog.pk] = dog
    return dog


@app.get('/dog/{pk}', summary='Get Dog By Pk')
def get_dog_by_pk(pk: int):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dogs_db[pk]


@app.get('/dog/{pk}', summary='Update Dog')
def update_dog(pk: int, dog: Dog):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    dogs_db[pk] = dog
    return dog
