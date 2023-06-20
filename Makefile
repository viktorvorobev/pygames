init-env:
	cd src && poetry install

type-check:
	cd src && poetry run mypy pygames

lint:
	cd src && poetry run pylint pygames tests --load-plugins pylint_quotes

style-check:
	cd src && poetry run flake8 pygames tests

test:
	cd src && poetry run pytest tests --cov=pygames --cov-report=html

coverage:
	cd src && poetry run coverage report --fail-under=80
