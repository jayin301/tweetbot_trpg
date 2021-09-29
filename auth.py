import logging
import tweepy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from threading import Thread

logger = logging.getLogger()

def google_auth():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds' ,'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('google spread_secret_filename', scope)
    client = gspread.authorize(creds)

    return client

def tweeter_auth():
    consumer_key = "write_your_tweet_consuer_key"
    consumer_secret = "and_secret"
    access_token = "your_access_token"
    access_token_secret = "and_secret"
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    print("API created")
    return api

