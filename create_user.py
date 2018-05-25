import requests, json, logging, time, urllib
import pandas as pd
from io import StringIO
import io as stringIOModule
from datetime import datetime

# Set up logging to catch errors, etc...
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(str(time.strftime("%d_%m_%Y")) +"_looker_API_Calls" + ".log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('Testing Logs')

class LookerAPI(object):
    """Class that contains methods and variables related to looker API authentication"""
    def __init__(self, api_info):
        self.api_endpoint = api_info['api_endpoint']
        self.client_secret = api_info['client_secret']
        self.client_id = api_info['client_id']
        self.login_endpoint = api_info['login_url']
        print(self.login_endpoint)

    def login(self):
        "login to looker API"
        try:
            auth_data = {'client_id':self.client_id, 'client_secret':self.client_secret}
            r = requests.post( self.login_endpoint,data=auth_data) # error handle here
            json_auth = json.loads(r.text)['access_token']
            return json_auth
        except requests.exceptions.RequestException as e:
            logger.error(e)


    def user_exists(self, email_address):
        try:
            request_url = self.api_endpoint + '/users/search?email={0}'.format(email_address)
            r = requests.get(request_url, headers={'Authorization': "token " + json_auth})
            user_exists = json.loads(r.text)
            return True if user_exists else False
        except requests.exceptions.RequestException as e:
            logger.error(e)

    def create_new_user(self, first_name, last_name, email):
        if not self.user_exists(email):
            try:
                """Create the user """
                user = json.dumps({"first_name": first_name, "last_name": last_name})
                request_url = self.api_endpoint + '/users'
                r = requests.post(request_url, headers={'Authorization': "token " + json_auth}, data=user)

                """Get the user ID and add an email address """
                user_id = json.loads(r.text)['id']
                user_email = json.dumps({"email": email})
                request_url = self.api_endpoint + '/users/{0}/credentials_email'.format(user_id)
                r = requests.post(request_url, headers={'Authorization': "token " + json_auth}, data=user_email)

                """Get the reset password URL to provide to the user """
                request_url = self.api_endpoint + '/users/{0}/credentials_email/password_reset'.format(user_id)
                r = requests.post(request_url, headers={'Authorization': "token " + json_auth}, data=user_email)
                reset_url = json.loads(r.text)["password_reset_url"]

                return "User {0} created with email address {1}. Password can be set at {2}".format(user_id, email, reset_url)

            except requests.exceptions.RequestException as e:
                logger.error(e)
        else:
            return "User {0} already exists".format(email)

creds = {
    'api_endpoint' : 'https://x.looker.com:19999/api/3.0',
    'login_url': 'https://x.looker.com:19999/login',
    'client_id' : 'x',
    'client_secret': 'x'
}

looker = LookerAPI(creds)
json_auth = looker.login()
print('Token: ' + json_auth)

first_name = 'Brecht'
last_name = 'Sup'
email = 'brechto2@looker.com'

looker.create_new_user(first_name, last_name, email)
