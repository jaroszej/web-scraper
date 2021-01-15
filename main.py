# python imports 
import time
import schedule

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# tweepy imports
import tweepy
from auth import Authorization

def splitChars(word):
    return list(word)

def scrapeWiki():
    authKeys = Authorization()

    auth = tweepy.OAuthHandler(authKeys.consumer_token, authKeys.consumer_secret)
    auth.set_access_token(authKeys.access_token, authKeys.access_token_secret)

    api = tweepy.API(auth)

    # twitter allows 280 characters in a tweet, 40 reserved for buffer
    TWITTER_CHARS = 240

    PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    # wikipedia main page
    driver.get("https://en.wikipedia.org/wiki/Main_Page")
    wikiTitle = str(driver.title)

    # find Random article list item
    # return article title
    randomArticle = driver.find_element_by_link_text("Random article")
    randomArticle.send_keys(Keys.RETURN)
    firstHeading = driver.find_element_by_id("firstHeading")
    # deduct # of chars from wiki title from # of available chars to tweet
    wikiHeading = str(firstHeading.text)
    TWITTER_CHARS = (TWITTER_CHARS - len(wikiHeading))
    print(wikiHeading + "\n")

    # find first paragraph
    mwParserOutput = driver.find_element_by_class_name("mw-parser-output")
    pTag = driver.find_element_by_tag_name("p")
    articleContent = str(pTag.text)
    articleList = splitChars(articleContent)

    # wiki link & deduct length of link from # of available chars to tweet
    permLink = str(driver.current_url)
    TWITTER_CHARS = TWITTER_CHARS - len(permLink)
    print(str(TWITTER_CHARS) + " available characters to tweet with\n")

    # wiki article
    articleListSmaller = articleList[:(TWITTER_CHARS)]
    articleStr = ''.join(articleListSmaller)
    elipse = "..."
    wikiArticle = articleStr + elipse
    readMore = "Read more:"

    driver.quit()

    # formats tweet
    with open('temptweet.txt', 'w', encoding="utf-8") as f:
        f.write(wikiHeading + '\n\n' + wikiArticle + '\n' + readMore + '\n' + permLink)

    print(f.read)

    # sends tweet
    with open('temptweet.txt', 'r') as f:
        api.update_status(f.read())

    print("Sent " + wikiHeading + " Wikipedia article as a tweet. . .")

# send a tweet every 4 hours
schedule.every(4).hours.do(scrapeWiki)

while True:
    schedule.run_pending()
    time.sleep(1)
