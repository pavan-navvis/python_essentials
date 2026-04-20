from pydantic import BaseModel, ValidationError, Field, EmailStr
from typing import Annotated

# Annotated[data_type, constraints]
# Field can be used to add constraints


class User(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20)]
    email: EmailStr
    age: Annotated[int, Field(ge=15, le=100)]


try:
    user1 = User(username="Pavan", email="some_email.com", age=13)
    print(user1)
except ValidationError as e:
    print(e)
