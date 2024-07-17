import pytest

from src.schema import Extra, SearchDataSchema
from tests.html import detail_page, search_page


@pytest.fixture
def mock_search_page_html():
    return search_page.html


@pytest.fixture
def mock_detail_page_html():
    return detail_page.html


@pytest.fixture
def search_page_result():
    return [
        "/openstack/openstack",
        "/JiYou/openstack",
        "/ContainX/openstack4j",
        "/openstack/openstack-ansible",
        "/php-opencloud/openstack",
        "/kubernetes/cloud-provider-openstack",
        "/terraform-provider-openstack/terraform-provider-openstack",
        "/openstack/openstack-manuals",
        "/openstack/openstack-helm",
        "/openstack/openstacksdk",
    ]


@pytest.fixture
def parsed_data():
    return [
        SearchDataSchema(
            url="https://github.com/openstack/openstack",
            extra=Extra(owner="openstack", language_stats={"Python": 100.0}),
        ),
        SearchDataSchema(
            url="https://github.com/openstack/openstack-helm",
            extra=Extra(
                owner="openstack",
                language_stats={
                    "Shell": 86.6,
                    "Python": 10.4,
                    "Smarty": 2.6,
                    "Makefile": 0.4,
                },
            ),
        ),
    ]


@pytest.fixture
def mock_proxies():
    return [
        "https://proxy1.com:80",
        "https://proxy2.com:80",
        "https://proxy3.com:80",
        "https://proxy4.com:80",
        "https://proxy5.com:80",
        "https://proxy6.com:80",
        "https://proxy7.com:80",
        "https://proxy8.com:80",
        "https://proxy9.com:80",
        "https://proxy10.com:80",
    ]


@pytest.fixture
def mock_shared_proxy():
    return {
        "http://": "https://proxy1.com:80",
        "https://": "https://proxy1.com:80",
    }
