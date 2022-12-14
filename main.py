import logging
from flask import Flask
from controllers import image_validator_controller, image_processing_status_controller
from tasks import image_validator_task

main_app = Flask(__name__)

logging.basicConfig(filename="application.log", level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

main_app.register_blueprint(image_validator_controller.app)
main_app.register_blueprint(image_validator_task.app)
main_app.register_blueprint(image_processing_status_controller.app)
