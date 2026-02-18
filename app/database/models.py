from sqlmodel import Field, SQLModel

class Links(SQLModel):
    id: str = Field(primary_key=True, index=True, unique=True)
    url: str