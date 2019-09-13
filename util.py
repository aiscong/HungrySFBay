import locale
import requests
import datetime
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from post import *
import time


class Util:
    delay = 5  # seconds

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_experimental_option('prefs', {
            'credentials_enable_autosignin': False,
            'credentials_enable_service': False,
        })
        chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})
        self.driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)

    def log_in(self, username, password):
        self.driver.get("https://www.instagram.com/accounts/login")
        try:
            user_name_form = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.NAME, "username")))
            user_name_form.send_keys(username)

            password_form = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.NAME, "password")))
            password_form.send_keys(password)

            log_in_button = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
            log_in_button.click()

            # cancel_popup = WebDriverWait(self.driver, self.delay).until(
            #     EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Cancel')]")))
            cancel_popup = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Not Now')]")))
            cancel_popup.click()
        except TimeoutException:
            print("Loading took too much time!")

    def search_by_tag(self, tag):
        self.driver.get("https://www.instagram.com/explore/tags/" + tag)

    def get_post_urls_by_tag(self, tag):
        # post_url_set = set()
        post_url_set = []
        self.search_by_tag(tag)
        try:
            thumbnail_list = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='eLAPa']/parent::a")))
            for thumbnail in thumbnail_list:
                # post_url_set.add(thumbnail.get_attribute("href"))
                if thumbnail.get_attribute("href") not in post_url_set:
                    post_url_set.append(thumbnail.get_attribute("href"))
        except TimeoutException:
            print("Loading took too much time!")
        # print(post_url_set, sep="\n")
        return post_url_set

    def get_total_post_cnt_by_tag(self, tag):
        self.search_by_tag(tag)
        try:
            post_cnt_string = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='button']/parent::div"))).text.split(' ')[0]
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            post_cnt = locale.atoi(post_cnt_string)
        except TimeoutException:
            print("Loading took too much time!")
        tag = Tag(tag=tag, post_cnt=post_cnt)
        return tag

    def save_tag_post_cnt_info(self, tag_list_input, tag_info_output, refresh_date):
        tag_list = pd.read_csv(tag_list_input, sep='\t', header=None, names=['tags'])
        tag_list = tag_list.drop_duplicates().sort_values(by='tags')
        tag_list.to_csv(tag_list_input, index=False, header=False)
        tag_post_cnt_output = []
        for tag in tag_list.tags:
            tag_post_cnt_output.append(self.get_total_post_cnt_by_tag(tag))
        tag_df = pd.DataFrame(([t.__dict__ for t in tag_post_cnt_output]))
        tag_df['refresh_date'] = refresh_date

        def tag_size(x):
            if x > 500000:
                return 'Large'
            elif x > 100000:
                return 'Medium'
            else:
                return 'Small'

        tag_df['size'] = tag_df.post_cnt.apply(lambda x: tag_size(x))
        tag_df = tag_df[['tag', 'post_cnt', 'size', 'refresh_date']]
        tag_df.to_csv(tag_info_output, index=False)

    def get_tagged_user_id_from_post_url(self):
        tagged_user_id_set = set()
        for tag in self.driver.find_elements_by_xpath("//a[@class='JYWcJ']"):
            tagged_user_id_set.add(urlparse(tag.get_attribute("href")).path[1:-1])
        return list(tagged_user_id_set)

    def get_at_user_id_from_post_url(self):
        at_user_id_set = set()
        for at_user_id_element in self.driver.find_elements_by_xpath(
                "//h2[@class='_6lAjh']/parent::div/span/a[contains(text(),'@')]"):
            at_user_id_set.add(at_user_id_element.text[1:])
        return list(at_user_id_set)

    def get_hashtag_from_post_url(self):
        hashtag_set = set()
        for hashtag in self.driver.find_elements_by_xpath(
                "//h2[@class='_6lAjh']/parent::div/span/a[contains(text(),'#')]"):
            hashtag_set.add(hashtag.text[1:])
        return list(hashtag_set)

    def build_post_from_url(self, post_url, retry_time):
        if retry_time > 1:
            print("=========this is a retry===========")
        if retry_time > 3:
            print("==========3 retry failed===========")
            return None

        print("visiting {}".format(post_url))
        self.driver.get(post_url)
        # is_video1 = self.driver.find_elements_by_xpath("//div[@class='oJub8']")
        # is_video2 = self.driver.find_elements_by_xpath("//video[@class='tWeCl']")
        num_photos = self.driver.find_elements_by_xpath("//div[@class='KL4Bh']")
        if len(num_photos) > 1 or len(num_photos) == 0:
            print('This post contain multiple photos or videos')
            return
        try:
            author_username = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//h2[@class='BrX75']/a"))).text
            author_page = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//h2[@class='BrX75']/a"))).get_attribute("href")
            timestamp = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='c-Yi7']/time"))).get_attribute("datetime")
            timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            photo_url = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//img[@class='FFVAD']")))

            time.sleep(1)
            if photo_url.get_attribute("src") is None:
                print("====will retry=====")
                print(len(self.driver.find_elements_by_xpath("//img[@class='FFVAD']")))
                print(photo_url.get_attribute("alt"))
                print(photo_url.get_attribute("style"))
                print(photo_url.get_attribute("sizes"))
                print(photo_url.get_attribute("srcset"))

                return self.build_post_from_url(post_url, retry_time + 1)

            post = Post(author_username=author_username, author_page=author_page,
                        timestamp=timestamp, photo_url=photo_url.get_attribute("src"))
            try:
                num_likes = WebDriverWait(self.driver, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='Nm9Fw']/a/span"))).text
                post.num_likes = num_likes
            except TimeoutException:
                print('No likes expt')
                pass
            try:
                num_comments = WebDriverWait(self.driver, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, "//li[@class='lnrre']/button/span"))).text
                post.num_comments = num_comments
            except TimeoutException:
                print('No comments expt')
                pass
            try:
                caption_text = self.driver.find_element_by_xpath("//h2[@class='_6lAjh']/parent::div/span").text
                post.caption = Caption(text=caption_text)
            except NoSuchElementException:
                pass
            try:
                post.caption.at_username = self.get_at_user_id_from_post_url()
            except NoSuchElementException:
                pass
            try:
                post.caption.hashtag = self.get_hashtag_from_post_url()
            except NoSuchElementException:
                pass
            try:
                post.tagged_username = self.get_tagged_user_id_from_post_url()
            except NoSuchElementException:
                pass
            try:
                explore_location_name = WebDriverWait(self.driver, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@class='O4GlU']"))).text
                explore_location_url = WebDriverWait(self.driver, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@class='O4GlU']"))).get_attribute("href")
                explore_location = ExploreLocation(url=explore_location_url, name=explore_location_name)
                post.explore_location = explore_location
            except TimeoutException:
                print('No explore_location expt')
                pass
            print(post)
            return post
        except TimeoutException:
            print("Loading took too much time!")

    def save_photo(self, photo_url, path):
        img_data = requests.get(photo_url).content
        with open(path, 'wb') as handler:
            handler.write(img_data)

    def build_page_from_url(self, page_url):
        self.driver.get(page_url)
        is_private = self.driver.find_elements_by_xpath("//h2[@class='rkEop']")
        if len(is_private) > 0:
            print('This account is private')
            return
        try:
            follower_element = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[@href='{}followers/']/span".format(urlparse(page_url).path))))
            following_element = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[@href='{}following/']/span".format(urlparse(page_url).path))))
            num_post_element = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//a[@href='{}followers/']/ancestor::ul/li[1]/span/span".format(
                                                    urlparse(page_url).path))))
            username_element = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='nZSzR']/h1")))
            page = Page(url=page_url, num_followers=Util.parse_num_string(follower_element.get_attribute("title")),
                        num_following=Util.parse_num_string(following_element.text),
                        num_posts=Util.parse_num_string(num_post_element.text), username=username_element.text)
            try:
                name_element = WebDriverWait(self.driver, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[@class='rhpdm']")))
                page.name = name_element.text
            except NoSuchElementException:
                pass
            try:
                bio_element = self.driver.find_element_by_xpath("//div[@class='-vDIg']/span")
                page.bio = bio_element.text
            except NoSuchElementException:
                pass
            try:
                bio_link_element = self.driver.find_element_by_xpath("//div[@class='-vDIg']/a")
                page.bio_link = bio_link_element.text
            except NoSuchElementException:
                pass
            print(page)
            return page
        except TimeoutException:
            print("Loading took too much time!")

    @staticmethod
    def parse_num_string(num_string):
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            num = locale.atoi(num_string)
            return num
        except ValueError:
            print("Parsing {} error!".format(num_string))
