from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import pandas as pd
from flask import Flask, redirect, request, session, render_template, url_for

import requests,json

app = Flask(__name__)

# Instantiate AuthClient
auth_client = AuthClient(
        client_id='AB8eoM4RipQmkEEZTClIJEh7A4j3PugxP118fbqSObWHfsX9OX',
        client_secret='OHP9jGFhyJz9cuXN8VhGMGxS0yJmoIteEAN9MZJm',
        access_token='ACCESS_TOKEN',  # If you do not pass this in, the Quickbooks client will call refresh and get a new access token.
        environment='sandbox',
        redirect_uri='http://localhost:5000/callback',
    )
# Prepare Scopes
scopes = [
    Scopes.ACCOUNTING,
]

# Get Authorization URL
auth_url = auth_client.get_authorization_url(scopes)

# Defining the home page of our site
@app.route("/", methods=['GET'])  # this sets the route to this page
def home():
	return redirect(auth_url)

@app.route('/getdata')
def getdata():
    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    url = "{0}/v3/company/{1}/reports/ItemSales?start_date=2015-08-01&end_date=2015-09-30".format(base_url, auth_client.realm_id)
    auth_header = 'Bearer {0}'.format(auth_client.access_token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)

    print("Response = ",response)
    print("Response Data = ",response.text)

    print("Success")
    df = pd.read_json(response.text)
    html = df.to_html()

    return html

@app.route('/callback', methods=['GET'])
def callback():
    #User is redirectred back after doing get request with auth URL
    #with this well recieve the auth code and realmid
    #since the previous function could not give the required stuff we need to handle exception
    state_from_request = request.args.get('state')
    auth_code = request.args.get('code')
    realmid = request.args.get('realmId')
    auth_client.get_bearer_token(auth_code, realm_id = realmid)
    return redirect(url_for('getdata'))



if __name__ == "__main__":
    app.run()
