import warnings

warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import sys
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import json
import os
from rich import print

class LoginError(Exception):
    pass

class crawler:    
       
    def __init__(self, keyword, start_date, end_date, email, username, password, path, debug) -> None:
        self.keyword = keyword
        self.start_date = start_date
        self.end_date = end_date
        self.email = email
        self.username = username
        self.password = password
        self.path = path
        self.chrome_options = webdriver.ChromeOptions()
        my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        service = Service(executable_path=ChromeDriverManager().install())
        self.chrome_options.add_argument("--log-level=3")
        self.chrome_options.add_argument(f"--user-agent={my_user_agent}")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        if not debug:
            self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        self.tweets_data_list = []
        self.error_count = 0


    # def debug(self):
    #     with open("test.html", "w", encoding="utf-8") as file:
    #         file.write(self.driver.page_source)

    def parse_count_string(self, count_str) -> int:
        multipliers = 1
        if "K" in count_str:
            multipliers = 1000
        elif "M" in count_str:
            multipliers = 1000000
        count_str = count_str.replace("K", "").replace("M", "")

        try:
            count = int(float(count_str) * multipliers)
            return count
        except ValueError:
            return None

    def get_articles(self,  timeout: int, target_count: int):
        
        flag = 0
        id_set = []
        timeout = timeout
        last_write_time = time.time()
        current_count = 0
        while True:
            # print(f"Found {len(tweets_data_list)} tweet(s) currently.", end="\r")
            current_time = time.time()
            articles = self.driver.find_elements(By.TAG_NAME, "article")

            for article in articles:
                data = {
                    "text": "",
                    "likes": 0,
                    "replies": 0,
                    "retweets": 0,
                    "reads": 0,
                    "publish_time": "",
                    "url": "",
                    "author": "",
                }
                try:
                    publish_time = article.find_element(
                        By.TAG_NAME, "time"
                    ).get_attribute("datetime")
                except Exception:
                    pass
                if publish_time:
                    data["publish_time"] = publish_time.split("T")[0]
                try:
                    tweet = article.find_element(
                        By.CSS_SELECTOR, '[data-testid="tweetText"]'
                    )
                except:
                    continue
                spans = tweet.find_elements(By.TAG_NAME, "span")
                id = tweet.get_attribute("id")

                for span in spans:
                    if "r-qvk6io" not in span.get_attribute(
                        "class"
                    ) and "r-lrvibr" not in span.get_attribute("class"):
                        data["text"] += span.text.replace("\n", "")

                likes = article.find_element(
                    By.CSS_SELECTOR, '[data-testid="like"]'
                ).text
                replies = article.find_element(
                    By.CSS_SELECTOR, '[data-testid="reply"]'
                ).text
                retweets = article.find_element(
                    By.CSS_SELECTOR, '[data-testid="retweet"]'
                ).text
                author = article.find_element(
                    By.CSS_SELECTOR, '[data-testid="User-Name"]'
                ).text
                reads = article.find_element(
                    By.CSS_SELECTOR, '[data-testid="app-text-transition-container"]'
                ).text


                if likes:
                    data["likes"] = self.parse_count_string(likes)
                else:
                    data["likes"] = 0
                if replies:
                    data["replies"] = self.parse_count_string(replies)
                else:
                    data["replies"] = 0
                if retweets:
                    data["retweets"] = self.parse_count_string(retweets)
                else:
                    data["retweets"] = 0
                if author:
                    # 获取@到下一个\n的字符串，包括@
                    data["author"] = author.split("@")[1].split("\n")[0]
                else:
                    data["author"] = "Unknown"
                if reads:
                    data["reads"] = self.parse_count_string(reads)
            
                try:
                    # 查找包含 Tweet 路径的 <a> 标签
                    link_element = article.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
                    href = link_element.get_attribute("href")  # 获取 href 属性值
                    tweet_id = href.split("/")[-1]  # 提取 Tweet ID
                    data["url"] = f"https://x.com/{data['author']}/status/{tweet_id}"  # 构建 Tweet URL
                except Exception as e:
                    print(f"Error extracting tweet URL: {e}")
                    data["url"] = "Unknown"

                if id not in id_set:
                    id_set.append(id)
                    self.tweets_data_list.append(data)
                    last_write_time = time.time()
                    current_count += 1
            
            if current_count >= target_count:
                break
            
            if current_time - last_write_time > timeout:
                flag = 1
            if flag == 1:
                break

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )

            body = self.driver.find_element(By.TAG_NAME, "body")
            if body:
                try:
                    # body.send_keys(Keys.PAGE_DOWN)
                    self.driver.execute_script(
                        "window.scrollTo(0,  document.body.scrollHeight);"
                    )
                    time.sleep(4)
                    
                except Exception as e:
                    # body.send_keys(Keys.PAGE_DOWN)
                    self.driver.execute_script(
                        "window.scrollTo(0,  document.body.scrollHeight);"
                    )
                    time.sleep(4)
            time.sleep(0.5)  


        
    def write_to_json(self)->None:
        dir = self.path
        path = dir + f"{self.keyword.replace(' ', ' - ')}_{self.start_date}_{self.end_date}.json".replace(
            " ", ""
        )

        tweets_dict = {
            f"tweet_{i + 1}": tweet_data 
            for i, tweet_data in enumerate(self.tweets_data_list)
        }
        print(f"\nWriting to json...")
        with open(path, "w", encoding="utf-8") as file:
            json.dump(tweets_dict, file, ensure_ascii=False, indent=4)
        print("Complete!!!")
     
  
    def crawl(self) -> None:

        current_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date()
        current_next_date = current_date + datetime.timedelta(days=1)
        start_date = datetime.datetime.strptime(self.start_date,  "%Y-%m-%d").date()
        end_date=datetime.datetime.strptime(self.end_date,  "%Y-%m-%d").date()
        total_days = (end_date - start_date).days + 1
         
        progress_bar_length = 50
               
        while current_date <= end_date:
                     
            email = self.email
            username = self.username
            password = self.password
            
            current_date_str = current_date.strftime("%Y-%m-%d")
            current_next_date_str = current_next_date.strftime("%Y-%m-%d")
            keyword = self.keyword

            since = "since:" + current_date_str
            until = "until:" + current_next_date_str
            search = f"{keyword} {since} {until}".replace(" ", "%20").replace(
                ":", "%3A"
            )
            url = f"https://twitter.com/search?q={search}"
                       
            self.driver.get(url)
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                        )
                    )
                )
                print(f"Trying to login...", end="\r")
                email_input = self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                )
                
                email_input.send_keys(email)
                email_input.send_keys(Keys.ENTER)

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                        )
                    )
                )

                check_user = self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                )
                check_user.send_keys(username)
                check_user.send_keys(Keys.ENTER)

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                        )
                    )
                )
                password_input = self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7",
                )
                password_input.send_keys(password)
                password_input.send_keys(Keys.ENTER)
                print(f"Login successfully", end="\r")
                time.sleep(5)
            except:
                print("Please double check your login information")
                exit()
        
            days_passed = (current_date - start_date ).days
            progress_percent = (days_passed / total_days) * 100 
            progress_bar = "#" * int(progress_percent / 100 * progress_bar_length)           
            
           
            try:
                error_element = self.driver.find_element(By.XPATH, '//span[contains(text(), "Something went wrong")]')                   
            except:
                error_element = None
                
            if error_element is not None:
                    self.error_count += 1
                    os.system('cls')
                    print(f"Something went wrong. I'll try it again... -> {self.error_count} retries")
                    print(f"Progress: [{progress_percent:.2f} %] [{progress_bar.ljust(progress_bar_length)}]", end="\r")
                    # return
                    continue
           
            

            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-testid="tweetText"]')
                )
            )
            self.get_articles(10, 15)  
                   
         
            current_date = current_next_date
            current_next_date += datetime.timedelta(days=1)
            self.error_count = 0

            # 打印进度条
            days_passed = (current_date - start_date ).days
            progress_percent = (days_passed / total_days) * 100 
            progress_bar = "#" * int(progress_percent / 100 * progress_bar_length)           
            print(f"Progress: [{progress_percent:.2f} %] [{progress_bar.ljust(progress_bar_length)}]", end="\r")


