import os
from dotenv import load_dotenv

load_dotenv()

REDIS_EXPIRATION_TIME=int(os.getenv("REDIS_EXPIRATION_TIME"))
REDIS_HOST=os.getenv("REDIS_HOST")
REDIS_PORT=os.getenv("REDIS_PORT")
CELERY_URL=os.getenv("CELERY_URL")
APPLICATION_PORT=os.getenv("APPLICATION_PORT")