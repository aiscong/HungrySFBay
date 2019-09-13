import util
import os
import pandas as pd
from datetime import date


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
    print("=====start new session========")
    ins = Instagram(auth[0], auth[1])

    sffood_tag_list_path = 'files/sffood_tag_list.txt'
    sffood_tag_info_path = 'files/sffood_tag_info.csv'
    username_info_path = 'files/username_info.csv'
    post_info_path = 'files/post_info.csv'
    photo_folder = 'photos/'

    # refresh tag size info
    # tag_refresh_date = date.today().strftime("%m/%d/%Y")
    # ins.util.save_tag_post_cnt_info(sffood_tag_list_path, sffood_tag_info_path, tag_refresh_date)

    sffood_tag_list = pd.read_csv(sffood_tag_list_path, sep='\t', header=None, names=['tags'])

    if os.path.exists(username_info_path):
        username_info = pd.read_csv(username_info_path)
        existing_user = set(username_info.username)
    else:
        existing_user = set()

    if os.path.exists(post_info_path):
        post_info = pd.read_csv(post_info_path)
        existing_post = set(post_info.photo_url)
    else:
        existing_post = set()

    new_username_set = set()
    new_username_info = []
    new_post_info = []

    for sffood_tag in sffood_tag_list.tags:
        post_url_list = ins.util.get_post_urls_by_tag(sffood_tag)[:9]

        for post_url in post_url_list:
            print("=====processing {}".format(post_url))
            post = ins.util.build_post_from_url(post_url, 1)
            if post is not None:
                if post.photo_url not in existing_post:
                    print("===to be added post===")
                    print(post)
                    new_post_info.append(post)
                    new_username_set.add(post.author_username)
                    new_username_set.union(set(post.tagged_username))
        if len(new_post_info) > 0:
            new_post_info = pd.DataFrame.from_records([p.to_dict() for p in new_post_info])
            new_post_info['source_tag'] = sffood_tag
            if not os.path.exists(post_info_path):
                new_post_info.to_csv(post_info_path, index=False)
            else:
                new_post_info.to_csv(post_info_path, mode='a', header=False, index=False)

        for username in new_username_set:
            username_url = 'https://www.instagram.com/' + username + '/'
            page = ins.util.build_page_from_url(username_url)
            if page is not None:
                if page.username not in existing_user:
                    new_username_info.append(page)
        if len(new_username_info) > 0:
            new_username_info = pd.DataFrame(([u.__dict__ for u in new_username_info]))
            if not os.path.exists(username_info_path):
                new_username_info.to_csv(username_info_path, index=False)
            else:
                new_username_info.to_csv(username_info_path, mode='a', header=False, index=False)
