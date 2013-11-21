from django.http import HttpResponse
import tweepy
import twitter_auth
from tweepy.parsers import Parser

class RawJsonParser(Parser):
    def parse(self, method, payload):
        return payload

def get_recent_tweets(request, count=20):
    auth = tweepy.OAuthHandler(twitter_auth.token, twitter_auth.secret)

    api = tweepy.API(auth_handler=auth, parser=RawJsonParser())
    recent_tweets = api.user_timeline('eje211', count=count)

    return HttpResponse(recent_tweets, mimetype="application/json")
