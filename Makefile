run:
	docker compose up --build

test:
	pytest -q

lint:
	ruff check .
	black --check .
	mypy app
