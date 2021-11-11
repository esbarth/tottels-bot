# tottels-bot
https://github.com/esbarth/tottels-bot
import tweepy
import random
import time
import sys
import os
from textgenrnn import textgenrnn

# Simple Twitter bot
# This bot constructs random tweets using a neural network provided by textgenrnn
# It can also tweet every t seconds based on user args

# @author Emily Barth
# @date 11/11/2021
# Check out my github at https://github.com/esbarth
# textgenrnn documentation can be found at https://github.com/esbarth/tottels-bot
# keras documentation can be found at

# API set up

consumer_key = 'QLtH7XGp8pCweIjqu9R76ivxi'
consumer_secret = 'bkKM7WgLWin46udwvk8ZWFGDK9GYP2MhalGcJLUYytgYEvi5kV'
access_token = '1457755087971966980-aJl398na3NWlNkx3rP21vxKY7l0sg5'
access_token_secret = 'Ci0tK1i4rHwyIPALkbyc2i4SphNk9C2KWK6v7ixwzC9WW'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def check_followers():
    followers = []
    for follower in tweepy.Cursor(api.followers).items():
        followers.append(follower)

    print ("Found %s followers, finding friends.." % len(followers))
    friends = []
    for friend in tweepy.Cursor(api.friends).items():
        friends.append(friend)

    # creating dictionaries based on id's is handy too

    friend_dict = {}
    for friend in friends:
        friend_dict[friend.id] = friend

    follower_dict = {}
    for follower in followers:
        follower_dict[follower.id] = follower

    # now we find all your "non_friends" - people who don't follow you
    # even though you follow them.

    non_followers = [friend for friend in friends if friend.id not in follower_dict] # people who are not following me but i am following them
    not_yet_following = [follower for follower in followers if follower.id not in friend_dict] # people who are following me but i am not following them
   

    for nf in non_followers:
        nf.unfollow() # unfollow non followers

    for nyf in not_yet_following:
        nyf.follow()
        api.update_status(status="Thanks for the follow @%s" % (nyf.screen_name))  # Saying hello to new followers
       

def status_update(textgen, timer, upper_limit): # Updates the status
    counter = 0
    while counter < upper_limit:
        check_followers()

        api.update_status(status=''.join(textgen.generate(temperature=1, return_as_list=True, max_gen_length=280))) # Publishes tweet
        counter += 1
        time.sleep(timer) # Waits for specified time

def training(textgen, filename, e):
    textgen.train_from_file([tottels bot.docx](https://github.com/esbarth/tottels-bot/files/7520964/tottels.bot.docx)
()
, num_epochs=int(e))
    textgen.generate()

# Status updates based on args
if len(sys.argv) == 1:
    t = textgenrnn("textgenrnn_weights.hdf5")
    status_update(t, 0, 1)
elif sys.argv[1] == "train":
    os.remove("textgenrnn_weights.hdf5")
    t = textgenrnn()
    training(t, sys.argv[2], sys.argv[3])
else:
    t = textgenrnn("textgenrnn_weights.hdf5")
    status_update(t, int(sys.argv[1]), int(sys.argv[2]))
