# _____ Testing using Makefile _____
make test-e2e
make test
make server

# _____ Manually testing the system _____
# Start the application through docker compose
docker-compose up -d --build

# Access Flower to see metrics about the tasks
http://localhost:5556/

# Running tests
pytest tests/controllers/* -s
pytest tests/tasks/* -s
pytest tests/crawlers/* -s
pytest tests/custom_validators/* -s

# Running E2E tests
First start the application user the aforementioned docker compose command.
pytest tests/E2E/* -s

# Application logs
application.log