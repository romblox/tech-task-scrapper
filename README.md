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
python run.py

# or using Makefile
make run
```


### Output without proxy
```shell
proxy: None url: https://github.com/search?q=openstack+OR+nova+OR+css&type=repositories
proxy: None url: https://github.com/openstack/nova
proxy: None url: https://github.com/int32bit/openstack-workflow
proxy: None url: https://github.com/openstack/python-novaclient
proxy: None url: https://github.com/crowbar/barclamp-nova
proxy: None url: https://github.com/openstack/openstack
proxy: None url: https://github.com/crowbar/barclamp-nova_dashboard
proxy: None url: https://github.com/docker-archive/openstack-docker
proxy: None url: https://github.com/ruby-openstack/ruby-openstack
proxy: None url: https://github.com/openstack/puppet-nova
proxy: None url: https://github.com/fog/fog-openstack
[
    {
        "url": "https://github.com/openstack/nova",
        "extra": {
            "owner": "openstack",
            "language_stats": {
                "Python": 97.7,
                "Smarty": 2.2
            }
        }
    },
    {
        "url": "https://github.com/int32bit/openstack-workflow",
        "extra": {
            "owner": "int32bit",
            "language_stats": {
                "Python": 91.7,
                "Shell": 6.2,
                "Makefile": 2.1
            }
        }
    },
    {
        "url": "https://github.com/openstack/python-novaclient",
        "extra": {
            "owner": "openstack",
            "language_stats": {
                "Python": 100.0
            }
        }
    },

    ....
    ....
    ....
    
    {
        "url": "https://github.com/fog/fog-openstack",
        "extra": {
            "owner": "fog",
            "language_stats": {
                "Ruby": 100.0
            }
        }
    }
]
```

### Output with random proxy from the list  
```shell
proxy: {'http://': 'http://5.75.200.249:80', 'https://': 'http://5.75.200.249:80'} url: https://github.com/search?q=openstack+OR+nova+OR+css&type=repositories
proxy: {'http://': 'http://5.75.200.249:80', 'https://': 'http://5.75.200.249:80'} url: https://github.com/openstack/nova
proxy: {'http://': 'http://5.75.200.249:80', 'https://': 'http://5.75.200.249:80'} url: https://github.com/int32bit/openstack-workflow
proxy: {'http://': 'http://5.75.200.249:80', 'https://': 'http://5.75.200.249:80'} url: https://github.com/openstack/python-novaclient
proxy: {'http://': 'http://5.75.200.249:80', 'https://': 'http://5.75.200.249:80'} url: https://github.com/crowbar/barclamp-nova
proxy: {'http://': 'http://5.75.200.249:80', 'https://': 'http://5.75.200.249:80'} url: https://github.com/openstack/openstack
proxy: {'http://': 'http://5.75.200.249:80', 'https://': 'http://5.75.200.249:80'} url: https://github.com/crowbar/barclamp-nova_dashboard
proxy: {'http://': 'http://5.75.200.249:80', 'https://': 'http://5.75.200.249:80'} url: https://github.com/docker-archive/openstack-docker
proxy: {'http://': 'http://5.75.200.249:80', 'https://': 'http://5.75.200.249:80'} url: https://github.com/ruby-openstack/ruby-openstack
proxy: {'http://': 'http://5.75.200.249:80', 'https://': 'http://5.75.200.249:80'} url: https://github.com/openstack/puppet-nova
proxy: {'http://': 'http://5.75.200.249:80', 'https://': 'http://5.75.200.249:80'} url: https://github.com/fog/fog-openstack
[
    {
        "url": "https://github.com/openstack/nova",
        "extra": {
            "owner": "openstack",
            "language_stats": {
                "Python": 97.7,
                "Smarty": 2.2
            }
        }
    },
    {
        "url": "https://github.com/int32bit/openstack-workflow",
        "extra": {
            "owner": "int32bit",
            "language_stats": {
                "Python": 91.7,
                "Shell": 6.2,
                "Makefile": 2.1
            }
        }
    },
    {
        "url": "https://github.com/openstack/python-novaclient",
        "extra": {
            "owner": "openstack",
            "language_stats": {
                "Python": 100.0
            }
        }
    },
    
    ....
    ....
    ....
    ....
    
    {
        "url": "https://github.com/fog/fog-openstack",
        "extra": {
            "owner": "fog",
            "language_stats": {
                "Ruby": 100.0
            }
        }
    }
]

