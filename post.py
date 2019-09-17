class Caption:
    def __init__(self, text="", at_username=[], hashtag=[]):
        self.text = text
        self.at_username = at_username
        self.hashtag = hashtag

    def __str__(self):
        return "\n\ttext: {}\n" \
               "\t@_users: {}\n" \
               "\thashtags: {}".format(self.text, self.at_username, self.hashtag)


class ExploreLocation:
    def __init__(self, url="", name=""):
        self.url = url
        self.name = name

    def __str__(self):
        return "\n\turl: {}\n" \
               "\tname: {}\n".format(self.url, self.name)


class Tag:
    def __init__(self, tag, post_cnt):
        self.tag = tag
        self.post_cnt = post_cnt

    def __str__(self):
        return "\n\ttag: {}\n" \
               "\tpost_cnt: {}".format(self.tag, self.post_cnt)


class Page:
    def __init__(self, username, url, num_posts, num_followers, num_following, name="", bio="", bio_link=""):
        self.username = username
        self.url = url
        self.num_posts = num_posts
        self.num_followers = num_followers
        self.num_following = num_following
        self.name = name
        self.bio = bio
        self.bio_link = bio_link

    def __str__(self):
        return "***************************************************\n" \
               "*username: {}\n" \
               "*url: {}\n" \
               "*num posts: {}\n" \
               "*num followers: {}\n" \
               "*num followings: {}\n" \
               "*name: {}\n" \
               "*bio: {}\n" \
               "*bio_link: {} \n" \
               "***************************************************" \
            .format(self.username, self.url, self.num_posts,
                    self.num_followers, self.num_following,
                    self.name, self.bio, self.bio_link)


class Post:
    def __init__(self, post_url, author_username, author_page, timestamp, photo_url,
                 num_likes=0, num_comments=0,
                 caption=Caption(), tagged_username=[], explore_location=ExploreLocation()):
        self.post_url = post_url
        self.author_username = author_username
        self.author_page = author_page
        self.timestamp = timestamp
        self.photo_url = photo_url
        self.num_likes = num_likes
        self.num_comments = num_comments
        self.caption = caption
        self.tagged_username = tagged_username
        self.explore_location = explore_location

    def __str__(self):
        return "***************************************************\n" \
               "*author username: {}\n" \
               "*author page: {}\n" \
               "*num_likes: {}\n" \
               "*num_comments: {}\n" \
               "*timestamp: {} \n" \
               "*photo url: {} \n" \
               "*caption: {} \n" \
               "*tagged username: {} \n" \
               "*explore location: {}\n" \
               "***************************************************" \
            .format(self.author_username, self.author_page,
                    self.num_likes,
                    self.num_comments, self.timestamp,
                    self.photo_url, self.caption,
                    self.tagged_username, self.explore_location)

    def to_dict(self):
        return {
            'post_url': self.post_url,
            'author_username': self.author_username,
            'author_page': self.author_page,
            'timestamp': self.timestamp,
            'photo_url': self.photo_url,
            'num_likes': self.num_likes,
            'num_comments': self.num_comments,
            'caption_text': self.caption.text,
            'caption_at_user': self.caption.at_username,
            'caption_hashtag': self.caption.hashtag,
            'tagged_username': self.tagged_username,
            'explore_location_name': self.explore_location.name,
            'explore_location_url': self.explore_location.url
        }

