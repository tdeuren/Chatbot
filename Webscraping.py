import requests as rq
import bs4

def getweathertoday():
    r = rq.get('https://www.bbc.com/weather/2800866')
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    temp = soup.find_all('span', {"class": "wr-value--temperature--c"})[0].get_text()
    print("\t\tToday's temperature: %s" %temp)

def gettimenow():
    r = rq.get('https://www.worldtimeserver.com/current_time_in_BE.aspx')
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    time = soup.find_all('span', {"id": "theTime"})[0].get_text()
    print("\t\tThe time is now: %s" %time) # time.time() would be easier
