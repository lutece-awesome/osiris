from requests import get
import settings

def fetch_waiting_submission():
    try:
        response = get( settings.fetch_submission_url )
        if response['status'] == False:
            return None
    except:
        return None
    return response.json()