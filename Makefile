build:
	python3 -m build

publish:
	python3 -m twine upload --repository prune-container-repo dist/*
