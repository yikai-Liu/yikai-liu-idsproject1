from fastapi import FastAPI
import uvicorn
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Financial News Crawler"}

@app.get("/crawl/{source_name}/{company_name}/{num_news}")
async def crawl(source_name: str, company_name: str, num_news: int):
    companies = []
    sources = source_name.split(",")
    companies = company_name.split(",")
    news = scrape(sources, companies, num_news)
    return {"news": news}



def scrape(sources, companies, number):
    number = int(number)
    all_result = []
    result = {}


    if "Forbes" in sources:
        for query in companies:
            website = "https://www.forbes.com/search/?q="
            URL = website + query
            source = requests.get(URL).text
            soup = BeautifulSoup(source, 'html5lib')
            article = soup.find_all('div', class_= "stream-item__text")[:number]
            for stream_text in article:
                try:
                    result = {}
                    result["company"] = query
                    result["source"] = 'Forbes'
                    headline = stream_text.h3.a.text
                    result["headline"] = headline
                    # print(headline)
                    url = stream_text.h3.a["href"]
                    result["url"] = url
                    # print(url)
                    date = stream_text.find('div', class_="stream-item__date").text
                    result['date'] = date
                    # print(date)
                    summary = stream_text.find('div', class_="stream-item__description").text
                    result['summary'] = summary
                    # print(summary)
                    all_result.append(result)
                except:
                    pass
    
    if "TheNewYorker" in sources:
        for query in companies:
            website = "https://www.newyorker.com/search/q/"
            URL = website + query
            source = requests.get(URL).text  
            soup = BeautifulSoup(source, 'html5lib')
            article = soup.find_all('li', class_="River__riverItem___3huWr")[:number]
            for stream_text in article:
                try:
                    result = {}
                    result["company"] = query
                    headline = stream_text.find('h4', class_="River__hed___re6RP").text
                    result["source"] = 'The New Yorker'
                    result["headline"] = headline
                    url= stream_text.findAll('a')[2]["href"]
                    url = "https://www.newyorker" + url
                    result["url"] = url
                    summary = stream_text.find('h5',class_="River__dek___CayIg").text
                    result["summary"] = summary
                    date = stream_text.find('h6', class_="River__publishDate___1fSSK").text
                    result["date"] = date
                    all_result.append(result)
                except:
                    pass

    if "TheNewYorkTimes" in sources:
        for query in companies:
            website = "https://www.nytimes.com/search?query="
            website_url = "https://www.nytimes.com"
            URL = website + query
            source = requests.get(URL).text
            soup = BeautifulSoup(source, 'html5lib')
            articles = soup.find_all('div', class_ = 'css-1bdu3ax')[:number]
            for article in articles:
                try:
                    result = {}
                    result["company"] = query
                    result['source'] = 'The New York Times'
                    headline = article.h4.text
                    result["headline"] = headline
                    # print(headline)
                    url = website_url + article.a["href"]
                    result["url"] = url
                    # print(url)
                    # date = article.find('span').text
                    # result["date"] = date
                    # print(date)
                    summary = article.find('p', class_="css-16nhkrn").text
                    result["summary"] = summary
                    # print(summary)
                    all_result.append(result)
                except:
                    pass
    return all_result

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
