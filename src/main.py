import asyncio
import contextvars
import random
from urllib.parse import urlencode, urljoin

import httpx
from fake_useragent import UserAgent
from parsel import Selector

from src import xpath
from src.schema import Extra, SearchDataSchema, SearchResultSchema, SearchSchema
from src.settings import Settings

settings = Settings()

shared_proxy = contextvars.ContextVar("shared_proxy")


def select_random_proxy(proxy_list: list[str]) -> dict[str, str] | None:
    if not proxy_list:
        return None
    selected_proxy = random.choice(proxy_list)
    return {"http://": selected_proxy, "https://": selected_proxy}


def get_search_url(scraping_data: SearchSchema) -> str:
    query_params = scraping_data.get_query_params()
    encodec_params = urlencode(query_params)
    return f"{settings.base_url}/search?{encodec_params}"


async def get_page_html(url: str) -> httpx.Response:
    proxies = shared_proxy.get()
    print("proxy:", proxies, "url:", url)
    headers = get_headers()
    async with httpx.AsyncClient(headers=headers, proxies=proxies) as client:
        response = await client.get(url, timeout=10)
        return response


def get_headers() -> dict[str, str]:
    user_agent = UserAgent(platforms="pc")
    return {
        "User-Agent": user_agent.random,
        "Accept": "text/html",
    }


def parse_search_page(page_body: str) -> list[str]:
    selector = Selector(page_body)
    links = selector.xpath(xpath.SEARCH_RESULTS).getall()
    return links


def parse_languages(selector: Selector) -> dict[str, float]:
    result = {}
    languages = selector.xpath(xpath.LANGUAGES)
    for language in languages:
        lang = language.xpath(xpath.LANGUAGE_TITLE).get()
        perc = language.xpath(xpath.LANGUAGE_PERCENT).re_first(r"\d+\.?\d+")
        result[lang] = float(perc)
    return result


async def parse_search_details(details_urls: list[str]) -> SearchResultSchema:
    results = []

    tasks = [
        asyncio.create_task(get_page_html(urljoin(settings.base_url, url)))
        for url in details_urls
    ]
    responses: tuple[httpx.Response] = await asyncio.gather(*tasks)

    for response in responses:
        selector = Selector(response.text)
        owner = selector.xpath(xpath.OWNER).get("not found")
        language_stats = parse_languages(selector)
        extra = Extra(owner=owner, language_stats=language_stats)
        results.append(SearchDataSchema(url=str(response.url), extra=extra))

    return SearchResultSchema(results)


async def collect_data(url: str) -> SearchResultSchema:
    response = await get_page_html(url)
    result_detail_links = parse_search_page(response.text)
    result: SearchResultSchema = await parse_search_details(result_detail_links)
    return result


async def get_search_results(scraping_data: SearchSchema) -> str:
    selected_random_proxy = select_random_proxy(scraping_data.proxies)
    shared_proxy.set(selected_random_proxy)

    search_url = get_search_url(scraping_data)
    results: SearchResultSchema = await collect_data(search_url)
    return results.model_dump_json(indent=4)
