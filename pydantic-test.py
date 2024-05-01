import datetime
from pprint import pprint
import re

from pydantic import BaseModel, validator, BaseSettings


class Tag(BaseModel):
    id: int
    name: str


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    tags: list[Tag]

    @validator("year")
    def validate_year(cls, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise ValueError(f'Publish year must be less than current year - {current_year}')
        return value


valid_book = """{
    "id": 1,
    "title": "Война и мир",
    "author": "Лев Толстой",
    "year": 1869,
    "tags": [
        {
            "id": 1, "name": "роман"
        },
        {
            "id": 2, "name": "классика"
        }
    ]
}"""

invalid_book = """{
    "id": 2,
    "title": "Хоббит",
    "author": "Толкиен",
    "year": 2030,
    "tags": [{"id": 3, "name": "Фэнтэзи"}]
}"""

try:
    valid_result = Book.parse_raw(valid_book)
    pprint(valid_result.json(exclude={'id'}, ensure_ascii=False))
    invalid_book = Book.parse_raw(invalid_book)
except ValueError as e:
    pprint(e.errors())


class Settings(BaseSettings):
    admin_email: str
    admin_password: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @validator("admin_email")
    def validate_email(cls, value):
        if not bool(re.fullmatch(r'[\w.-]+@[\w-]+\.[\w.]+', value)):
            raise ValueError("Email is invalid")
        return value

    @validator("admin_password")
    def validate_password(cls, value):
        password_length = len(value)
        if password_length < 8 or password_length > 16:
            raise ValueError("The password must be between 8 and 16 characters long")
        return value


try:
    settings = Settings()
    print(settings.admin_email)
    print(settings.admin_password)
except ValueError as e:
    pprint(e.errors())


