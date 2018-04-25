from requests import get
from settings import fetch_submission_url

def fetch_waiting_submission():
    try:
        response = get( fetch_submission_url )
        if response['status'] == False:
            return None
    except:
        return None
    return response.json()