from flask import Flask,request
import requests
import json
from urlparse import urlparse,parse_qs
import urllib
from requests_oauthlib import OAuth1
import webbrowser

app = Flask(__name__)

apiKey = "ENTER API KEY"
apiSecret = "ENTER API SECRET"

requestTokenUrl = "https://api.twitter.com/oauth/request_token"
tweetsUrl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
accessTokenUrl = "https://api.twitter.com/oauth/access_token"

OAuthSecret = ""

def deleteTweetsFromIdList(textInTweet,tweetIdList,oauth):
	count = 0
	try:
		for tweetId in tweetIdList:
			print "Deleting tweet with ID : " + str(tweetId)
			deleteUrl = "https://api.twitter.com/1.1/statuses/destroy/" + str(tweetId) + ".json"
			params = {'id': tweetId}
			deleteResponse = requests.post(url=deleteUrl , params=params, auth=oauth)
			print "Deleted Tweet : " + str(textInTweet[count])
			count = count + 1
	except:
		"Exception in traversing tweets"

	return count

@app.route('/')
def data():
	try:
		deletions = 0
		OAuthToken = request.args.get('oauth_token')
		OAuthVerifier = request.args.get('oauth_verifier')
		oauth = OAuth1(apiKey,
                   resource_owner_key = OAuthToken,
                   resource_owner_secret = OAuthSecret,
                   verifier = OAuthVerifier)

		response = requests.post(url=accessTokenUrl, auth=oauth)

		token = str(parse_qs(urlparse('?'+str(response.content)).query)['oauth_token'])
		secret = str(parse_qs(urlparse('?'+str(response.content)).query)['oauth_token_secret'])
		userId = str(parse_qs(urlparse('?'+str(response.content)).query)['user_id'])
		name = str(parse_qs(urlparse('?'+str(response.content)).query)['screen_name'])


		while True:

		  	oauth = OAuth1(apiKey,
					client_secret = apiSecret,
                   resource_owner_key = token[2:-2],
                   resource_owner_secret = secret[2:-2]
                   )
		  	response = requests.get(url=tweetsUrl,auth=oauth)

			jsonTweets = json.dumps(response.text)

		  	twitterJsonResponse = json.loads(response.text)
		  	#print json.dumps({"tweets":twitterJsonResponse})

			for x in range(3):
		  		print ""

			tweetIdList = []
			textInTweet = []

			if not twitterJsonResponse:
				break

		 	for tweets in twitterJsonResponse:
				tweetIdList.append(str(tweets['id']))
				try:
					tweet =  str(tweets['text'])
					textInTweet.append(tweet)
				except:
					textInTweet.append("Some Tweet")

			numberOfTweetsDeleted = deleteTweetsFromIdList(textInTweet,tweetIdList,oauth)

			deletions = deletions + numberOfTweetsDeleted

		return json.dumps({"response":"true","Deleted tweets":deletions})

	except:
		return json.dumps({"response":"false","message":"something went wrong"})

@app.route('/twitter')
def make():

	oauth = OAuth1(apiKey,
					client_secret = apiSecret
                   )

	response = requests.post(url=requestTokenUrl, auth=oauth)

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

	return json.dumps({"response":"true","message":"Please Authorize the TwitterRefresh App to Proceed Further"})

if __name__ == '__main__':
	app.run(debug=True,threaded=True)
