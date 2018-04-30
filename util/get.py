from requests import get
from . import settings

def fetch_waiting_submission():
    try:
        response = get( settings.fetch_submission_url )
    except:
        return None
    response = response.json()
    if response['status'] == False:
        response = None
    return response
