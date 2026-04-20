from pydantic import (
    BaseModel,
    ValidationError,
    Field,
    EmailStr,
    field_validator,
    model_validator,
    computed_field,
    ConfigDict,
)
from typing import Annotated


# field_validator is a after validator i.e. it runs after pydantic runs all the basic validation. It can also made to validate before by adding a mode="before" to the decorator
# add a ConfigDict to confugure how your BaseModel class behaves
# strict=True --> means model wont automatically type cast somethigs --> normally, basemodel would convert "123" to  123.
class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True, strict=True, validate_assignment=True
    )

    username: Annotated[str, Field(min_length=3, max_length=20)]
    email: EmailStr
    password: str
    confirm_password: str
    age: Annotated[int, Field(ge=15, le=100)]
    first_name: str = ""
    last_name: str = ""
    fav_books: list[str] = Field(default_factory=list)  # an empty list

    @field_validator("username")
    @classmethod
    def validate_username(cls, name: str) -> str:
        if not name.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric")
        return name.lower()

    # complete model validation
    @model_validator(mode="after")
    def check_password(self) -> "User":
        if self.password != self.confirm_password:
            raise ValueError("Passwords dont match!")
        return self

    # used for computed fields
    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name}_{self.last_name}"
        return self.username


try:
    user1 = User(
        username="Pavan_V",
        email="some_email@some.com",
        password="hhh",
        confirm_password="hhh",
        age=16,
        first_name="Awesome",
        last_name="Guy",
    )
    print(user1)
    print(user1.model_dump_json(indent=2, include={"username", "age"}))
    print(user1.model_dump_json(indent=2, exclude={"username", "age"}))

except ValidationError as e:
    print(e)
