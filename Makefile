.PHONY: docs

debug:
	pip install . --force --no-deps

test:
	pytest -v .

docs:
	cd docs && $(MAKE) html

release:
	PYTEZOS_VERSION=$$(cat pyproject.toml | grep version | awk -F\" '{ print $$2 }')
	git tag $$PYTEZOS_VERSION && git push origin $$PYTEZOS_VERSION