from pydantic import HttpUrl

from app.repositories.link_repo import LinkRepository
from app.utils.snowflake import new_id
from app.utils.base62 import to_base62
from app.config.settings import BASE_URL

async def generate_new_short_link(repo: LinkRepository, url: HttpUrl, custom_alias: str | None = None) -> HttpUrl:
    # If custom_alias is not specified by user, we assume snowflake ID in base62 as alias to original link  
    if custom_alias:
        shard_key = custom_alias
        final_id = custom_alias
    else:
        final_id = to_base62(new_id())
        shard_key = final_id

    try:
        short_id = await repo.create_link(str(url), final_id)
    except Exception:
        return None

    return HttpUrl(str(BASE_URL) + "c/" + short_id)