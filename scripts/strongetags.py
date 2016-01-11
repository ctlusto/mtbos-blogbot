import re

weak_flag = re.compile(r'W/')

def stripweak(etag):
    """
    Strip the leading 'W/' from weak ETags
    """

    # Some sort of interaction between Feedparser and Blogger sometimes
    # leads to a 200 response instead of 304 if the raw weak ETag
    # is passed as an argument to feedparser.parse(), which
    # defeats the purpose of conditional GET requests later on.
    return weak_flag.sub('', etag)