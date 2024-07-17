import asyncio

from src.main import get_search_results
from src.schema import SearchSchema

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
            "http://35.185.196.38:3128",
            "http://76.185.196.38:3128",
            "http://134.185.196.38:3128",
            "http://35.185.196.38:3128",
            "http://76.185.196.38:954",
            "http://5.185.196.38:44",
            "http://1.185.196.38:8080"
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
