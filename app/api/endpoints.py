from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.api.schemas import CreateAliasIn, CreateAliasResponse, ErrorResponse
from app.repositories.link_repo import LinkRepository
from app.dependencies import get_link_repo

from app.logic.link_generator import generate_new_short_link


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
async def create_short_link(payload: CreateAliasIn, repo: LinkRepository = Depends(get_link_repo)):
    alias = await generate_new_short_link(repo, payload.url, payload.custom_alias)
    return CreateAliasResponse(url=payload.url, alias=alias)
