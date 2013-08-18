# stellar-tweetbot (python version)

## Instructions

### Getting started

1. Make sure you have an account on [stellar.io](http://www.stellar.io) and you're following interesting people.
2. Make a zombie/bot account on [twitter](http://www.twitstellar.com). You can call it whatever you like.
3. While you're still logged into your zombie account, go to the [twitter dev site](https://dev.twitter.com/apps/new) to create a new application. Provide all required information (whatever works - you only want the api keys). Create your access token on the next screen by pressing on the `create my access token` button, go to the `Settings` tab, change the `Access` checker to `Read and Write`, and `Update this twitters application settings`.
4. Go back to `details` and copy the Consumer key, Consumer secret, Access token & Access token secret for later configuration.
5. Create a folder on your server for this bot, and change into the director (`cd`).

### Installation

I assume you have [virtualenv](http://www.virtualenv.org) and [pip](http://www.pip-installer.org) installed. If not, this would be a good time :-).

#### Using the bootstrap script

6. Run the bootstrap script, and proceed with the configuration

```bash
git clone https://github.com/pjan/stellar-tweetbot.git && cd stellar-tweetbot && source bootstrap.sh
```

#### The longer way...

6. Clone the repository in your directory of choice (`git clone https://github.com/pjan/stellar-tweetbot.git`)
7. Change (`cd`) into the directory and make a new virtualenv (e.g. `virtualenv env`)
8. Load the virtualenv (`env/bin/activate`) and install tweepy (`pip install tweepy`)
9. Change the index.py permissions to 755.

Alternatively... if you don't want to use virtualenv and/or python: the script depends on the [tweepy](https://github.com/tweepy/tweepy) library, so make sure you then have it on your pythonpath/site-packages.


### Configuration

10. Edit the index.py script with your zombie/bot account, your stellar feed url, the api info from step 4 (key, token & secrets). The history file is the name of a local file that will keep track of what the bot has retweeted (and thus acts as a pointer). The retweet flag defines whether the stellar tweets should be retweeted by the bot, the tweet_others flag will generate a tweet ('title - url' format) of the other (non-twitter) stellar items.
11. Make sure the index.py parent folder is writable for the account running the script (or alternatively, `touch` the history file, and change it's permissions)
12. Set up a cron job (`crontab -e`). e.g., if you want it to run every 5 minutes...

```
*/5 * * * * /path/to/your/stellar-tweetbot/env/bin/python /path/to/your/stellar-tweetbot/index.py
```

Now follow your zombie/bot account, and you're done.

## Credits

Thanks to [Jason Kottke](http://kottke.org/) for his inception of stellar.io, and [Mike Davidson](http://www.mikeindustries.com/) for making the original version of this script in php. The script stopped working for me a couple of months ago, which became my motivation to create this python-based port. At the same time, it should be easier to install, and provide some extra functionality.
