class Page:
    def __init__(self, url, user_name, num_posts, num_followers, num_following, name="", bio="", bio_link=""):
        self.url = url
        self.user_name = user_name
        self.num_posts = num_posts
        self.num_followers = num_followers
        self.num_following = num_following
        self.name = name
        self.bio = bio
        self.bio_link = bio_link


class Post:
    def __init__(self, url, author_page, tag_page, photo_url, caption, num_likes, num_comments, explore_location, timestamp):
        self.photo_url = photo_url
        self.caption = caption
        self.num_likes = num_likes
        self.num_comments = num_comments
        self.explore_location = explore_location
        self.timestamp = timestamp


class ExploreLocation:
    def __int__(self, url, name):
        self.url = url
        self.name = name