import requests
from bs4 import BeautifulSoup
import pandas
import time

pageOneURL = "https://www.bdh-online.de/patienten/therapeutensuche/"
pageTwoURL = pageOneURL + "?seite=2"
people = []

def ReceiveHTMLFile(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  return soup


def ScrapPeople(url, people):
  soup = ReceiveHTMLFile(url)
  soup.find("tr").decompose()
  table = soup.select(".search_list>table>tr")
  for row in table:
    personURL = row.find_all("a")[-1].get("href")
    zip = row.find_all("td")[2].getText()
    ort = row.find_all("td")[3].getText()
    personSoup = ReceiveHTMLFile(personURL)
    personData = personSoup.select("#therapeuten>div:nth-child(2)>div>div>div:last-child")
    fullName = personData[0].find("b").getText().split()
    firstName = fullName[0]
    lastName = fullName[1]
    if len(fullName) == 3:
      lastName += ", " + fullName[2]
    emailRaw = personData[0].find("table").getText()
    email = emailRaw[emailRaw.find("E-Mail") + 6:]
    people.append([firstName, lastName, zip, ort, email])
      
  

ScrapPeople(pageOneURL, people)
ScrapPeople(pageTwoURL, people)

df = pandas.DataFrame(people, columns=["First Name", "Last Name", "PLZ", "Ort", "Email"])
df.to_csv('peopleScraped.csv')