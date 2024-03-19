from bs4 import BeautifulSoup
from selenium import webdriver
import time
from collections import deque
import csv

driver=webdriver.Chrome()

total = 0

visited = []
def scrape(target):
    global total
    target_url = f"https://twitter.com{target}"
    visited.append(target)
    driver.get(target_url)
    time.sleep(5)
    t = {}
    flag = 25
    prev_len = 0
    with open('data2.csv', 'a',newline="",  encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        for i in range(150):

            driver.execute_script("window.scrollBy(0, 600)")
            resp = driver.page_source

            soup=BeautifulSoup(resp,'html.parser')
            l = []
            try:
                l = soup.find_all("div", {"class":"css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"})
            except:
                pass
            for i in l:
                try:
                    o = {}
                    reply_el = i.find("div", {"data-testid":"reply"})
                    replies = reply_el.get("aria-label").split()[0]
                    like_el = i.find("div", {"data-testid":"like"})
                    likes = like_el.get("aria-label").split()[0]
                    retweet_el = i.find("div", {"data-testid":"retweet"})
                    retweets= retweet_el.get("aria-label").split()[0]
                    t_parent = i.find("div", {"class":"css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim"})
                    tweet_el = t_parent.contents
                    o["tweet"] = tweet_el[0].text
                    o["replies"] = replies
                    o["retweets"] = retweets
                    o["likes"] = likes
                    t[hash(tweet_el[0].text)] = o
                    writer.writerow(o.values())
                    # print(t[hash(tweet_el[0].text)])
                    print(f"no. of tweets = {len(t)}    ||| TOTAL {total}")
                    
                    if(len(t)!= prev_len):
                        flag = 25
                    else:
                        flag-=1
                    prev_len = len(t)
                    # print(flag)
                    if(flag <= 0):
                        total += len(t)
                        driver.execute_script("window.scrollTo(0,-60000)")
                        return

                except AttributeError:
                    pass
    total += len(t)
    driver.execute_script("window.scrollBy(0,-60000)")

# scrape("/ICC")
potential_targets = deque()
    

def updateTargets():
    time.sleep(5)
    resp = driver.page_source
    soup=BeautifulSoup(resp,'html.parser')
    wtf = soup.find_all("aside",{"aria-label": "Who to follow"})
    links = wtf[0].find_all("a", {"role":"link"})[:-1]  #Sliced for the show more
    for i in links:
        targName = i.get("href")
        if targName not in potential_targets and targName not in visited:
            potential_targets.append(targName)
    # print(potential_targets)


scrape("/nike")
updateTargets()

while total < 5000:
    print(visited)
    print(potential_targets)
    curr_target = potential_targets.pop()
    if(curr_target not in visited):
        scrape(curr_target)
    updateTargets()



# username
# retweets
# likes
# views
# tweet
#css-1qaijid r-bcqeeo r-qvutc0 r-poiln3
driver.close()

# print(resp)