import json
import os
import time
from easy_twitter_crawler.twitter_crawler.twitter_scraper import TwitterScraper

class UserInfoScraper:
    """
    用户信息抓取器
    """
    def __init__(self, proxy, cookie, dir_path):
        self.scraper = TwitterScraper()
        self.scraper.set_proxy(proxy)
        self.scraper.default_headers["cookie"] = cookie
        self.dir_path = dir_path
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

    def scrape_user_info(self, input_filename, output_filename):
        """
        抓取用户信息
        :param input_filename: 输入 JSON 文件名
        :param output_filename: 输出 JSON 文件名
        """
        input_path = os.path.join(self.dir_path, input_filename)
        output_path = os.path.join(self.dir_path, output_filename)

        # 读取输入数据
        with open(input_path, "r", encoding="utf-8") as file:
            tweet_data = json.load(file)

        user_info_list = []
        for tweet_key, tweet_info in tweet_data.items():
            user_id = tweet_info.get("author")
            if not user_id:
                print(f"Skipping {tweet_key} due to missing user ID.")
                continue

            print(f"Fetching user info for user ID: {user_id}")
            try:
                # 抓取用户信息
                for user_info in self.scraper.user_crawler(user_id=user_id):
                    user_info_list.append(user_info)
                time.sleep(5)  # 限制请求频率
            except Exception as e:
                print(f"Error fetching user info for {user_id}: {e}")
                continue

        # 保存用户信息
        with open(output_path, "w", encoding="utf-8") as output_file:
            json.dump(user_info_list, output_file, ensure_ascii=False, indent=4)
        print(f"User info saved to {output_path}")

