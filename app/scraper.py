import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time

# job_data = []
# url = "https://www.linkedin.com/jobs/search/?currentJobId=4225916174&distance=25&geoId=103644278&keywords=Data%20Analyst&origin=JOBS_HOME_KEYWORD_HISTORY&refresh=true"

# try:
#     response = requests.get(url)
#     response.raise_for_status()

#     soup = BeautifulSoup(response.content, 'html-parser')

#     job_listings = soup.find_all('h1', class='t-24 t-bold inline')
    
#     for job in job_listings:
#         try:
#             title_element = job.find('h2')

def extract(job_title):
    