# Python developer technical task  

## Task description
* Python 3
* The crawler should be as efficient as possible (fast, low memory usage, low CPU usage,...)
* Input:
    * Search keywords: a list of keywords to be used as search terms (unicode characters must be supported)
    * List of proxies: one of them should be selected and used randomly to perform all the HTTP requests (you can get a free list of proxies to work with at https://free-proxy-list.net/)
    * Type: the type of object we are searching for (Repositories, Issues and Wikis should be supported)
* Documentation about how to use it should be included
* Output: URLS for each of the results of the search
* The code should also include unit tests with a minimum code coverage of 90%
* For the purpose of this task you only have to process first page results
* For the purpose of this task we want to work with raw HTML, JSON API can't be used.
* You can use any library you consider useful for the task (e.g. HTTP libraries, parser libraries,...) but not frameworks (e.g. Scrapy)

### Example

`Keywords`: “openstack”, “nova” and “css”  
`Proxies`: “194.126.37.94:8080” and “13.78.125.167:8080”  
`Type`: “Repositories”

So the input will be a JSON containing:  

```json
{
  "keywords": [
    "openstack",
    "nova",
    "css"
  ],
  "proxies": [
    "194.126.37.94:8080",
    "13.78.125.167:8080"
  ],
  "type": "Repositories"
}
```

For the repository in the example above expected results should be now a JSON like:  
```json
[
  {
    "url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage",
    "extra": {
      "owner": "atuldjadhav",
      "language_stats": {
        "CSS": 52.0,
        "JavaScript": 47.2,
        "HTML": 0.8
      }
    }
  }
]
```


## Solution

The provided solution is a Python script designed for `web scraping GitHub search` results, focusing on extracting details such as repository links, repository owners, and programming language statistics.  

It leverages asynchronous programming with `asyncio`, `httpx` for making HTTP requests, and `parsel` for parsing HTML responses.  
The script uses `contextvars` to manage proxies, ensuring thread-safe operations across asynchronous tasks.  The random selection a proxy from a list of proxies in a contextvars, to distribute requests across different proxies and minimize the risk of being blocked by the target website.  

This script is a comprehensive example of modern asynchronous web scraping in Python, demonstrating best practices for using proxies, parsing HTML, and managing asynchronous tasks.

The script utilizes several Python packages, each serving a specific purpose in the context of asynchronous web scraping and handling HTTP requests.  

Packages which where used:  

1. `asyncio`: This is a Python library to write concurrent code using the async/await syntax. It is used for managing asynchronous operations, allowing the script to handle multiple tasks and I/O operations efficiently, which is crucial for web scraping tasks that involve making numerous HTTP requests and waiting for responses.  
2. `httpx`: A fully featured HTTP client for Python 3, which supports async/await paradigms. httpx is used for making asynchronous HTTP requests to fetch web pages. It is an alternative to requests but with support for asynchronous operations, making it suitable for concurrent web scraping.  
3. `parsel`: A library for extracting data from HTML and XML using XPath and CSS selectors. In the context of the script, parsel is used to parse the HTML content of web pages fetched by httpx to extract relevant information such as repository links, owners, and programming language statistics.  
4. `pytest`: A framework that makes it easy to write simple tests, yet scales to support complex functional testing. It is used for writing unit tests for the script, ensuring that each component functions correctly.  
5. `coverage`: A tool for measuring code coverage of Python programs. It monitors the script to see which parts are executed and which are not, helping to identify parts of the code that are not covered by unit tests.  

These packages together provide a robust environment for developing an efficient, asynchronous web scraping application, capable of handling multiple concurrent HTTP requests, parsing the returned HTML content, and ensuring the reliability and maintainability of the code through testing.  

### How to use it

1. Clone the repository
2. Install the requirements
3. Run the script

```shell
# setup
git clone https://github.com/romblox/n-ix-technical-task.git
cd n-ix-technical-task
pip install -r requirements.txt

# run the script
python main.py

# or using Makefile
make run
```

### Output
```shell
[
    {
        "url": "https://github.com/openstack/openstack",
        "extra": {
            "owner": "openstack",
            "language_stats": {
                "Python": 100.0
            }
        }
    },
    {
        "url": "https://github.com/JiYou/openstack",
        "extra": {
            "owner": "JiYou",
            "language_stats": {
                "Python": 92.9,
                "JavaScript": 2.5,
                "Smarty": 1.3,
                "Shell": 1.3,
                "HTML": 0.8,
                "CSS": 0.7
            }
        }
    },
    {
        "url": "https://github.com/ContainX/openstack4j",
        "extra": {
            "owner": "ContainX",
            "language_stats": {
                "Java": 97.0,
                "Groovy": 3.0
            }
        }
    },
    {
        "url": "https://github.com/openstack/openstack-ansible",
        "extra": {
            "owner": "openstack",
            "language_stats": {
                "Python": 61.5,
                "Shell": 26.7,
                "Jinja": 11.7,
                "Smarty": 0.1
            }
        }
    },
    
    ....
    ....
    ....
    ....
    
    {
        "url": "https://github.com/gustavoguanabara/html-css",
        "extra": {
            "owner": "gustavoguanabara",
            "language_stats": {
                "HTML": 98.4,
                "CSS": 1.6
            }
        }
    },
    {
        "url": "https://github.com/AllThingsSmitty/css-protips",
        "extra": {
            "owner": "AllThingsSmitty",
            "language_stats": {}
        }
    }
]

```

### Without Proxies
```shell
proxy: None url: https://github.com/search?q=openstack&type=Repositories
proxy: None url: https://github.com/openstack/openstack
proxy: None url: https://github.com/JiYou/openstack
proxy: None url: https://github.com/ContainX/openstack4j
proxy: None url: https://github.com/openstack/openstack-ansible
proxy: None url: https://github.com/php-opencloud/openstack
proxy: None url: https://github.com/kubernetes/cloud-provider-openstack
proxy: None url: https://github.com/terraform-provider-openstack/terraform-provider-openstack
proxy: None url: https://github.com/openstack/openstack-manuals
proxy: None url: https://github.com/openstack/openstack-helm
proxy: None url: https://github.com/openstack/openstacksdk
[
    {
        "url": "https://github.com/openstack/openstack",
        "extra": {
            "owner": "openstack",
            "language_stats": {
                "Python": 100.0
            }
        }
    },
    {
        "url": "https://github.com/JiYou/openstack",
        "extra": {
            "owner": "JiYou",
            "language_stats": {
                "Python": 92.9,
                "JavaScript": 2.5,
                "Smarty": 1.3,
                "Shell": 1.3,
                "HTML": 0.8,
                "CSS": 0.7
            }
        }
    },
    ....
    ....
    ....
```

### With Proxies rotation
```shell
proxy: {'http://': 'http://35.185.196.38:3128', 'https://': 'http://35.185.196.38:3128'} url: https://github.com/search?q=openstack&type=Repositories
proxy: {'http://': 'http://35.185.196.38:3128', 'https://': 'http://35.185.196.38:3128'} url: https://github.com/openstack/openstack
proxy: {'http://': 'http://155.94.241.133:3128', 'https://': 'http://155.94.241.133:3128'} url: https://github.com/JiYou/openstack
proxy: {'http://': 'http://134.209.29.120:3128', 'https://': 'http://134.209.29.120:3128'} url: https://github.com/ContainX/openstack4j
proxy: {'http://': 'http://50.174.145.15:80', 'https://': 'http://50.174.145.15:80'} url: https://github.com/openstack/openstack-ansible
proxy: {'http://': 'http://155.94.241.133:3128', 'https://': 'http://155.94.241.133:3128'} url: https://github.com/php-opencloud/openstack
proxy: {'http://': 'http://134.209.29.120:3128', 'https://': 'http://134.209.29.120:3128'} url: https://github.com/kubernetes/cloud-provider-openstack
proxy: {'http://': 'http://198.44.255.3:80', 'https://': 'http://198.44.255.3:80'} url: https://github.com/terraform-provider-openstack/terraform-provider-openstack
proxy: {'http://': 'http://50.174.145.15:80', 'https://': 'http://50.174.145.15:80'} url: https://github.com/openstack/openstack-manuals
proxy: {'http://': 'http://35.185.196.38:3128', 'https://': 'http://35.185.196.38:3128'} url: https://github.com/openstack/openstack-helm
proxy: {'http://': 'http://198.44.255.3:80', 'https://': 'http://198.44.255.3:80'} url: https://github.com/openstack/openstacksdk
[
    {
        "url": "https://github.com/openstack/openstack",
        "extra": {
            "owner": "openstack",
            "language_stats": {
                "Python": 100.0
            }
        }
    },
    {
        "url": "https://github.com/JiYou/openstack",
        "extra": {
            "owner": "JiYou",
            "language_stats": {
                "Python": 92.9,
                "JavaScript": 2.5,
                "Smarty": 1.3,
                "Shell": 1.3,
                "HTML": 0.8,
                "CSS": 0.7
            }
        }
    },
    ....
    ....
    ....
```

### Unit Testing
```shell
pytest -v tests/

# or using Makefile
make test
```

### Output
```shell
========================================================================== test session starts ===================================================
platform linux -- Python 3.11.5, pytest-8.2.2, pluggy-1.5.0 -- /home/******/python/versions/3.11.5/envs/technical-task/bin/python
rootdir: /home/***********/projects/technical_task
plugins: asyncio-0.23.7, anyio-4.4.0
asyncio: mode=Mode.STRICT
collected 10 items                                                                                                                                                        

tests/test_main.py::test_get_headers PASSED                                                                                                  [ 10%]
tests/test_main.py::test_get_page_html PASSED                                                                                                [ 20%]
tests/test_main.py::test_parse_search_page PASSED                                                                                            [ 30%]
tests/test_main.py::test_parse_languages PASSED                                                                                              [ 40%]
tests/test_main.py::test_parse_search_details PASSED                                                                                         [ 50%]
tests/test_main.py::test_collect_data PASSED                                                                                                 [ 60%]
tests/test_main.py::test_get_search_results PASSED                                                                                           [ 70%]
tests/test_main.py::test_select_proxy PASSED                                                                                                 [ 80%]
tests/test_main.py::test_select_proxy_without_proxy_list_passed PASSED                                                                       [ 90%]
tests/test_main.py::test_select_proxy_on_random PASSED                                                                                       [100%]

===================================================================================================== 10 passed in 0.27s ==========================
```

### Coverage

```bash
coverage run -m pytest -v tests/
coverage report -m

# or using Makefile
make coverage
```

### Output
```shell
========================================================================== test session starts ====================================================
platform linux -- Python 3.11.5, pytest-8.2.2, pluggy-1.5.0 -- /home/******/python/versions/3.11.5/envs/technical-task/bin/python

rootdir: /home/***********/projects/technical_task
plugins: asyncio-0.23.7, anyio-4.4.0
asyncio: mode=Mode.STRICT
collected 10 items                                                                                                                                                        

tests/test_main.py::test_get_headers PASSED                                                                                                  [ 10%]
tests/test_main.py::test_get_page_html PASSED                                                                                                [ 20%]
tests/test_main.py::test_parse_search_page PASSED                                                                                            [ 30%]
tests/test_main.py::test_parse_languages PASSED                                                                                              [ 40%]
tests/test_main.py::test_parse_search_details PASSED                                                                                         [ 50%]
tests/test_main.py::test_collect_data PASSED                                                                                                 [ 60%]
tests/test_main.py::test_get_search_results PASSED                                                                                           [ 70%]
tests/test_main.py::test_select_proxy PASSED                                                                                                 [ 80%]
tests/test_main.py::test_select_proxy_without_proxy_list_passed PASSED                                                                       [ 90%]
tests/test_main.py::test_select_proxy_on_random PASSED                                                                                       [100%]

===================================================================================================== 10 passed in 0.27s ==========================
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
main.py                        70      0   100%
schema.py                      14      0   100%
tests/__init__.py               0      0   100%
tests/conftest.py              18      0   100%
tests/html/__init__.py          0      0   100%
tests/html/detail_page.py       1      0   100%
tests/html/search_page.py       1      0   100%
tests/test_main.py             87      0   100%
---------------------------------------------------------
TOTAL                         191      0   100%
```
