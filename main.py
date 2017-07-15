import base64
import requests
from requests_oauthlib import OAuth1


apiKey = "P9HvIxlPA2luSxEzdq0g5iznR"
apiSecret = "nUZ8NkT0Lxf08whUCm30O87yeYHQzEA3VQcioLrF4VJg89mziK"

bearerToken = apiKey + ':' + apiSecret

encoded = base64.b64encode(bearerToken)

url = "https://api.twitter.com/oauth/request_token"

headers = {
    'authorization': "OAuth oauth_consumer_key=\"P9HvIxlPA2luSxEzdq0g5iznR\",oauth_signature_method=\"HMAC-SHA1\",oauth_timestamp=\"1500130533\",oauth_nonce=\"bpvFNDzBbJ3\",oauth_version=\"1.0\",oauth_signature=\"NuR91jXE%2BCzxHAPVoTcsIj8F8xw%3D\"",
    }

response = requests.request("POST", url, headers=headers, params=None)

print(response.text)
