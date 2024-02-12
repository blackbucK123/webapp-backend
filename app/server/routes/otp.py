import asyncio
from fastapi import APIRouter, Form, status
from fastapi.responses import FileResponse, RedirectResponse
from twilio.rest import Client
import config
import os


account_sid = "AC64ee21fc7500dfda0b5594e7c9620bf9"
auth_token = "154ca65c09d605340ee1386275dbb246"
verify_sid = "VAce69a27f8f40f63df770c0a347d3c8f2"
verified_number = "+916281353466"

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