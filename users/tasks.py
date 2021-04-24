import json

from django.contrib.auth import get_user_model
from django.utils import timezone

from celery import shared_task
from celery.utils.log import get_task_logger

from utils.abstract_api import AbstractAPI

logger = get_task_logger(__name__)


@shared_task
def update_user_geolocation(user_email):
    user_model = get_user_model()
    user = user_model.objects.filter(email=user_email).first()
    abstract_api = AbstractAPI()

    if user:
        logger.info(f"Updating user with email ({user.email})")
        geolocation, status_code = abstract_api.ip_geolocation()

        if status_code == 200:
            user.geolocation = json.dumps(geolocation)

            now = timezone.now()
            country = geolocation['country']
            holiday, status_code = abstract_api.holidays(country=country, year=now.year, month=now.month, day=now.day)

            if status_code == 200:
                user.signup_holiday = json.dumps(holiday)

            else:
                logger.info(f"Error getting holiday data: {status_code}")

        else:
            logger.info(f"Error getting geolocation data: {status_code}")

        user.save()
    else:
        logger.info(f"Error getting user with email ({user_email})")
