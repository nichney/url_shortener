from pydantic import BaseModel, HttpUrl


class CreateAliasIn(BaseModel):
    url: HttpUrl
    server_url: HttpUrl
    custom_alias: str | None = None


class CreateAliasResponse(BaseModel):
    url: HttpUrl
    alias: HttpUrl


class ErrorResponse(BaseModel):
    message: str