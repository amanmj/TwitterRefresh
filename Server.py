from flask import Flask,request
import requests
import json
from urlparse import urlparse,parse_qs
import urllib
from requests_oauthlib import OAuth1

app = Flask(__name__)
apiKey = "P9HvIxlPA2luSxEzdq0g5iznR"
apiSecret = "nUZ8NkT0Lxf08whUCm30O87yeYHQzEA3VQcioLrF4VJg89mziK"

OAuthSecret = ""


def makeRequest(OAuthToken,OAuthVerifier):
	url = "https://api.twitter.com/oauth/access_token"

	oauth = OAuth1(apiKey,
                   client_secret=apiSecret,
                   resource_owner_key=OAuthToken,
                   resource_owner_secret=OAuthSecret,
                   verifier=OAuthVerifier)

	response = requests.post(url=url, auth=oauth)
	
	print(response.content)

@app.route('/')
def data():
	try:
	    OAuthToken = request.args.get('oauth_token')
	    OAuthVerifier = request.args.get('oauth_verifier')
	    makeRequest(OAuthToken,OAuthVerifier)
	    return json.dumps({"oauthtoken":OAuthToken,"oauthverifier":OAuthVerifier})    

	except:
		return json.dumps({"response":"false"})

@app.route('/test')
def make():
	url = "https://api.twitter.com/oauth/request_token"

	headers = {
    	'authorization': "OAuth oauth_consumer_key=\"P9HvIxlPA2luSxEzdq0g5iznR\",oauth_signature_method=\"HMAC-SHA1\",oauth_timestamp=\"1500130533\",oauth_nonce=\"bpvFNDzBbJ3\",oauth_version=\"1.0\",oauth_signature=\"NuR91jXE%2BCzxHAPVoTcsIj8F8xw%3D\"",
    }

	response = requests.request("POST", url, headers=headers, params=None)

	OAuthSecret =  str(parse_qs(urlparse('?'+str(response.text)).query)['oauth_token_secret'])
	OAuthToken = str(parse_qs(urlparse('?'+str(response.text)).query)['oauth_token'])
	OAuthSecret = OAuthSecret[2:-2]
	OAuthToken = OAuthToken[2:-2]
	return json.dumps({"oauthtoken":OAuthToken,"oauthsecret":OAuthSecret}) 


if __name__ == '__main__':
	app.run(debug=True,threaded=True)