# selenium web scraper app

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

TWITTER_CHARS = 280

def splitChars(word):
    return list(word)

PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# wikipedia main page
driver.get("https://en.wikipedia.org/wiki/Main_Page")
print(driver.title)

# find Random article list item
# return article title
randomArticle = driver.find_element_by_link_text("Random article")
randomArticle.send_keys(Keys.RETURN)
firstHeading = driver.find_element_by_id("firstHeading")
# deduct # of chars from wiki title from # of available chars to tweet
TWITTER_CHARS = TWITTER_CHARS - len(firstHeading.text)
print(firstHeading.text)

# find first paragraph
mwParserOutput = driver.find_element_by_class_name("mw-parser-output")
pTag = driver.find_element_by_tag_name("p")
articleContent = str(pTag.text)
articleList = splitChars(articleContent)

# wiki link & deduct length of link from # of available chars to tweet
permLink = str(driver.current_url)
TWITTER_CHARS = TWITTER_CHARS - len(permLink)

# print wiki article with space left for tweet
articleListSmaller = articleList[:(TWITTER_CHARS - 15)]
articleStr = ''.join(articleList)
print(articleStr, end ="")
print("...")
readMore = "Read more: "
print(readMore + permLink)

driver.quit()
