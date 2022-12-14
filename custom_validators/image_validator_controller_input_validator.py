from custom_validators.url_validator import is_valid_url
from marshmallow import Schema, fields, ValidationError
from models.responses import ValidationResponse

class AssetPathSchema(Schema):
    location = fields.String(required=True)
    path = fields.String(required=True)

class NotificationsSchema(Schema):
    onStart = fields.String(required=True)
    onSuccess = fields.String(required=True)
    onFailure = fields.String(required=True)

class InputSchema(Schema):
    assetPath = fields.Nested(AssetPathSchema, required=True)
    notifications = fields.Nested(NotificationsSchema, required=True)

def _validate_urls(notifications):
    invalid_urls = []
    if not is_valid_url(notifications["onStart"]):
        invalid_urls.append({"onStart": "URL is invalid"})

    if not is_valid_url(notifications["onSuccess"]):
        invalid_urls.append({"onSuccess": "URL is invalid"})

    if not is_valid_url(notifications["onFailure"]):
        invalid_urls.append({"onFailure": "URL is invalid"})

    return invalid_urls

def validate(request_data):
    schema = InputSchema()
    try:
        # Validate input schema
        response = schema.load(request_data)

        # Validate notification URLs
        urls_validation_response = _validate_urls(response["notifications"])
        if len(urls_validation_response) > 0:
            return ValidationResponse(False, {"errors": urls_validation_response})

        return ValidationResponse(True, response)
    except ValidationError as err:
        return ValidationResponse(False, {"errors": err.messages})