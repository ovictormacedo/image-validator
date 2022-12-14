from flask import Flask, request, Response, Blueprint
from utilities import redis_utility
import logging

app = Blueprint("image_processing_status", __name__)
flask_app = Flask(__name__)

redis_utilility = redis_utility.make_redis()
logger = logging.getLogger(__name__)

'''
This method is only responsible for validating the urls and input schema, the image validation
is made later async.
'''
@app.route("/api/assets", methods=["GET"])
def get_image_processing_status():
    asset_id = request.args.get("id")
    if not asset_id:
        return Response("Please inform an asset id", status=400)

    logger.info(f"Retrieving queue state for: {asset_id}")

    status = None
    try:
        status = redis_utilility.get(str(asset_id))
    except Exception as ex:
        logger.error(str(ex))

    if not status:
        return Response(status=204)

    return Response(status, status=200)