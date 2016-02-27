#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys

argfile = str(sys.argv[1])

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'XXXXX'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'XXXXX'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = 'XXXXX'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'XXXXX'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)




##Finds followers ids of a selected twitter user.
#text_file = open("idfile.txt", "w")
#
#ids = []
#for page in tweepy.Cursor(api.followers_ids, screen_name="Android").pages():
#    for line in page:
#        text_file.write(str(line))
#        text_file.write("\n")
#    #ids.extend(page)
#    time.sleep(60)
#
#text_file.close()
#Gets the name of said users.
#screen_names = [user.screen_name for user in api.lookup_users(user_ids=ids)]





# Following users from the idfile.txt and deleting those users from the file
# FOLLOW_THIS_MANY = 1000
#running = True
#counter = 0
#
#while running:
#
#    with open("idfile.txt", "r") as f:
#        line = f.readline()
#    api.create_friendship(int(line))
#    time.sleep(4)
#    with open("idfile.txt", "r") as fin:
#        data = fin.read().splitlines(True)
#    with open('idfile.txt', 'w') as fout:
#        fout.writelines(data[1:])
#
#    if counter > FOLLOW_THIS_MANY:
#        running = False
#    counter = counter + 1






#Unfollow users you are following, starting from the end of the file
your_name = 'flyBlockGame'
UNFOLLOW_THIS_MANY = 3000

text_file = open("followingnow.txt", "w")
ids = []
for page in tweepy.Cursor(api.followers_ids, screen_name=your_name).pages():
    for line in page:
        text_file.write(str(line))
        text_file.write("\n")
    #ids.extend(page)
    time.sleep(60)
text_file.close()
#Gets the name of said users.
#screen_names = [user.screen_name for user in api.lookup_users(user_ids=ids)]

running = True
counter = 0
while running:

    with open("followingnow.txt", "r") as f:
        lines = f.readlines()
        last_line = lines[-1]
    api.destroy_friendship(int(last_line))
    #time.sleep(2)
    with open("followingnow.txt", "r") as fin:
        data = fin.read().splitlines(True)
    with open('followingnow.txt', 'w') as fout:
        fout.writelines(data[:-1])

    if counter > UNFOLLOW_THIS_MANY:
        running = False
    counter = counter + 1











## Tweets tweets in tweets.txt
##filename=open(argfile,'r')
##f=filename.readlines()
##filename.close()
##for line in f:
##    api.update_status(status=line)
