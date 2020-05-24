# -*- coding: utf-8 -*-
import functools, json, requests, os

from flask import flash, redirect, render_template, request
from flask import Blueprint, session, url_for, g
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from oauthlib.oauth2 import WebApplicationClient
from app.models.user import User
from app.settings import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
# from app.services.google import Google

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
# Activation happen in app.py

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()



@blueprint.route('/login')
def googleLogin():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@blueprint.route('/login/callback')
def googleCallback():
    if 'code' not in request.args:
        return '', 500

    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    user = User.find_or_create_from_token(userinfo_response)
    login_user(user)
    session['user_id'] = user.id
    
    return redirect(url_for('home.index'))

@blueprint.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('home.index'))

# @blueprint.before_app_request
# def get_current_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = User.query.filter_by(id=user_id).first()
