# Testing using Makefile
```
make test-e2e
make test
make server
```
# API
The application is running on the port 3001 by default, but you can change that on the .env file.
```
Image validation - POST: http://localhost:3001/api/image/validate
{
    "assetPath": { 
        "location": "local",
        "path": "./files/valid-image.jpg"
    },
    "notifications": {
        "onStart": "<any-valid-url>",
        "onSuccess": "<any-valid-url>",
        "onFailure": "<any-valid-url>"
    }
}
```
```
Get processing status on the queue - GET localhost:3001/api/assets?id=<asset-id>
```
# Architecture
![alt text](https://github.com/ovictormacedo/image-validator/blob/master/architecture.png?raw=true)

# Manually testing the system
#### Start the application through docker compose
```
docker-compose up -d --build --env-file .env
```
#### Access Flower to see metrics about the tasks
```
http://localhost:5556/
```
#### Running tests
```
pytest tests/controllers/* -s
pytest tests/tasks/* -s
pytest tests/crawlers/* -s
pytest tests/custom_validators/* -s
```
#### Running E2E tests
First start the application user the aforementioned docker compose command.
```
pytest tests/E2E/* -s
```

# Application logs
```
application.log
```

# Future work
* Lint and coding style. Keep imports on the same standards, and follow recommendations from the peps. Having a git hook and a lint running on the pipeline would be good.
* Use NGINX to setup DNSes and serve the API using SSL certificates (prevent CORS).
* Authentication and authorization layers could be added to this application, or it could be a separate service called in an API gateway before the call to this API. The auth method can be API Key or Oauth 2, API Key is probably a better option to integrate two back end services, since it's simpler to manage the secret and this is not exposed to the public. In terms of authorization, the user should have permissions to: validate the specific asset which he informed on the payload, and to track the status of his requests.
* In terms of infrastructure, there is also some work to do in terms of routing and distribution, machines receiving requests should be dedicated to that, Redis should be in a separated cluster, the workers in another cluster, and finally the images should be stored in another cluster.
* Having a DDoS protection service in front of the APIs would also be great if that is exposed to the internet.
* CI/CD.
* The system already has non structured logs, but having structured logs would also be good to leverage better tools like Elastic Search (ELK stack). The key metrics for this service are: E2E latency, latency for each component (API, async Task), heart beat, ram memory consumption, expected errors, exceptions, warnings, health check based on volume, system reliability and availability. For all these metrics alerts should be setup based on certain thresholds, the thresholds could the SLAs (e.g. alert if reliability drops below 99.99% etc).
* Using K8S might be a good idea.
* More tests =)