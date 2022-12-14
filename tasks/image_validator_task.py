from flask import Flask, Blueprint
from utilities import redis_utility
import logging
from custom_validators import image_validator
from crawlers import image_crawler
from utilities import celery_utility
from utilities.client_notification_utility import notify_success, notify_failure
from settings import REDIS_EXPIRATION_TIME
from utilities.message_states import IN_PROGRESS, FAILED, COMPLETE

app = Blueprint("subscriber", __name__)
flask_app = Flask(__name__)

celery_utility = celery_utility.make_celery(flask_app)
redis_utilility = redis_utility.make_redis()
logger = logging.getLogger(__name__)

@celery_utility.task()
def validate_image(message):
    logger.info(message)

    redis_utilility.set(message["id"], IN_PROGRESS)

    # Retrieves image and validates if the path is correct
    crawler_response = image_crawler.crawl(message["assetPath"])
    if crawler_response.status != "success":
        logger.warning(crawler_response.status)
        redis_utilility.set(message["id"], FAILED, ex=REDIS_EXPIRATION_TIME)
        notify_failure(message["notifications"]["onFailure"], message["id"], [crawler_response.status])
        return False
    
    # Validates image
    validation_response = image_validator.validate(crawler_response.object)
    if not validation_response.is_valid:
        logger.warning(validation_response.object)
        redis_utilility.set(message["id"], FAILED, ex=REDIS_EXPIRATION_TIME)
        notify_failure(message["notifications"]["onFailure"], message["id"], validation_response.object["errors"])
        return False

    redis_utilility.set(message["id"], COMPLETE, ex=REDIS_EXPIRATION_TIME)
    notify_success(message["notifications"]["onSuccess"], message["id"])
    return True
    