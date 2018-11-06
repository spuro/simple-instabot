from InstagramAPI import InstagramAPI
from fake_useragent import UserAgent
import random
import urllib.request
import time
import os

#specifies useragent, this sort of precaution is necessary if you wish to bot continously
ua = UserAgent()
ua.chrome

#sets proxy via user input
print("Copy and paste your proxy in the following format:")
proxy = input("address:port (Requires IP verification through your proxy provider. Just press enter to continue without a proxy.) ")
print(proxy)
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

#double checking your proxy is in place
#safety precaution as accidentally using the wrong ip once on insta could get you banned
print("Your current IP is:")
htmlfile = urllib.request.urlopen("http://v6.ipv6-test.com/api/myip.php")
htmltext = htmlfile.read()
ip = "colored.clickselect".encode()
print(htmltext)
ip_confirm = input("Double check it . Continue with this? y / n ")
if ip_confirm != "y":
    input("Change your proxy then.")
    sys.exit()
else:
    print("Continuing")

def ask_for_info():
    """
    Ask the user running this script for certain info we need.
    Returns a dictionary with the answers.
    """
    username = input('What\'s your Instagram Username? ')
    password = input('What\'s your Instagram Password? ')
    num_to_follow = input('How many people should we follow per day? ')
    tags_to_use = [input('What tag should I use? (No #) ')]
    while True:
        more = input('Any more? (Leave blank for no) ')
        if more == '':
            break
        tags_to_use.append(more)

    # This does not validate the username or password, so make sure you enter in the right one!

    return {
        'username': username,
        'password': password,
        'num_to_follow': int(num_to_follow),
        'tags_to_use': tags_to_use
    }


def login(username, password):
    api = InstagramAPI(username, password)  # Instantiate the class
    api.login()  # Send a login request
    return api


def find_targets(api, tag):
    """
    Search for users who have posted a picture with tag, and return a list of user IDs.
    """

    ok = api.tagFeed(tag)  # Automatically prints an error
    if not ok:
        raise Exception  # Error the script

    resp = api.LastJson
    images = resp['items']

    users = []
    for image in images:
        users.append(
            # We use .get so we can filter out invalid data.
            # Invalid data is rare, but in this case we are prepared
            # pk is ID
            image.get('user', {}).get('pk', '')
        )

    # a list of users from the list of users which id isn't an empty string
    return [u for u in users if u != '']


def follow_all(api, targets, time_to_wait):
    """
    Follow all targets, while waiting time_to_wait in seconds
    """
    total_targets = len(targets)
    num = 0
    for t in targets:
        ok = api.follow(t)
        if not ok:
            print('Error while trying to follow ID: %s', t)
        num += 1
        print('Followed %d/%d' % (num, total_targets))
        time.sleep(time_to_wait)


if __name__ == '__main__':
    answers = ask_for_info()
    print('Thanks!')

    username = answers['username']
    password = answers['password']
    num_to_follow = answers['num_to_follow']
    tags_to_use = answers['tags_to_use']

    api = login(username, password)

    targets = []
    for tag in tags_to_use:
        targets += find_targets(api, tag)
    print('%d Targets Acquired!' % len(targets))

    secs_in_a_day = 86400
    time_to_wait = secs_in_a_day / num_to_follow

    follow_all(api, targets, time_to_wait)
    print('All Done!')
