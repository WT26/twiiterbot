#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys

#argfile = str(sys.argv[1])

selection = input("Which user, use number?\n1. @flyBlockGame\n2. @DevWt26\n")


if(selection == 1):
    #enter the corresponding information from your Twitter application:
    your_name = 'flyBlockGame'
    CONSUMER_KEY = 'xxxxx'#keep the quotes, replace this with your consumer key
    CONSUMER_SECRET = 'xxxxx'#keep the quotes, replace this with your consumer secret key
    ACCESS_KEY = 'xxxxx'#keep the quotes, replace this with your access token
    ACCESS_SECRET = 'xxxxx'#keep the quotes, replace this with your access token secret
else:
    your_name = 'DevWt26'
    CONSUMER_KEY = 'xxxxx'
    CONSUMER_SECRET = 'xxxxx'
    ACCESS_KEY = 'xxxxxx'
    ACCESS_SECRET = 'xxxxx'

UNFOLLOW_THIS_MANY = 3000
FOLLOW_THIS_MANY = 1000
USER_TO_FIND_FOLLOWERS_OF = 'Android'
print ("\n\nAccount name: " + your_name + "\nUnfollowing: " +
       str(UNFOLLOW_THIS_MANY) + "\nFollowing: " + str(FOLLOW_THIS_MANY) + "\nUser to find followers of: " + USER_TO_FIND_FOLLOWERS_OF + "\n\n")
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

command = input("What do you want to do?\n1. Find users to idfile.txt\n2. "
                  "Follow users from idfile.txt\n3. Unfollow people you are following\n")

if(command == str(1)):
    ##Finds followers ids of a selected twitter user.
    text_file = open("idfile.txt", "w")

    ids = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=USER_TO_FIND_FOLLOWERS_OF).pages():
        for line in page:
            text_file.write(str(line))
            text_file.write("\n")
        #ids.extend(page)
        time.sleep(60)

    text_file.close()
    #Gets the name of said users.
    #screen_names = [user.screen_name for user in api.lookup_users(user_ids=ids)]




elif(command == str(2)):
    # Following users from the idfile.txt and deleting those users from the file
    running = True
    counter = 0
    every_tenth = 0

    print("Starting to follow: " + str(FOLLOW_THIS_MANY) + " Users..\n" )
    while running:
        with open("idfile.txt", "r") as f:
            line = f.readline()
        #try:
        api.create_friendship(int(line))
        ##except tweepy.TweepError:
        #    print("Skipping an Id, some problem with it(Account deleted etc.)")
        #    pass
        time.sleep(1)
        with open("idfile.txt", "r") as fin:
            data = fin.read().splitlines(True)
        with open('idfile.txt', 'w') as fout:
            fout.writelines(data[1:])

        if counter > FOLLOW_THIS_MANY:
            running = False
        counter = counter + 1

        if every_tenth > 10:
            print ("Followed so far: " + str(counter) + "/" + str(FOLLOW_THIS_MANY))
            every_tenth = 0

        every_tenth += 1



elif(command == str(3)):
    #Unfollow users you are following, starting from the end of the file
    text_file = open("followingnow.txt", "w")
    ids = []
    for page in tweepy.Cursor(api.friends_ids, screen_name=your_name).pages():
        for line in page:
            text_file.write(str(line))
            text_file.write("\n")
        print("Batch done, waiting 60s..\n")
        #ids.extend(page)
        time.sleep(60)
    text_file.close()
    #Gets the name of said users.
    #screen_names = [user.screen_name for user in api.lookup_users(user_ids=ids)]

    print("All current 'following now gathered', Starting to unfollow.\n")
    running = True
    counter = 0
    per_hundred = 0
    while running:

        with open("followingnow.txt", "r") as f:
            lines = f.readlines()
            last_line = lines[-1]
        api.destroy_friendship(int(last_line))
        with open("followingnow.txt", "r") as fin:
            data = fin.read().splitlines(True)
        with open('followingnow.txt', 'w') as fout:
            fout.writelines(data[:-1])

        if counter > UNFOLLOW_THIS_MANY:
            running = False
        counter = counter + 1

        if(per_hundred > 100):
            print("100 more unfollowed, continuing..")
            per_hundred = 0
        per_hundred += 1

    print("Unfollowing done!")









## Tweets tweets in tweets.txt
##filename=open('tweets.txt','r')
##f=filename.readlines()
##filename.close()
##for line in f:
##    api.update_status(status=line)
#time.sleep(900) #15mins
