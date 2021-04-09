from bs4 import BeautifulSoup
import requests
import time

print('Enter Skill that you are aware of (space separated):')
known_skills = input('>')
known_skills = known_skills.replace(' ', '+')
print('Enter Skill that you arent aware of:')
not_known_skills = input('>')
global shut_program
shut_program = False


def getScraped(currentPage):
    url = str.format(
        f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords={known_skills}&searchBy=0'
        f'&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords={known_skills}&pDate=I'
        f'&sequence={currentPage}&startPage=1')
    url = url.format(known_skills=known_skills, currentPage=currentPage)
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    if len(jobs) == 0:
        global shut_program
        shut_program = True
    for job in jobs:
        published_date = job.find('span', class_='sim-posted').text.strip()
        skills = job.find('span', class_='srp-skills').text.replace(' ', '').strip()
        if ('1' in published_date) and (not_known_skills not in skills):
            company_name = job.find('h3', class_='joblist-comp-name').text.replace('(More Jobs)', '').strip()
            more_info = job.header.h2.a['href']
            print(
                f"Company Name : {company_name}\nRequired Skills: {skills}\nPublished Date: {published_date}\nClick "
                f"here for more info: {more_info}\n\n")


if __name__ == '__main__':
    current = 1
    print('------------------- Welcome to Times Jobs Scrapper ----------------------\n')
    while not shut_program:
        getScraped(current)
        time_wait = 1
        print("\n---------------Waiting---------------")
        current = current + 1
        time.sleep(5)
