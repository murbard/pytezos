.ONESHELL:
.PHONY: docs

debug:
	pip install . --force --no-deps

isort:
	poetry run isort pytezos

pylint:
	poetry run pylint pytezos || poetry run pylint-exit $$?

lint: isort pylint

test:
	pytest -v .

docs:
	cd docs && rm -rf ./build && $(MAKE) html

rpc-docs:
	python -m scripts.fetch_docs

release:
	PYTEZOS_VERSION=$$(cat pyproject.toml | grep version | awk -F\" '{ print $$2 }')
	git tag $$PYTEZOS_VERSION -f && git push origin $$PYTEZOS_VERSION -f