# Python Web Scraping

A Python app that crawls on the website, gets their data, determines the gender using AI and then exports the data as CSV.

## Lessons Learned

The working process for this project was enjoyable, because I learned how to use the powerful tool for crawling the web pages (Beautiful Soup) and the very interesting tool known as OpenAI API.

## Features
- Crawl the following website: https://www.bdh-online.de/patienten/therapeutensuche/
- Scrap the first name, last name, email, zip code and city from the first 2 pages of people.
- Determine the gender of the person using their name with the help of OpenAI API.
- Create the data table
- Export the data as CSV


## Environment Variables

To run this project, you will need to add the only environment variable to your .env file
`OPENAI_API_KEY`


## Used Packages
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) - For parsing the webpage as HTML
- [Requests](https://pypi.org/project/requests/) - For making Requests
- [Pandas](https://pandas.pydata.org/) - For exporting data as CSV
- [Dotenv](https://pypi.org/project/python-dotenv/) - For loading the .env file
- [OpenAI](https://platform.openai.com/docs/quickstart?context=python) - For determining the gender