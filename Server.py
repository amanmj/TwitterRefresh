from flask import Flask,request
import requests
import json

app = Flask(__name__)

def makeRequest(OAuthVerifier):
	url = "https://api.twitter.com/oauth/access_token"

	querystring = {"oauth_consumer_key":"P9HvIxlPA2luSxEzdq0g5iznR","oauth_signature_method":"HMAC-SHA1","oauth_timestamp":"1500137919","oauth_nonce":"v77DWKVSzKW","oauth_version":"1.0","oauth_signature":"DF/glCYKN9lfdwGUMhQm5GtNgeY="}

	headers = {
    	'oauth_verifier': OAuthVerifier,
    	'authorization': "OAuth oauth_consumer_key=\"P9HvIxlPA2luSxEzdq0g5iznR\",oauth_signature_method=\"HMAC-SHA1\",oauth_timestamp=\"1500138078\",oauth_nonce=\"qTTJTTkGKfa\",oauth_version=\"1.0\",oauth_signature=\"wuW%2BbpQVqozPQaQrecGr8ILipyY%3D\"",
    }
	print OAuthVerifier
	response = requests.request("POST", url, headers=headers, params=None)
	print(response.text)

@app.route('/')
def data():
	try:
	    #print request.args
	    OAuthToken = request.args.get('oauth_token')
	    OAuthVerifier = request.args.get('oauth_verifier')
	    makeRequest(OAuthVerifier)
	    return json.dumps({"oauthtoken":OAuthToken,"oauthverifier":OAuthVerifier})    

	except:
		return json.dumps({"response":"false"})


if __name__ == '__main__':
	app.run(debug=True,threaded=True)