import random
import tweepy
from tweepy import API

import local

# Authenticate through Twitter
auth = tweepy.OAuthHandler(local.API_KEY, local.API_SECRET)
auth.set_access_token(local.ACCESS_TOKEN, local.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#Parameter called replyTo=None as default, with option to reply to
def create_tweet(status_id, publish=False):
    global api

    tweet = api.get_status(status_id)

    with open("resources.txt", "r") as resources_file:
        resources_list = list(resources_file)

    tweet_text = f"@{tweet.author.screen_name} we found a resource for you! Check this out: \n" + random.choice(
        resources_list)

    #Option 1
    #if replyTo:
    #   add @ mention to beginning of tweet text OR use Tweepy to reply

    if publish:
        # Option 2
        #if replyTo
        print("Actually Tweet the thing")
        # Assuming next line would be a way to generate the Tweet?
        api.update_status(tweet_text, in_reply_to_status_id=status_id, auto_populate_reply_metadata=True)
    else:
        print("In reply to: ", status_id, "\n", tweet_text)


def get_mentions():
    global api

    # Testing OPTION A - read and then write
    replied_mentions = []

    with open("mentions.txt", "r") as mentions_file:
        for line in mentions_file:
            replied_mentions.append(line.strip())

    with open("mentions.txt", "a") as mentions_file:
        mentions = api.mentions_timeline(since_ids=replied_mentions[-1])
        mentions.reverse()
        for mention in mentions:
            if int(mention.id) > int(replied_mentions[-1]):
                if int(mention.id) not in replied_mentions:
                    print(mention.id, " is not in replied_mentions, and will be added to mentions.txt")
                    mentions_file.write(str(mention.id))
                    mentions_file.write("\n")
                    print("Response to Tweet #", str(mention.id), ": ")
                    # If tweet starts with @botname
                    # Reply to the tweet
                    create_tweet(mention.id, publish=True)
                    #create_tweet(mention.id)

    # Testing OPTION B - Read and write at once - Pull replied mentions from mentions_file and then write
    # with open("mentions.txt", "a+") as mentions_file:
    #     mentions = api.mentions_timeline(since_ids=replied_mentions[-1])
    #     for mention in mentions:
    #         for line in mentions_file:
    #             if str(mention.id) != line:
    #                 mentions_file.write(str(mention.id))
    #                 mentions_file.write("\n")


def main():
    # create_tweet()
    # pass
    # print(dir())
    get_mentions()


main()
