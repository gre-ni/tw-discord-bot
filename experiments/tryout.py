from bs4 import BeautifulSoup
import requests

r = requests.get("https://app.thestorygraph.com/books/ac3ea915-993d-4f30-8632-0f91e4ad0704")
with open("sample.html", "w") as f:
    f.write(r.text)