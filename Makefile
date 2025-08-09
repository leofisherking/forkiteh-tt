
check:
	isort src
	ruff check --fix
	ruff format
	mypy --config mypy.ini
