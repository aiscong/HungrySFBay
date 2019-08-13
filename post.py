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
    def __init__(self, author_username, author_page, num_likes, num_comments, timestamp, photo_url,
                 caption=None, tagged_username=[], explore_location=None):
        self.author_username = author_username
        self.author_page = author_page
        self.num_likes = num_likes
        self.num_comments = num_comments
        self.timestamp = timestamp
        self.photo_url = photo_url
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


class Caption:
    def __init__(self, text, at_username=[], hashtag=[]):
        self.text = text
        self.at_username = at_username
        self.hashtag = hashtag

    def __str__(self):
        return "\n\ttext: {}\n" \
               "\t@_users: {}\n" \
               "\thashtags: {}".format(self.text, self.at_username, self.hashtag)


class ExploreLocation:
    def __int__(self, url, name):
        self.url = url
        self.name = name

    def __str__(self):
        return "\n\turl: {}\n" \
               "\tname: {}\n".format(self.url, self.name)
