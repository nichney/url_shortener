from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.api.schemas import CreateAliasIn, CreateAliasResponse
from app.repositories.link_repo import LinkRepository
from app.dependencies import get_link_repo, get_redis_repo

from app.logic.link_generator import generate_new_short_link
from app.logic.link_getter import get_link


router = APIRouter()


@router.post(
    "/create",
    response_model=CreateAliasResponse
    )
async def create_short_link(payload: CreateAliasIn, repo: LinkRepository = Depends(get_link_repo)):
    alias = await generate_new_short_link(repo, payload.url, payload.custom_alias)
    return CreateAliasResponse(url=payload.url, alias=alias)


@router.get(
    "/c/{alias_url}",
    response_class=RedirectResponse,
    status_code=302
    )
async def redirect_from_alias_to_url(alias_url: str, repo: LinkRepository = Depends(get_link_repo), redis_db = Depends(get_redis_repo)):
    original_url = await get_link(repo, redis_db, alias_url)
    if not original_url:
        raise HTTPException(status_code=404, detail="Alias not found")

    return RedirectResponse(url=original_url, status_code=302)