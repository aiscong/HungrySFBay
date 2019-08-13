from selenium import webdriver
import os
import time
import util


class Instagram:
    def __init__(self, un, ps):
        self.username = un
        self.password = ps
        self.util = util.Util()
        self.util.log_in(un, ps)
        # self.util.search_by_tag("sffood")
        # self.util.search_by_tag("Sffoodie")
        # self.util.get_post_urls_by_tag("sffood")
        # self.util.get_tagged_page_urls_from_post_url("https://www.instagram.com/p/B01f42sBFzh/")
        # self.util.build_post_from_post_url("https://www.instagram.com/p/B01f42sBFzh/")
        # self.util.build_page_from_page_url("https://www.instagram.com/katieeeebell/")


if __name__ == '__main__':
    auth = open('safe', 'r').readline().split(':')
    ins = Instagram(auth[0], auth[1])




