import util
import pandas as pd


class Instagram:
    def __init__(self, un, ps):
        self.username = un
        self.password = ps
        self.util = util.Util()
        self.util.log_in(un, ps)
        # self.util.search_by_tag("sffoodie")
        # self.util.get_post_urls_by_tag("sffood")
        # self.util.build_post_from_url("https://www.instagram.com/p/B1FoVuKHj68/")
        # self.util.build_post_from_url("https://www.instagram.com/p/B1NVB90D1LS/")
        # self.util.build_page_from_url("https://www.instagram.com/katieeeebell/")
        # self.util.build_post_from_url("https://www.instagram.com/p/B0eCF1uhKwp/")
        # test_post = self.util.build_post_from_url("https://www.instagram.com/p/B0_dJJsgyU1/")
        # self.util.get_total_post_cnt_by_tag("yummy")
        # self.util.save_tag_post_cnt_info(sffood_tag_list_path, sffood_tag_info_path, tag_refresh_date)


if __name__ == '__main__':
    auth = open('safe', 'r').readline().split(':')
    ins = Instagram(auth[0], auth[1])

    sffood_tag_list_path = 'files/sffood_tag_list.txt'
    sffood_tag_info_path = 'files/sffood_tag_info.csv'
    tag_refresh_date = '20190815'
    # ins.util.save_tag_post_cnt_info(sffood_tag_list_path, sffood_tag_info_path, tag_refresh_date)

    username_info_path = 'files/username_info.csv'
    post_info_path = 'files/post_info.csv'
    photo_folder = 'photos/'
    username_set = set()
    username_info = []
    post_info = []
    post_url_set = ins.util.get_post_urls_by_tag("sffood")

    for post_url in post_url_set:
        print(post_url)
        post = ins.util.build_post_from_url(post_url)
        if post is not None:
            post_info.append(post)
            username_set.add(post.author_username)
            username_set.union(set(post.tagged_username))
    if len(post_info) > 0:
        post_info = pd.DataFrame.from_records([p.to_dict() for p in post_info])
        post_info.to_csv(post_info_path, index=False)

    for username in username_set:
        print(username)
        username_url = 'https://www.instagram.com/' + username + '/'
        page = ins.util.build_page_from_url(username_url)
        if page is not None:
            username_info.append(page)
    if len(username_info) > 0:
        username_info = pd.DataFrame(([u.__dict__ for u in username_info]))
        username_info.to_csv(username_info_path, index=False)