```

### Unit Testing
```shell
pytest -v tests/

# or using Makefile
make test
```

### Output
```shell
========================================================================== test session starts ===========================================================================
platform linux -- Python 3.11.5, pytest-8.2.2, pluggy-1.5.0 -- /home/******/.pyenv/versions/3.11.5/envs/technical-task/bin/python
cachedir: .pytest_cache
rootdir: /home/******/PycharmProjects/nix_pythonProject
plugins: asyncio-0.23.7, anyio-4.4.0
asyncio: mode=Mode.STRICT
collected 12 items                                                                                                                                                       

tests/test_main.py::test_get_headers PASSED                                                                                                                        [  8%]
tests/test_main.py::test_get_page_html PASSED                                                                                                                      [ 16%]
tests/test_main.py::test_parse_search_page PASSED                                                                                                                  [ 25%]
tests/test_main.py::test_parse_languages PASSED                                                                                                                    [ 33%]
tests/test_main.py::test_parse_search_details PASSED                                                                                                               [ 41%]
tests/test_main.py::test_collect_data PASSED                                                                                                                       [ 50%]
tests/test_main.py::test_get_search_results_with_mocked_collect_data PASSED                                                                                        [ 58%]
tests/test_main.py::test_select_proxy PASSED                                                                                                                       [ 66%]
tests/test_main.py::test_select_proxy_without_proxy_list_passed PASSED                                                                                             [ 75%]
tests/test_main.py::test_select_random_proxy PASSED                                                                                                                [ 83%]
tests/test_main.py::test_select_random_proxy_on_empty_list PASSED                                                                                                  [ 91%]
tests/test_schema.py::test_search_schema PASSED                                                                                                                    [100%]

=========================================================================== 12 passed in 0.24s ===========================================================================
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
========================================================================== test session starts ===========================================================================
platform linux -- Python 3.11.5, pytest-8.2.2, pluggy-1.5.0 -- /home/******/.pyenv/versions/3.11.5/envs/technical-task/bin/python
cachedir: .pytest_cache
rootdir: /home/******/PycharmProjects/nix_pythonProject
plugins: asyncio-0.23.7, anyio-4.4.0
asyncio: mode=Mode.STRICT
collected 12 items                                                                                                                                                       

tests/test_main.py::test_get_headers PASSED                                                                                                                        [  8%]
tests/test_main.py::test_get_page_html PASSED                                                                                                                      [ 16%]
tests/test_main.py::test_parse_search_page PASSED                                                                                                                  [ 25%]
tests/test_main.py::test_parse_languages PASSED                                                                                                                    [ 33%]
tests/test_main.py::test_parse_search_details PASSED                                                                                                               [ 41%]
tests/test_main.py::test_collect_data PASSED                                                                                                                       [ 50%]
tests/test_main.py::test_get_search_results_with_mocked_collect_data PASSED                                                                                        [ 58%]
tests/test_main.py::test_select_proxy PASSED                                                                                                                       [ 66%]
tests/test_main.py::test_select_proxy_without_proxy_list_passed PASSED                                                                                             [ 75%]
tests/test_main.py::test_select_random_proxy PASSED                                                                                                                [ 83%]
tests/test_main.py::test_select_random_proxy_on_empty_list PASSED                                                                                                  [ 91%]
tests/test_schema.py::test_search_schema PASSED                                                                                                                    [100%]

=========================================================================== 12 passed in 0.27s ===========================================================================
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
src/__init__.py                 0      0   100%
src/main.py                    65      0   100%
src/schema.py                  16      0   100%
src/settings.py                 3      0   100%
src/xpath.py                    5      0   100%
tests/__init__.py               0      0   100%
tests/conftest.py              21      0   100%
tests/html/__init__.py          0      0   100%
tests/html/detail_page.py       1      0   100%
tests/html/search_page.py       1      0   100%
tests/test_main.py             83      0   100%
tests/test_schema.py            9      0   100%
---------------------------------------------------------
TOTAL                         204      0   100%
```
