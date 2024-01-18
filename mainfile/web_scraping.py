import requests
from bs4 import BeautifulSoup as bs4
import json

result = requests.get('https://www.mayoclinic.org/biographies/abboud-charles-f-m-b/bio-20053030').content
soup = bs4(result, "lxml")
body = soup.find("body").text.strip()
# print(body)
data = json.loads(body)
# print(body)