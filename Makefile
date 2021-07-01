deploy:
	git pull


install_requirements:
	pip install -r ./.requirements/common.txt

install_linters:
	pip install -r ./.requirements/linters.txt
	pre-commit install
	pre-commit install --hook-type commit-msg
	pre-commit autoupdate


migrate:
	cd bot/db/ && alembic upgrade head

makemigrations:
	cd bot/db/ && alembic revision --autogenerate


init_db:
	make install_requirements
	docker-compose up --build db

init_test_db:
	docker-compose up --build test_db

make run_bot:
	docker-compose up -d --build run_bot
