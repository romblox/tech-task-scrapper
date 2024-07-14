import asyncio
import json
from unittest.mock import AsyncMock

import pytest
from httpx import Request

import main
from main import (
    SearchResultSchema,
    Selector,
    collect_data,
    get_headers,
    get_page_html,
    httpx,
    parse_languages,
    parse_search_details,
    parse_search_page,
    proxies,
    select_proxy,
)
from schema import SearchSchema


def test_get_headers():
    headers = get_headers()
    assert "User-Agent" in headers
    assert "Accept" in headers
    assert headers["Accept"] == "text/html"


@pytest.mark.asyncio
async def test_get_page_html(monkeypatch):
    # Mock proxies
    proxies.set(None)

    async def mock_get(*args, **kwargs):
        return httpx.Response(200, text="Mocked page HTML")

    monkeypatch.setattr("httpx.AsyncClient.get", AsyncMock(side_effect=mock_get))

    response = await get_page_html("https://example.com")

    assert response.status_code == 200
    assert response.text == "Mocked page HTML"


def test_parse_search_page(mock_search_page_html, search_page_result):
    result_urls = parse_search_page(mock_search_page_html)

    expected_urls = search_page_result

    assert len(result_urls) == len(
        expected_urls
    ), "The number of parsed URLs does not match the expected number."
    assert (
        result_urls == expected_urls
    ), "The parsed URLs do not match the expected URLs."


def test_parse_languages(mock_detail_page_html):
    selector = Selector(mock_detail_page_html)
    result = parse_languages(selector)

    expected_result = {"Python": 100.0}

    assert (
        result == expected_result
    ), "The parsed languages do not match the expected languages."


@pytest.mark.asyncio
async def test_parse_search_details(monkeypatch, mock_detail_page_html):
    # Prepare the mock response and patch the get_page_html function
    request = Request(method="GET", url="https://example.com/detail")
    mock_response = httpx.Response(200, text=mock_detail_page_html, request=request)
    async_mock = AsyncMock(return_value=mock_response)
    monkeypatch.setattr("main.get_page_html", async_mock)

    result: SearchResultSchema = await parse_search_details(
        ["https://example.com/detail"]
    )

    assert isinstance(
        result, SearchResultSchema
    ), "The result is not an instance of SearchResultSchema."
    assert len(result.root) == 1, "The number of results is incorrect."
    assert (
        result.root[0].url == "https://example.com/detail"
    ), "The URL of the result is incorrect."
    assert (
        result.root[0].extra.owner == "openstack"
    ), "The owner of the result is incorrect."
    assert result.root[0].extra.language_stats == {
        "Python": 100.0
    }, "The language stats of the result are incorrect."


@pytest.mark.asyncio
async def test_collect_data(monkeypatch, search_page_result, mock_detail_page_html):
    # Mock parse_search_page to return predefined URLs
    def mock_parse_search_page(*args, **kwargs):
        return search_page_result

    monkeypatch.setattr("main.parse_search_page", mock_parse_search_page)

    # Prepare the mock response and patch the get_page_html function
    request = Request(method="GET", url="https://example.com/detail")
    mock_response = httpx.Response(200, text=mock_detail_page_html, request=request)
    async_mock = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(main, "get_page_html", async_mock)

    result = await collect_data("https://example.com/search?q=openstack")

    print(result)

    assert isinstance(
        result, SearchResultSchema
    ), "The result is not an instance of SearchResultSchema."
    assert len(result.root) == len(
        search_page_result
    ), "The number of results is incorrect."


@pytest.mark.asyncio
async def test_get_search_results(monkeypatch, parsed_data):
    mock_result = SearchResultSchema(parsed_data)

    async def mock_asyncio_gather(*args, **kwargs):
        return (mock_result,)

    monkeypatch.setattr(asyncio, "gather", mock_asyncio_gather)

    test_search_schema = SearchSchema(keywords=["test"], type="Repositories")
    result = await main.get_search_results(test_search_schema)

    assert isinstance(result, str), "The result is not a string."
    assert len(result) > 0, "The result string is empty."

    data = json.loads(result)
    assert isinstance(data, list), "The result is not a list."
    assert len(data) == len(parsed_data), "The number of results is incorrect."
    assert all(
        isinstance(item, dict) for item in data
    ), "Not all items in the result are dictionaries."


def test_select_proxy(mock_proxies):
    # Mock the proxies
    proxies.set(mock_proxies)

    result = select_proxy()
    assert result is not None, "Expected a dictionary, got None"
    assert set(result.keys()) == {
        "http://",
        "https://",
    }, "Keys should be 'http://' and 'https://'"
    assert (
        result["http://"] in mock_proxies
    ), "The selected proxy should be one from the mock list"
    assert (
        result["https://"] == result["http://"]
    ), "HTTP and HTTPS proxies should match"


def test_select_proxy_without_proxy_list_passed(monkeypatch):
    proxies.set(None)
    result = select_proxy()
    assert result is None, "Expected None for an empty proxy list"


def test_select_proxy_on_random(mock_proxies):
    proxies.set(mock_proxies)

    # Call select_proxy() multiple times to check for rando of selection
    selections = [select_proxy() for _ in range(10)]

    # Extract just the HTTP or HTTPS proxy URLs for simplicity
    http_selections = [selection["http://"] for selection in selections if selection]

    # Check if all selected proxies are the same, indicating lack of randomness
    assert not all(
        proxy == http_selections[0] for proxy in http_selections
    ), "Proxies selected are not randomized"
