run:
	python main.py

test:
	pytest -v tests/

coverage:
	coverage run -m pytest -v tests/ && coverage report -m
