from utils.Http import Http

http = Http()
rs = http.get('https://www.amazon.com/dp/B07214SKYV')
print(rs.text)
