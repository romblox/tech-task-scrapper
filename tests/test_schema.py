from src.schema import SearchSchema


def test_search_schema():
    scraping_data = SearchSchema(
        keywords=["openstack", "nova", "css"],
        type="Repositories",
        proxies=["https://proxy1.com:80", "https://proxy2.com:80"],
    )

    result = scraping_data.get_query_params()
    print(result)

    expected = {"q": "openstack OR nova OR css", "type": "repositories"}

    assert isinstance(result, dict), "The result is not a dictionary."
    assert result["q"] == expected["q"], "The query parameters are incorrect."
    assert result["type"] == expected["type"], "The query parameters are incorrect."
