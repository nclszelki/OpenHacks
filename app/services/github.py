# import requests, json
# from oauthlib.oauth2 import WebApplicationClient
# from flask import request

# GOOGLE_DISCOVERY_URL = (
#     "https://accounts.google.com/.well-known/openid-configuration"
# )

# def get_google_provider_cfg():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()


# class GitHub():

#     def __init__(self, client_id = '', client_secret = '', access_token = ''):
#         self.client_id = client_id
#         self.client_secret = client_secret
#         self.access_token = access_token
#         self.client = WebApplicationClient(self.client_id)


#     def authorization_url(self):
#         google_provider_cfg = get_google_provider_cfg()
#         authorization_endpoint = google_provider_cfg["authorization_endpoint"]
#         request_uri = self.client.prepare_request_uri(
#             authorization_endpoint,
#             redirect_uri=request.base_url + "/callback",
#             scope=["openid", "email", "profile"],
#         )
#         return request_uri

#     def get_token(self, code):
#         # """Fetch GitHub Access Token for GitHub OAuth."""
#         # headers = { 'Accept': 'application/json' }
#         # params = {
#         #     'code': code, 
#         #     'client_id': self.client_id,
#         #     'client_secret': self.client_secret,
#         # }

#         # data = requests.post(token_url, params=params, headers=headers).json()

#         google_provider_cfg = get_google_provider_cfg()
#         token_endpoint = google_provider_cfg["token_endpoint"]
#         token_url, headers, body = client.prepare_token_request(
#             token_endpoint,
#             authorization_response=request.url,
#             redirect_url=request.base_url,
#             code=code
#         )
#         token_response = requests.post(
#             token_url,
#             headers=headers,
#             data=body,
#             auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#         )

#         client.parse_request_body_response(json.dumps(token_response.json()))

#         return token_response.get('access_token', None)

#     def get(self, route_url, params = {}):
#         url = api_url + route_url
#         params['access_token'] = self.access_token

#         return requests.get(url, params=params).json()

#     def post(self, route_url, params = {}):
#         url = api_url + route_url
#         params['access_token']  = self.access_token

#         return requests.post(url, params=params).json()

#     def delete(self, route_url, params = {}):
#         url = api_url + route_url
#         params['access_token']  = self.access_token

#         return requests.delete(url, params=params)

#     @staticmethod
#     def get_user_from_token(access_token):
#         """Fetch user data using the access token."""
#         url = api_url + '/user'
#         params = { 'access_token': access_token }

#         return requests.get(url, params=params).json()
