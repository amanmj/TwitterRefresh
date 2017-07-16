from flask import Flask,request
import requests
import json
from urlparse import urlparse,parse_qs
import urllib
from requests_oauthlib import OAuth1
import webbrowser

app = Flask(__name__)
apiKey = "P9HvIxlPA2luSxEzdq0g5iznR"
apiSecret = "nUZ8NkT0Lxf08whUCm30O87yeYHQzEA3VQcioLrF4VJg89mziK"

OAuthSecret = ""


def makeRequest(OAuthToken,OAuthVerifier):
	url = "https://api.twitter.com/oauth/access_token"

	oauth = OAuth1(apiKey,
                   resource_owner_key=OAuthToken,
                   resource_owner_secret=OAuthSecret,
                   verifier=OAuthVerifier)

	response = requests.post(url=url, auth=oauth)
	
	print(response.content)

	token = str(parse_qs(urlparse('?'+str(response.content)).query)['oauth_token'])
	secret = str(parse_qs(urlparse('?'+str(response.content)).query)['oauth_token_secret'])
	userId = str(parse_qs(urlparse('?'+str(response.content)).query)['user_id'])
	name = str(parse_qs(urlparse('?'+str(response.content)).query)['screen_name'])

	oauth = OAuth1(apiKey,
                   resource_owner_key=token[2:-2],
                   resource_owner_secret=secret[2:-2]
                   )

	tweetsUrl = "https://api.twitter.com/1.1/statuses/user_timeline.json"

	response = requests.get(url=tweetsUrl,auth=oauth)

	deleteUrl = "https://api.twitter.com/1.1/statuses/destroy/" + str(880429316663779328) + ".json"
	
	params = {'id':880429316663779328}
	deleteResponse = requests.post(url=deleteUrl,params=params, auth=oauth)
	

	print deleteResponse.content

	return json.dumps(response.content)



@app.route('/')
def data():
	try:
	    OAuthToken = request.args.get('oauth_token')
	    OAuthVerifier = request.args.get('oauth_verifier')
	    x = makeRequest(OAuthToken,OAuthVerifier)
	    return x
	    #return json.dumps({"oauthtoken":OAuthToken,"oauthverifier":OAuthVerifier})    

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

	# MacOS
	try:
		chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
		webbrowser.get(chrome_path).open("https://api.twitter.com/oauth/authenticate?oauth_token=" + str(OAuthToken))
	except:
		print "You don't use mac!"

	# Windows
	try:
		chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
		webbrowser.get(chrome_path).open("https://api.twitter.com/oauth/authenticate?oauth_token=" + str(OAuthToken))

	except:
		print "You don't use windows!"
	
	# Linux
	try:
		chrome_path = '/usr/bin/google-chrome %s'
		webbrowser.get(chrome_path).open("https://api.twitter.com/oauth/authenticate?oauth_token=" + str(OAuthToken))
	except:
		print "You don't use linux!"

	return json.dumps({"oauthtoken":OAuthToken,"oauthsecret":OAuthSecret}) 


if __name__ == '__main__':
	app.run(debug=True,threaded=True)