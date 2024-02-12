import asyncio
from fastapi import APIRouter, Form, status
from fastapi.responses import FileResponse, RedirectResponse
from twilio.rest import Client
import config
import os


account_sid = "AC1a05cec6f078472cf93553d3bf45ca31"
auth_token = "fa9599efbff479b95d8c7a6c0a1ef8c4"
verify_sid = "VAa3b9281dbf9db5125238d24207d54aa1"
verified_number = "+919538677729"

router = APIRouter()

settings = config.Settings()

@router.post("/")
def send_otp():
    client = Client(account_sid, auth_token)
    verification = client.verify.v2.services(verify_sid).verifications.create(to=verified_number, channel="sms")
    return verification.status

@router.get("/")
def check_otp(otp_code):
    client = Client(account_sid, auth_token)
    verification = client.verify.v2.services(verify_sid).verification_checks.create(to=verified_number, code=otp_code)
    return verification.status