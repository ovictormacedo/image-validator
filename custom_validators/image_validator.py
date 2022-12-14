from models.responses import ValidationResponse
from utilities.file_constraints import SUPPORTED_IMAGE_FORMATS, MAX_WIDTH, MAX_HEIGHT

def _is_a_supported_format(image):
    return image.format.lower() in SUPPORTED_IMAGE_FORMATS

def _is_inside_the_size_limit(image):
    return image.height <= MAX_HEIGHT and image.width <= MAX_WIDTH

def validate(image):
    validation_errors = []
    if not _is_a_supported_format(image):
        validation_errors.append({"format": f"Only {SUPPORTED_IMAGE_FORMATS} are formats supported"})
    
    if not _is_inside_the_size_limit(image):
        validation_errors.append({"dimension": f"Height and width must not be greater than {MAX_HEIGHT} and {MAX_WIDTH}"})

    is_valid = len(validation_errors) == 0

    return ValidationResponse(is_valid, {"errors": validation_errors})