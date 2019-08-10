class Page:
    def __init__(self, url, num_posts, num_followers, num_following, nick_name, bio):
        self.num_posts = num_posts
        self.num_followers = num_followers
        self.num_following = num_following
        self.nick_name = nick_name
        self.bio = bio


class Post:
    def __init__(self, url, author_page, tag_page, photo_url, caption, num_likes, num_comments, post_timestamp):
        self.photo_url = photo_url
        self.caption = caption
        self.num_likes = num_likes
        self.num_comments = num_comments
        self.post_timestamp = post_timestamp
