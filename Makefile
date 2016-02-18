lint:
	@tox -e py27-lint,py34-lint

clean:
	@-find src -name __pycache__ -exec rm -rf {} \;
	@-find src -name *.pyc -exec rm {} \;
	@-find tests -name __pycache__ -exec rm -rf {} \;
	@-find tests -name *.pyc -exec rm {} \;

install:
	pip install -U .
