test:
	. venv/bin/activate
	pip3 install -r requirements.txt
	pytest tests/controllers/* -s
	pytest tests/tasks/* -s
	pytest tests/crawlers/* -s
	pytest tests/custom_validators/* -s

test-e2e:
	docker-compose down
	docker-compose up -d --build --force-recreate
	pytest tests/E2E/validate_system_test.py -s
server:
	docker-compose up -d --build