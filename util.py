from selenium import webdriver
import time
import requests
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from post import Page
import locale


class Util:
    delay = 10  # seconds

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
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

            cancel_popup = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Cancel')]")))
            cancel_popup.click()
        except TimeoutException:
            print("Loading took too much time!")

    def search_by_tag(self, tag):
        self.driver.get("https://www.instagram.com/explore/tags/" + tag)

    def get_tagged_page_urls_from_post_url(self, post_url):
        self.driver.get(post_url)
        page_url_set = set()
        for tagged_page in self.driver.find_elements_by_xpath("//a[@class='JYWcJ']"):
            page_url_set.add(tagged_page.get_attribute("href"))
        print(page_url_set)
        return page_url_set

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

    def build_post_from_post_url(self, post_url):
        self.driver.get(post_url)
        print(self.driver.find_element_by_xpath("//h2[@class='BrX75']/a").get_attribute("href"))  # author page
        print(self.driver.find_element_by_xpath("//div[@class='Nm9Fw']/a/span").text)  # likes

    def build_page_from_page_url(self, page_url):
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
