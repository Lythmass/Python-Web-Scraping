import requests
from bs4 import BeautifulSoup
import pandas
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

pageOneURL = "https://www.bdh-online.de/patienten/therapeutensuche/"
pageTwoURL = pageOneURL + "?seite=2"
people = []
client = OpenAI()

def ReceiveHTMLFile(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  return soup

def SplitThePersonName(fullName):
  firstName = fullName[0]
  lastName = fullName[1]
  if len(fullName) == 3:
    lastName += ", " + fullName[2]
  return firstName, lastName

def DetermineGender(firstName):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You determine the gender from names from all countries. Your output answer should ONLY be either 'f' or 'm'. Don't give me any other answer."},
      {"role": "user", "content": "What gender is the name '" + firstName + "' associated to?"},
    ]
  )
  return response.choices[0].message.content

def ScrapPeople(url, people):
  soup = ReceiveHTMLFile(url)
  soup.find("tr").decompose() #Delete the first head row
  table = soup.select(".search_list>table>tr")
  for row in table:
    personURL = row.find_all("a")[-1].get("href")
    zip = row.find_all("td")[2].getText()
    ort = row.find_all("td")[3].getText()
    personSoup = ReceiveHTMLFile(personURL)
    personData = personSoup.select("#therapeuten>div:nth-child(2)>div>div>div:last-child")
    firstName, lastName = SplitThePersonName(personData[0].find("b").getText().split())
    emailRaw = personData[0].find("table").getText()
    email = emailRaw[emailRaw.find("E-Mail") + 6:]
    gender = DetermineGender(firstName)
    people.append([firstName, lastName, gender, zip, ort, email])
      
  

ScrapPeople(pageOneURL, people)
ScrapPeople(pageTwoURL, people)

df = pandas.DataFrame(people, columns=["First Name", "Last Name", "Gender", "PLZ", "Ort", "Email"])
df.to_excel('peopleScraped.xlsx')