from sqlmodel import Field, SQLModel

class Links(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True, unique=True)
    url: str