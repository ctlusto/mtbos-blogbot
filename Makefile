.PHONY: env
env:
	virtualenv env && \
	. env/bin/activate && \
	make deps

.PHONY: deps
deps:
	pip install -r requirements.txt
	