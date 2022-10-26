import openai
from bs4 import BeautifulSoup
import requests
import random
from config import KeyMaster

def get_yahoo_article(site='https://news.yahoo.com/us-now-just-25-days-160000619.html'):
    req = requests.get(site)
    soup = BeautifulSoup(req.content, 'html.parser')
    article = soup.find('div', {'class':'caas-body'})

    para = article.find_all('p')
    body = ''
    for p in para[:-1]:
        body += p.text + '\n'

    return body

def get_featured_articles(yahoo_url='https://news.yahoo.com/'):
    home = requests.get(yahoo_url)
    soup = BeautifulSoup(home.content, 'html.parser')

    main_section = soup.find('div', {'id':'item-0'})

    links = []
    for a in main_section.find_all('a'):
        links.append(yahoo_url + a['href'])

    bodies = []
    for url in links:
        bodies.append(get_yahoo_article(url))

    return (bodies, links)

def showPaperSummary(paperContent):

    openai.api_key = KeyMaster.gpt3key
    response = openai.Completion.create(engine="ada",prompt=paperContent,temperature=0.3,
        max_tokens=140,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    return response["choices"][0]["text"]

def fakeSummary():
    return f'Example summary output here {random.randint(0,100)}'

def main():
    articles, links = get_featured_articles()
    #print(articles[0])

    bites = []
    for article, link in zip(articles, links):
        try:
            output = showPaperSummary(article) # comment out to not use GPT-3 and uncomment next line
            #output = fakeSummary()
            bites.append(output)
        except:
            bites.append(link)
    
    return (bites, links)

if __name__ == '__main__':
    main()