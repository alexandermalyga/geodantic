sources = geodantic tests

.PHONY: test lint check

test:
	pytest -vv --cov=geodantic tests

lint:
	isort $(sources)
	black $(sources)

check:
	isort --check --diff $(sources)
	black --check --diff $(sources)
	mypy -p geodantic
