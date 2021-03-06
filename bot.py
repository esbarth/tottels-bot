# tottels-bot

# This bot constructs random tweets using a neural network provided by textgenrnn
# It can also tweet every t seconds based on user args

# @author Emily Barth
# @date 11/11/2021
# Check out my github at https://github.com/esbarth

#!/usr/bin/env python
"""
Tweet a random line from a text file.
For example, use it to tweet a random six-word sentence from Project Gutenberg.
https://twitter.com/sixworderbot
"""
try:
    import resource

    mem0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024.0)
except ImportError:
    # resource not on Windows
    pass

import argparse
import random
import sys
import twitter
import webbrowser
import yaml

TWITTER = None

SEPERATORS = [" ", " ", " ", " ", "\n", "\n", "\n\n"]


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode("utf-8"))


def timestamp():
    if args.quiet:
        return
    import datetime

    print(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))


def load_yaml(yamlkey.txt):
    """
    File should contain:
    consumer_key: QLtH7XGp8pCweIjqu9R76ivxi
    consumer_secret: bkKM7WgLWin46udwvk8ZWFGDK9GYP2MhalGcJLUYytgYEvi5kV
    access_token: 1457755087971966980-aJl398na3NWlNkx3rP21vxKY7l0sg5
    access_token_secret: Ci0tK1i4rHwyIPALkbyc2i4SphNk9C2KWK6v7ixwzC9WW
    """
    with open(tottels_bot.txt) as f:
        data = yaml.safe_load(f)

    keys = data.viewkeys() if sys.version_info.major == 2 else data.keys()
    if not keys >= {
        "access_token",
        "access_token_secret",
        "consumer_key",
        "consumer_secret",
    }:
        sys.exit("Twitter credentials missing from YAML: " + filename)

    return data


def get_twitter():
    global TWITTER

    if TWITTER is None:
        data = load_yaml(args.yaml)

        # Create and authorise an app with (read and) write access at:
        # https://dev.twitter.com/apps/new
        # Store credentials in YAML file
        TWITTER = twitter.Twitter(
            auth=twitter.OAuth(
                data["access_token"],
                data["access_token_secret"],
                data["consumer_key"],
                data["consumer_secret"],
            )
        )

    return TWITTER


def get_random_sentence_from_file():
    with open(args.infile) as f:
        lines = f.read().splitlines()

    return random.choice(lines)


def tweet_it(string, in_reply_to_status_id=None):
    global TWITTER

    if len(string) <= 0:
        print("ERROR: trying to tweet an empty tweet!")
        return

    t = get_twitter()

    if not args.quiet:
        print_it("TWEETING THIS: " + string)

    if args.test:
        if not args.quiet:
            print("(Test mode, not actually tweeting)")
    else:
        if not args.quiet:
            print("POST statuses/update")
        result = t.statuses.update(
            status=string, in_reply_to_status_id=in_reply_to_status_id
        )
        url = (
            "http://twitter.com/"
            + result["user"]["screen_name"]
            + "/status/"
            + result["id_str"]
        )
        if not args.quiet:
            print("Tweeted: " + url)
        if not args.no_web:
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


def get_random_hashtag():
    # CSV string to list
    hashtags = args.hashtags.split(",")
    # Replace "None" with None
    hashtags = [None if x == "None" else x for x in hashtags]
    # Return a random hashtag
    return random.choice(hashtags)


def main():
    random_sentence = get_random_sentence_from_file()
    print(random_sentence)

    hashtag = get_random_hashtag()
    if not hashtag:
        tweet = random_sentence
    else:
        # 50% lowercase hashtag
        if random.randint(0, 1) == 0:
            hashtag = hashtag.lower()
        # Random order of text and hashtag
        things = [hashtag, random_sentence]
        random.shuffle(things)
        if not args.quiet:
            print(">" + " ".join(things) + "<")
        # Random separator between text and hashtag
        tweet = random.choice(SEPERATORS).join(things)

    if not args.quiet:
        print(">" + tweet + "<")
        print("Tweet this:\n", tweet)

    try:
        tweet_it(tweet)

    except twitter.api.TwitterHTTPError as e:
        print("*" * 80)
        print(e)
        print("*" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tweet a random line from a text file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-y",
        "--yaml",
        default="/Users/hugo/Dropbox/bin/data/randomsentencebot.yaml",
        # default='E:/Users/hugovk/Dropbox/bin/data/randomsentencebot.yaml',
        help="YAML file location containing Twitter keys and secrets",
    )
    parser.add_argument(
        "-i",
        "--infile",
        default="https://www.dropbox.com/s/5wbzgsaezuiwo4s/tottels_bot.txt",
        # default='https://www.dropbox.com/s/5wbzgsaezuiwo4s/tottels_bot.txt',
        help="A random line is chosen from this text file",
    )
    parser.add_argument(
        "--hashtags",
        default="#TottelsMiscellany",
        help="Comma-separated list of random hashtags",
    )
    parser.add_argument(
        "-nw",
        "--no-web",
        action="store_true",
        help="Don't open a web browser to show the tweeted tweet",
    )
    parser.add_argument(
        "-x",
        "--test",
        action="store_true",
        help="Test mode: go through the motions but don't update anything",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Only print out tweet (and errors)"
    )
    args = parser.parse_args()

    timestamp()
    main()

# End of file









