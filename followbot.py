#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy, time, sys, os

def followbot():
    #name_to_find_ids_of = input("Name to find ids of? Example: twitter, Android, gameinformer, gamasutra\n>")
    name_to_find_ids_of = 'twitter'
    name_list = []
    info_list = []
    with open("twitter_accounts.txt", "r") as f:
        lines = f.readlines()

        print("Gathering status of all accounts in the .txt file, this will take a while.")
        for line in lines:
            list = line.split(':')

            name = list[0]
            CONSUMER_KEY = list[1]
            CONSUMER_SECRET = list[2]
            ACCESS_KEY = list[3]
            ACCESS_SECRET = list[4][:-1]
            #print(repr(CONSUMER_KEY))
            #print(repr(CONSUMER_SECRET))
            #print(repr(ACCESS_KEY))
            #print(repr(ACCESS_SECRET))

            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
            api = tweepy.API(auth)

            text_file = open("unfollowlist.txt", "w")
            following_counter = 0
            for page in tweepy.Cursor(api.friends_ids, screen_name=name).pages():
                for line in page:
                    following_counter += 1
                    text_file.write(str(line))
                    text_file.write("\n")
                #time.sleep(60)
            text_file.close()
            with open("followingnow.txt", "r") as f:
                lines = f.readlines()
                last_line = lines[-1]
            write_actions = True
            try:
                api.destroy_friendship(int(last_line))

            except tweepy.TweepError as e:
                errorcode = e.args[0][0]['code']
                if (errorcode == 261):
                    print("Application cannot do write actions. Name: " + name)
                    write_actions = False
                else:
                    print(e)
                    print("Error happened on account: " + name)
                    time.sleep(10)
                pass

            except ConnectionResetError:
                print("Connection error, sleeping 10s and continuing")
                time.sleep(10)
                continue

            new_list = [name, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, following_counter, write_actions]
            info_list.append(new_list)
            name_list.append(new_list[0])


    for acc in info_list:
        if (int(acc[5]) > 2126) and acc[6]:
            number_to_unfollow = int(acc[5]) - 2126
            unfollow(acc, number_to_unfollow)

    for acc in info_list:
        if acc[6]:
            follow(acc, name_to_find_ids_of)




def unfollow(acc, number_to_unfollow):

    name = acc[0]
    CONSUMER_KEY = acc[1]
    CONSUMER_SECRET = acc[2]
    ACCESS_KEY = acc[3]
    ACCESS_SECRET = acc[4]

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    text_file = open("unfollowlist.txt", "w")
    for page in tweepy.Cursor(api.friends_ids, screen_name=name).pages():
        for line in page:
            text_file.write(str(line))
            text_file.write("\n")
    print("People who " + name + " is currently following gathered, starting the unfollowing")
    text_file.close()

    #print("All current 'following now gathered', Starting to unfollow.\n")
    running = True
    counter = 0
    while running:
        try:
            with open("followingnow.txt", "r") as f:
                lines = f.readlines()
                last_line = lines[-1]
            try:
                api.destroy_friendship(int(last_line))
            except ConnectionResetError or tweepy.TweepError:
                print("Some sort of error, waiting 20s")
                time.sleep(20)
                pass
            time.sleep(6)
            with open("followingnow.txt", "r") as fin:
                data = fin.read().splitlines(True)
            with open('followingnow.txt', 'w') as fout:
                fout.writelines(data[:-1])

            s = str(counter) + ' / ' + str(number_to_unfollow) + ' unfollowed.'# string for output
            print(s, end='')                        # just print and flush
            # sys.stdout.flush()                    # needed for flush when using \x08
            backspace(len(s))                       # back for n chars

            if counter >= number_to_unfollow:
                running = False
            counter = counter + 1

        except tweepy.TweepError or ConnectionResetError:
            print("Some sort of error, waiting 20s")
            time.sleep(20)
            pass
    print("Unfollowing done on " + name + "!")

def backspace(n):
    # print((b'\x08' * n).decode(), end='') # use \x08 char to go back
    print('\r' * n, end='')                 # use '\r' to go back

def follow(acc, name_to_find_followers_of):

    name = acc[0]
    CONSUMER_KEY = acc[1]
    CONSUMER_SECRET = acc[2]
    ACCESS_KEY = acc[3]
    ACCESS_SECRET = acc[4]

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Following users from the idfile.txt and deleting those users from the file
    running = True
    counter = 1

    print("Starting to follow: " + str(1000) + " Users on: " + name )
    while running:
        if os.stat("idfile.txt").st_size <= 0:
            find_ids(api, name_to_find_followers_of)
        else:
            with open("idfile.txt", "r") as f:
                line = f.readline()
            try:
                api.create_friendship(int(line))
                counter += 1
            except tweepy.TweepError as e:
                errorcode = e.args[0][0]['code']
                if (errorcode == 261):
                    print("Application cannot do write actions. Name: " + name)
                else:
                    print(e)
                    print("Error happened on account: " + name)
                    time.sleep(10)
                pass
            except ConnectionResetError:
                print("Connection error, sleeping 10s and continuing")
                time.sleep(10)
                continue
            time.sleep(5)
            with open("idfile.txt", "r") as fin:
                data = fin.read().splitlines(True)
            with open('idfile.txt', 'w') as fout:
                fout.writelines(data[1:])


            s = str(counter) + ' / ' + str(1000) + ' followed.'# string for output
            print(s, end='')                        # just print and flush
            # sys.stdout.flush()                    # needed for flush when using \x08
            backspace(len(s))                       # back for n chars

            if counter > 995:
                running = False
                print("Following Done on: " + name)


def find_ids(api, name_to_find_ids_of):

    text_file = open("idfile.txt", "w")
    counter = 0
    for page in tweepy.Cursor(api.followers_ids, screen_name=name_to_find_ids_of).pages():
        for line in page:
            text_file.write(str(line))
            text_file.write("\n")
        time.sleep(60)
        counter += 1
        if (counter > 10):
            break
    text_file.close()


def run():
    running = True
    while running:
        DAY_IN_SECONDS = 86400
        start_time = time.time()

        followbot()

        script_took = start_time - time.time()
        time_to_wait = DAY_IN_SECONDS - script_took
        time.sleep(time_to_wait)


run()