class CommentScraper:
    """
    评论抓取器
    """
    def __init__(self, proxy, cookie, dir_path):
        self.scraper = TwitterScraper()
        self.scraper.set_proxy(proxy)
        self.scraper.default_headers["cookie"] = cookie
        self.dir_path = dir_path
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

    def extract_tweet_ids(self, input_filename):
        """
        从 JSON 文件中提取推文 ID
        :param input_filename: 输入 JSON 文件名
        :return: 推文 ID 列表
        """
        input_path = os.path.join(self.dir_path, input_filename)
        with open(input_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        tweet_ids = []
        for key, tweet in data.items():
            try:
                url = tweet["url"]
                tweet_id = url.split("/")[-1]  # 提取 URL 中的最后一部分为 Tweet ID
                tweet_ids.append(tweet_id)
            except KeyError:
                print(f"Invalid entry in JSON: {tweet}")
        return tweet_ids

    def scrape_comments(self, input_filename, output_filename):
        """
        抓取评论信息
        :param input_filename: 输入 JSON 文件名
        :param output_filename: 输出 JSON 文件名
        """
        output_path = os.path.join(self.dir_path, output_filename)
        tweet_ids = self.extract_tweet_ids(input_filename)

        all_comments = {}  # 修改为字典形式，key 为推特 ID，value 为评论列表

        for index, tweet_id in enumerate(tweet_ids):
            print(f"Processing ({index + 1}/{len(tweet_ids)}): Tweet ID = {tweet_id}")
            try:
                # 抓取评论
                comments = list(self.scraper.comment_crawler(tweet_id, page_limit=5))
                all_comments[tweet_id] = comments  # 将评论列表存储为字典的值
                time.sleep(2)  # 限制请求频率
            except Exception as e:
                print(f"Error processing Tweet ID {tweet_id}: {e}")
                all_comments[tweet_id] = []  # 如果抓取失败，存储一个空列表
                continue

        # 保存评论数据
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(all_comments, file, ensure_ascii=False, indent=4)
        print(f"Comments saved to {output_path}")

import os

if __name__ == "__main__":
    


    Keyword = "liziqi"              # 搜索关键词
    Start_date = "2024-11-13"       # 开始日期
    End_date = "2024-11-16"         # 结束日期
    Email = "okita.kaslana.kiyamitsu@gmail.com"                      # 推特账号邮箱
    Username = "puliuru_luciano"                   # 推特账号@之后的名字
    Password = "Lyy-1998118214"                   # 推特账号密码
    cookie = 'night_mode=2; kdt=1Nhh2JnEJ62SNyK1hbC8bPpwA33HwQgrBaraQjby; dnt=1; guest_id=v1%3A173168018594959237; guest_id_marketing=v1%3A173168018594959237; guest_id_ads=v1%3A173168018594959237; g_state={"i_l":0}; auth_token=5169a2e3b265fdeeeab9e0736276b6c55146fb25; ct0=e7c7fe2e4029bd163a2802c0e1452166d772e191cf28e66b2657b612a15fb2a9108adc4312a1e9686eebd050489f0aecaaa8a6c601a5f3e187e725b1d6c0a3efc4290ac9b82bac468736578aa9049834; att=1-UTrlqm3CdggDMd01kvdHPvxEaYrLboILP5x41c7B; twid=u%3D1705144227460685824; personalization_id="v1_M5dSxujbPb8sgLtW81T2Zw=="; lang=en; _twitter_sess=BAh7BiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7AA%253D%253D--1164b91ac812d853b877e93ddb612b7471bebc74'                     # 替换为你的 Cookie

    # 设置代理
    proxy = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }

                
    dir_path = "./new_tweets/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path) 

    tweet_file = f"{Keyword.replace(' ', ' - ')}_{Start_date}_{End_date}.json".replace(" ", "")
    user_info_file = f"{Keyword.replace(' ', ' - ')}_{Start_date}_{End_date}_user_info.json".replace(" ", "")
    comments_file = f"{Keyword.replace(' ', ' - ')}_{Start_date}_{End_date}_comments.json".replace(" ", "")


    # from twitter_crawl_tools import crawler

    x_crawler = crawler(
        keyword=Keyword,
        start_date=Start_date,
        end_date=End_date,
        email = Email,
        username = Username,
        password = Password,
        path=dir_path,
        debug=False # This means a headless browser will be used.
    )
    x_crawler.crawl() 
    x_crawler.write_to_json()
    x_crawler.driver.quit()

    
    # 初始化用户信息抓取器
    user_scraper = UserInfoScraper(proxy, cookie, dir_path)

    # 抓取用户信息
    user_scraper.scrape_user_info(
        input_filename=tweet_file,
        output_filename=user_info_file
    )


    # 初始化评论抓取器
    comment_scraper = CommentScraper(proxy, cookie, dir_path)

    # 抓取评论
    comment_scraper.scrape_comments(
        input_filename=tweet_file,
        output_filename=comments_file
    )

    print("所有数据抓取完成。")