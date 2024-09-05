from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
# Create your views here.

def get_html_content(city):

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session=requests.Session()
    session.headers['User-Agent']=user_agent
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city=city.replace(' ','+')
    html_content=session.get(f'https://www.google.com/search?q=weather+of+{city}&hl=en').text
    # print(html_content)
    return html_content
def home(request):
    weather_data = {}

    if 'city' in request.GET:
        city=request.GET.get('city')
        html_content=get_html_content(city)
        soup=BeautifulSoup(html_content,'html.parser')
        # print(soup.prettify())
        weather_data=dict()
        weather_data['span'] = soup.find('span',class_='BBwThe').text
        weather_data['temp']= soup.find('span',class_='wob_t q8U8x').text
        weather_data['day']= soup.find('div',attrs={'id':'wob_dts'}).text
        weather_data['sky']= soup.find('span',attrs={'id':'wob_dc'}).text
        weather_data['Precipitation']= soup.find('span',attrs={'id':'wob_pp'}).text
        weather_data['Humidity']= soup.find('span',attrs={'id':'wob_hm'}).text
        weather_data['Wind']= soup.find('span',attrs={'id':'wob_ws'}).text
        img=soup.find('img',id='wob_tci')
        if img:
            img_scr=img['src']
            img_url='https:'+ img_scr
            weather_data['url']=img_url
            
        # city_text=span.get_text()
        print(weather_data)


        pass
    return render(request,'index.html',{'weather':weather_data})
    