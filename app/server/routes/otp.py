import asyncio
from fastapi import APIRouter, Form, status
from fastapi.responses import FileResponse, RedirectResponse
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import config
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

load_dotenv()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
verify_sid = os.environ['TWILIO_VERIFY_ID']
verified_number = "+919538677729"

api_key = os.environ['TWILIO_API_KEY']
api_secret = os.environ['TWILIO_API_KEY_SECRET']
service_id = os.environ['TWILIO_SERVICE_SID']

# required for Chat grants
service_sid = service_id
identity = 'tanujohari.tj@gmail.com'

router = APIRouter()

settings = config.Settings()

def get_twilio_auth_token():
    # Your logic to retrieve a new Twilio Auth Token (e.g., from a rotating token service)
    # For demonstration purposes, I'm returning the static token defined above
    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create an Chat grant and add to token
    chat_grant = ChatGrant(service_sid=service_sid)
    token.add_grant(chat_grant)
    return token.to_jwt()

def get_twilio_client():
    # Calculate token expiration time (typically, Twilio tokens expire after 24 hours)
    expiration_time = datetime.utcnow() + timedelta(hours=24)

    # Initialize Twilio HTTP client with rotating token
    http_client = TwilioHttpClient()
    http_client.session.headers["Authorization"] = f"Bearer {get_twilio_auth_token()}"

    # Initialize Twilio client with custom HTTP client
    client = Client(account_sid, auth_token, http_client=http_client)
    return client

@router.post("/")
def send_otp():
    client = get_twilio_client()
    verification = client.verify.v2.services(verify_sid).verifications.create(to=verified_number, channel="sms")
    return verification.status

@router.get("/")
def check_otp(otp_code):
    client = get_twilio_client()
    verification = client.verify.v2.services(verify_sid).verification_checks.create(to=verified_number, code=otp_code)
    return verification.status