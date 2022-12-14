import requests
import logging

logger = logging.getLogger(__name__)

def notify_start(url, id):
    response = requests.post(url, json={"id": id, "state": "started"})
    logger.info({f"Notifying start to client {url} about asset {id} - {response.status_code}"})
    return response

def notify_success(url, id):
    response = requests.post(url, json={"id": id, "state": "success"})
    logger.info({f"Notifying success to client {url} about asset {id} - {response.status_code}"})
    return response

def notify_failure(url, id, errors):
    response = requests.post(url, json={"id": id, "state": "failed", "errors": errors})
    logger.info({f"Notifying failure to client {url} about asset {id} - {errors} - {response.status_code}"})
    return response