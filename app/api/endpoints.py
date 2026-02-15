from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.api.schemas import CreateAliasIn, CreateAliasResponse, ErrorResponse


router = APIRouter()


@router.get(
    "/{alias_url}",
    response_class=RedirectResponse,
    status_code=302
    )
async def redirect_from_alias_to_url():
    """Steps:
        1. Get url from cache
        2. If there is no value in cache, turn alias_url to ID and search in database. Usually, alias_url is base62 of ID, but it may be custom alias
        3. If there is no value in database, return 404
        4. Write extracted value to cache and return redirect 302
    """
    pass


@router.post(
    "/create",
    response_model=CreateAliasResponse
    )
async def create_short_link(payload: CreateAliasIn):
    """Steps:
        1. Generate unique ID (snowflake)
        2. Turn ID to base62
        3. Save (ID, url, custom_alias) to DB
        4. If custom_alias specified, concatinate it with server_url and return. If not, add base62 ID to server_url and return it
    """
    pass
