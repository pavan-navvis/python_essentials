from pydantic import BaseModel, ValidationError


class User(BaseModel):
    username: str
    email: str
    age: int


user1 = User(username="Pavan", email="some_email.com", age=25)
print(user1)
print(user1.model_dump())
print(user1.model_dump_json(indent=4))

try:
    user2 = User(username=3, email=None, age="25")
    print(user2)
except ValidationError as e:
    print(e)
