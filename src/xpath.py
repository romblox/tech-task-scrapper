SEARCH_RESULTS = '//div[@data-testid="results-list"]//h3//div[contains(@class, "search-title")]/a/@href'
OWNER = 'normalize-space(//a[@rel="author"]/text())'
LANGUAGES = "//div[contains(./h2, 'Language')]/ul//a"
LANGUAGE_TITLE = "./span[@class]/text()"
LANGUAGE_PERCENT = "./span[@class]/following-sibling::span/text()"
