import feedparser
import twitter
import logging
import os
from firebase import firebase
from strongetags import stripweak

# Environment variables
FIREBASE_URL = os.environ.get('FIREBASE_URL')
FIREBASE_SECRET = os.environ.get('FIREBASE_SECRET')
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_TOKEN_SECRET = os.environ.get('TWITTER_TOKEN_SECRET')

# Logging setup
root_dir = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.DEBUG,
                    filemode='w',
                    filename=os.path.join(root_dir, '..', 'blogbot.log'))

# Firebase setup
print FIREBASE_URL
fb = firebase.FirebaseApplication(FIREBASE_URL, None)
auth = {'auth': FIREBASE_SECRET}

# Twitter setup
api = twitter.Api(consumer_key=TWITTER_API_KEY,
                  consumer_secret=TWITTER_API_SECRET,
                  access_token_key=TWITTER_ACCESS_TOKEN,
                  access_token_secret=TWITTER_TOKEN_SECRET)

def tweetblog(title, author, url):
    """Tweet a blog post"""

    message = u"""\
    "{}"

    via {}

    {}
    """.format(title, author, url)

    try:
      api.PostUpdate(message)
      print message
      logging.info(message)
    except twitter.TwitterError as e:
      print e
      logging.error(e)

def post_updates(res):
  """
  Tweet all blog posts that are new since the last call
  """

  updates = 0
  print 'Parsing feeds...'

  for blog, data in res.iteritems():
    current_etag = data.get('etag')
    current_modified = data.get('modified')
    current_owner = data.get('owner')
    current_url = data.get('url')
    latest_link = data.get('latest_link')

    # Conditional GET
    feed_data = feedparser.parse(current_url,
                                 etag=current_etag,
                                 modified=current_modified)

    print current_url
    logging.info(current_url)
    if feed_data.bozo:
      logging.info('Got malformed XML.')

    # A nonempty array means there's an update
    # (A few edge cases produce false positives...see comment below)
    if feed_data.entries:
      post = feed_data.entries[0]
      post_title = post.get('title')
      post_link = post.get('link')

      if post_link != latest_link: # The 2xx wasn't a false positive

        # Send the tweet
        tweetblog(post_title, current_owner, post_link)

        # Update the metadata
        new_etag = feed_data.get('etag')
        new_modified = feed_data.get('modified')
        data['latest_link'] = post_link
        if current_etag:
          data['etag'] = stripweak(new_etag)
        if current_modified:
          data['modified'] = new_modified

        updates += 1

      else:
        logging.info('No new content.')

    else:
      logging.info('No new content.')


  if updates:
    fb.patch('blogs/', res, params=auth)

  print 'Posted %d update(s).' % updates
  logging.info('Posted %d update(s).' % updates)

# DO ALL THE THINGS
fb.get_async('blogs/', None, params=auth, callback=post_updates)
