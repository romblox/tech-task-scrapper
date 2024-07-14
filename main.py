import asyncio
import contextvars
import json
import random
from urllib.parse import urljoin

import httpx
from fake_useragent import UserAgent
from parsel import Selector

from schema import Extra, SearchDataSchema, SearchResultSchema, SearchSchema

XPATH_SEARCH_RESULTS = '//div[@data-testid="results-list"]//h3//div[contains(@class, "search-title")]/a/@href'
XPATH_OWNER = 'normalize-space(//a[@rel="author"]/text())'
XPATH_LANGUAGES = "//div[contains(./h2, 'Language')]/ul//a"
XPATH_LANGUAGE_TITLE = "./span[@class]/text()"
XPATH_LANGUAGE_PERCENT = "./span[@class]/following-sibling::span/text()"

BASE_URL = "https://github.com"
QUERY_PARAM = "/search?q={keyword}&type={search_type}"
SEARCH_URL = urljoin(BASE_URL, QUERY_PARAM)


proxies = contextvars.ContextVar("proxies")


def select_proxy() -> dict[str, str] | None:
    proxy_list = proxies.get()
    if not proxy_list:
        return None
    selected_proxy = random.choice(proxy_list)
    return {"http://": selected_proxy, "https://": selected_proxy}


async def get_page_html(url: str) -> httpx.Response:
    proxies = select_proxy()
    print("proxy:", proxies, "url:", url)
    headers = get_headers()
    async with httpx.AsyncClient(headers=headers, proxies=proxies) as client:
        response = await client.get(url, follow_redirects=True, timeout=10)
        return response


def get_headers():
    user_agent = UserAgent(platforms="pc")
    return {
        "User-Agent": user_agent.random,
        "Accept": "text/html",
    }


def parse_search_page(page_body: str) -> list[str]:
    selector = Selector(page_body)
    links = selector.xpath(XPATH_SEARCH_RESULTS).getall()
    return links


def parse_languages(selector: Selector) -> dict[str, float]:
    result = {}
    languages = selector.xpath(XPATH_LANGUAGES)
    for language in languages:
        lang = language.xpath(XPATH_LANGUAGE_TITLE).get()
        perc = language.xpath(XPATH_LANGUAGE_PERCENT).re_first(r"\d+\.?\d+")
        result[lang] = float(perc)
    return result


async def parse_search_details(details_urls: list[str]) -> SearchResultSchema:
    results = []

    tasks = [
        asyncio.create_task(get_page_html(urljoin(BASE_URL, url)))
        for url in details_urls
    ]
    responses: tuple[httpx.Response] = await asyncio.gather(*tasks)

    for response in responses:
        selector = Selector(response.text)
        owner = selector.xpath(XPATH_OWNER).get("not found")
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
    proxies.set(scraping_data.proxies)

    tasks = [
        asyncio.create_task(
            collect_data(
                SEARCH_URL.format(keyword=keyword, search_type=scraping_data.type)
            )
        )
        for keyword in scraping_data.keywords
    ]
    results: tuple[SearchResultSchema] = await asyncio.gather(*tasks)

    data = []
    for res in results:
        data.extend(res.model_dump())

    return json.dumps(data, indent=4)


if __name__ == "__main__":  # pragma: no cover
    input_data = """
                {
                "keywords": [
                    "openstack",
                    "nova",
                    "css"
                ],
                "type": "Repositories"
            }
        """

    # use it in case you have working list of proxies
    input_data_with_proxies = """
            {
            "keywords": [
                "openstack",
                "nova",
                "css"
            ],
            "proxies": [
                "http://5.75.200.249:80",
                "http://35.185.196.38:3128"
            ],
            "type": "Repositories"
        }
    """

    result = asyncio.run(
        get_search_results(SearchSchema.model_validate_json(input_data))
    )

    print(result)

    # You can use more convenient way to pass input data
    # with using SearchSchema model
    # result = asyncio.run(
    #     get_search_results(
    #         SearchSchema(
    #             keywords=["openstack", "nova", "css"],
    #             type="Repositories",
    #             proxies=[
    #                 "http://5.75.200.249:80",
    #                 "http://35.185.196.38:3128",
    #             ],
    #         )
    #     )
    # )
    #
    # print(result)
