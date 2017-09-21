NAME=tdidf_similarity

build:
	docker build -t $(NAME) .

sh:
	docker run -p 8000:8000 -it --rm=true $(NAME) bash

start:
	docker run -p 8000:8000 -i --rm=true $(NAME)

remove:
	-docker stop $(NAME)
	-docker rm $(NAME

venv:
	virtualenv venv
	. venv/bin/activate & pip install -r requirements.txt

.PHONY: test
test:
	. venv/bin/activate & nosetests -v test/*
