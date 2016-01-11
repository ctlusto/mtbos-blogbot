MTBoS Blogbot
=============

I, Robot
--------
This is the code that powers the [@MTBoS_Blogbot](https://twitter.com/MTBoS_Blogbot), for those of you who like your RSS feed Twitterfied. Follow the Blogbot or check out the [MTBoS Blogroll](http://www.mtbos-blogroll.org/) web page for hourly updates from blogs around the [mathtwitterblogosphere](http://mathtwitterblogosphere.weebly.com/), which is a pretty cool place. Even for a robot.

Adding Yourself to the Blogroll
-------------------------------
Feel free to tweet [@MTBoS_Blogbot](https://twitter.com/MTBoS_Blogbot) and let me/it know that you'd like to be added to the blogroll. Or, I suppose, let me know that you *don't* want to be on it anymore (I pulled your info from [@Jstevens009](https://twitter.com/Jstevens009)'s list on [fishing4tech](http://www.fishing4tech.com/mtbos.html)).

Of course, if you're a GitHub kind of person who's going to fork the repo anyway, you can just add yourself to `blogroll.yaml` (alphabetically by Twitter handle) and submit a pull request. Just make sure that the `feed_url` points to something that returns your XML feed.

Getting the Code
----------------
As you presumably know, the code is hosted at https://github.com/ctlusto/mtbos-blogbot.

To get your own copy of the repo and see what's what:
```bash
git clone git://github.com/ctlusto/mtbos-blogbot.git
cd mtbos-blogbot
```
You're going to need [pip](https://pip.pypa.io/en/stable/) to install Python packages. If you don't already have it:
```bash
sudo easy_install pip
```

You're also going to need [virtualenv](https://virtualenv.readthedocs.org/en/latest/) to manage dependencies:
```bash
pip install virtualenv
```

Setting Up for Development
--------------------------
Create a virtual environment and install dependencies:
```bash
make env
```

If you already have a virtual environment, just install dependencies:
```bash
make deps
```

Activate your virtual environment:
```bash
source env/bin/activate
```

When you're done hacking, you can simply deactivate the virtual environment:
```bash
deactivate
```

Running Tests
-------------
LOLWUT!? There are no tests.

Firebase and Twitter
--------------------
The Blogbot uses [Firebase](https://www.firebase.com/) as a backend data store and the [Twitter API](https://dev.twitter.com/overview/documentation) to post updates. If you want your bot to do something useful, you'll need to [set up a Firebase app](https://www.firebase.com/docs/web/guide/setup.html) and [register your app with Twitter](https://apps.twitter.com/).

From there, you'll need to include some of your account credentials in order to authorize requests. The stuff you'll need to get is listed in `config.example.py`. Fill in the empty strings with your personal keys and tokens from their respective providers and rename the file `config.py`. (Make sure you don't check your actual `config.py` file into source control, please.)

Creating/Updating a Blogroll
----------------------------
The feeds you want to follow should live in `blogroll.yaml`. Just make sure that the `feed_url` points to something that returns XML (*not*, for example, the main blog page).

Save your changes and run:
```bash
scripts/migrate.py
```
Any feeds that aren't already in Firebase will be added to the database and have a current snapshot recorded.

Tweeting Updates
----------------
To check for updates and tweet any new posts:
```bash
python scripts/blogbot.py
```

If you want to check for updates and tweet them on a regular basis, you can run `blogbot.py` as a [Cron job](https://en.wikipedia.org/wiki/Cron). Just like a real robot.

Author
------
Chris Lusto

Twitter: [@Lustomatical](https://twitter.com/lustomatical)

Site: [{math pun}](http://chrislusto.com/)

License
-------
MIT

