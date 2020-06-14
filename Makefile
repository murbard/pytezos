.PHONY: docs

debug:
	pip install . --force --no-deps

test:
	pytest -v .

docs:
	cd docs && $(MAKE) html

release:
	VERSION=$$(cat pyproject.toml | grep version | awk -F\" '{ print $$2 }')
	git tag $$VERSION && git push origin $$VERSION