from utils.Http import Http
from app.crawlers.Captcha import Captcha

http = Http()
rs = http.get('https://www.amazon.com/dp/B07214SKYV')

Captcha(base_url='https://www.amazon.com', html=rs.text, http=http)
rs = http.get('https://www.amazon.com/dp/B07214SKYV')
print(rs.text)

# import requests
#
# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
# }
# session = requests.session()
# session.headers = headers
# re = session.get(url='https://www.amazon.com')
# print(re.text)
# url = input()
#
# re = session.get(url)
# print(re.cookies)
#
# re = session.get(url='https://www.amazon.com')
# print(re.text)
