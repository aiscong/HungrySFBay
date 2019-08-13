import locale
import time
import requests
import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from post import Page
from post import Post
from post import Caption


class Util:
    delay = 10  # seconds

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
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

            cancel_popup = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Cancel')]")))
            cancel_popup.click()
        except TimeoutException:
            print("Loading took too much time!")

    def search_by_tag(self, tag):
        self.driver.get("https://www.instagram.com/explore/tags/" + tag)

    def get_post_urls_by_tag(self, tag):
        post_url_set = set()
        self.search_by_tag(tag)
        try:
            thumbnail_list = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='eLAPa']/parent::a")))
            for thumbnail in thumbnail_list:
                post_url_set.add(thumbnail.get_attribute("href"))
        except TimeoutException:
            print("Loading took too much time!")

        print(post_url_set, sep="\n")
        return post_url_set
        # thumbnail_href = thumbnail_list[0].get_attribute("href")
        # self.driver.get(thumbnail_href)
        # time.sleep(1)
        # photo_url = self.driver.find_element_by_xpath("//img[@class='FFVAD']").get_attribute("src")
        # self.driver.get(photo_url)
        # requests.get(photo_url).content
        # with open('image_name.jpg', 'wb') as handler:
        #     handler.write(img_data)
        #
        # print(len(thumbnail_list))

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

    def build_post_from_url(self, post_url):
        self.driver.get(post_url)
        try:
            author_username = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//h2[@class='BrX75']/a"))).text
            author_page = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//h2[@class='BrX75']/a"))).get_attribute("href")
            num_likes = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='Nm9Fw']/a/span"))).text
            num_comments = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//li[@class='lnrre']/button/span"))).text
            timestamp = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='c-Yi7']/time"))).get_attribute("datetime")
            timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            post = Post(author_username=author_username, author_page=author_page, num_likes=num_likes,
                        num_comments=num_comments, timestamp=timestamp)
            try:
                caption_text = self.driver.find_element_by_xpath("//h2[@class='_6lAjh']/parent::div/span").text
                post.caption = Caption(text=caption_text)
            except NoSuchElementException:
                pass

            try:
                post.caption.at_user_id = self.get_at_user_id_from_post_url()
            except NoSuchElementException:
                pass

            try:
                post.caption.hashtag = self.get_hashtag_from_post_url()
            except NoSuchElementException:
                pass

            try:
                post.tagged_user_id = self.get_tagged_user_id_from_post_url()
            except NoSuchElementException:
                pass

            try:
                explore_location = WebDriverWait(self.driver, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@class='O4GlU']"))).text
                post.explore_location = explore_location
            except NoSuchElementException:
                pass
            print(post.author_username)
            print(post.author_page)
            print(post.num_likes)
            print(post.num_comments)
            print(post.timestamp)
            print(post.caption)
            print(post.caption.at_user_id)
            print(post.caption.hashtag)
            print(post.tagged_user_id)
            print(post.explore_location)
        except TimeoutException:
            print("Loading took too much time!")

    def build_page_from_url(self, page_url):
        self.driver.get(page_url)
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
            user_name_element = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='nZSzR']/h1")))

            page = Page(url=page_url, num_followers=Util.parse_num_string(follower_element.get_attribute("title")),
                        num_following=Util.parse_num_string(following_element.text),
                        num_posts=Util.parse_num_string(num_post_element.text), user_name=user_name_element.text)

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
            print(page.url)
            print(page.name)
            print(page.num_followers)
            print(page.num_following)
            print(page.num_posts)
            print(page.user_name)
            print(page.bio)
            print(page.bio_link)
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
