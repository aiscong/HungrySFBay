class Page:
    def __init__(self, user_name, url, num_posts, num_followers, num_following, name="", bio="", bio_link=""):
        self.user_name = user_name
        self.url = url
        self.num_posts = num_posts
        self.num_followers = num_followers
        self.num_following = num_following
        self.name = name
        self.bio = bio
        self.bio_link = bio_link


# url, photo_url
class Post:
    def __init__(self, author_username, author_page, num_likes, num_comments, timestamp,
                 caption=None, tagged_user_id=[], explore_location=None):
        self.author_username = author_username
        self.author_page = author_page
        self.num_likes = num_likes
        self.num_comments = num_comments
        self.timestamp = timestamp
        self.caption = caption
        self.tagged_user_id = tagged_user_id
        self.explore_location = explore_location


class Caption:
    def __init__(self, text, at_user_id=[], hashtag = []):
        self.text = text
        self.at_user_id = at_user_id
        self.hashtag = hashtag


class ExploreLocation:
    def __int__(self, url, name):
        self.url = url
        self.name = name
