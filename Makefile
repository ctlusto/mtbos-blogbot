.PHONY: publish
publish:
	. env/bin/activate && \
	python scripts/blogbot.py

.PHONY: migrate
migrate:
	. env/bin/activate && \
	scripts/migrate.py

.PHONY: env
env:
	virtualenv env && \
	. env/bin/activate && \
	make deps

.PHONY: deps
deps:
	pip install -r requirements.txt
	