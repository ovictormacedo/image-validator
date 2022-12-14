import json
from flask import Flask, request, Response, Blueprint
from custom_validators import image_validator_controller_input_validator
from utilities import redis_utility
from utilities import celery_utility, client_notification_utility
import logging
import uuid
from settings import REDIS_EXPIRATION_TIME
from utilities.message_states import QUEUED, FAILED

app = Blueprint("publisher", __name__)
flask_app = Flask(__name__)

celery_utilility = celery_utility.make_celery(flask_app)
redis_utilility = redis_utility.make_redis()
logger = logging.getLogger(__name__)

'''
This method is only responsible for validating the urls and input schema, the image validation
is made later async.
'''
@app.route("/api/image/validate", methods=["POST"])
def validate_image():
    logger.info("Request received")
    input_payload = request.json

    # Validates input
    validation_response = image_validator_controller_input_validator.validate(input_payload)
    if not validation_response.is_valid:
        logger.warning(validation_response.object)
        return Response(json.dumps(validation_response.object), status=400)

    input_payload["id"] = str(uuid.uuid4())

    ''''
    Image validation is done later asynchronously because we want the API to not consume so much memory,
    the heavy work can be done by async workers.
    '''
    try:
        # Notifies client about the start
        client_notification_utility.notify_start(input_payload["notifications"]["onSuccess"], input_payload["id"])

        # Post message to Redis.
        celery_utilility.send_task("tasks.image_validator_task.validate_image",
            kwargs={"message": input_payload})

        redis_utilility.set(input_payload["id"], QUEUED)

        logger.info("Request posted to the queue")
    except Exception as ex:
        logger.error(ex)
        redis_utilility.set(input_payload["id"], FAILED, ex=REDIS_EXPIRATION_TIME)
        client_notification_utility.notify_failure(input_payload["notifications"]["onFailure"], input_payload["id"], ["Internal Server Error"])
        return Response("Internal Server Error", status=500)

    logger.info(input_payload)
    return Response("Success", status=200)