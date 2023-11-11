from datetime import datetime
from typing import List
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
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


@app.get('/')
def root():
    return {"message": "Hello"}


@app.post("/post", response_model=Timestamp)
def get_post():
    next_id = post_db[-1].id + 1
    post_db.append(Timestamp(id=next_id, timestamp=datetime.now().day))
    return post_db[-1]


@app.get("/dog", response_model=List[Dog])
def get_dogs(kind: DogType):
    return [dogs_db[i] for i in dogs_db if dogs_db[i].kind == kind]


@app.get("/dog/{pk}", response_model=Dog)
def get_dog_pk(pk: int):
    if pk in dogs_db.keys():
        return dogs_db[pk]
    else:
        raise HTTPException(status_code=400, detail=f"{pk} нет в базе данных")


@app.post("/dog", response_model=Dog)
def create_dog_by_pk(new_dog: Dog):
    dogs_db[new_dog.pk] = new_dog
    return new_dog


@app.patch("/dok/{pk}", response_model=Dog)
def update_dog(up_dog: Dog, pk: int):
    if pk != up_dog.pk:
        raise HTTPException(status_code=400, detail=f"Введенные вами pk в Request body = {pk} "
                                                    f"и в URI {up_dog.pk} не совпадают")
    else:
        dogs_db[pk] = up_dog
        return dogs_db[pk]