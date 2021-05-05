import requests
r = requests.get('https://search.cctv.com/index.php')
print(r.url)