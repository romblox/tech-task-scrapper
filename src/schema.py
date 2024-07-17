from typing import Literal

from pydantic import BaseModel, RootModel


class SearchSchema(BaseModel):
    keywords: list[str]
    proxies: list[str] | None = None
    type: Literal["Repositories", "Issues", "Wikis"]

    def get_query_params(self) -> dict[str, str]:
        return {
            "q": " OR ".join(self.keywords),
            "type": self.type.lower(),
        }


class Extra(BaseModel):
    owner: str
    language_stats: dict[str, float] = {}


class SearchDataSchema(BaseModel):
    url: str
    extra: Extra


class SearchResultSchema(RootModel[list[SearchDataSchema]]):
    pass