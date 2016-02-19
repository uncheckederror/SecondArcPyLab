from bs4 import BeautifulSoup
from urllib2 import urlopen


base_url = ("https://www.zagat.com/l/seattle/seattles-10-best-burgers")
soup = BeautifulSoup(urlopen(base_url).read(), "lxml")

text = []
for line in soup("a"):
    container = []
    container.append(str(line.get('href')))
    for i in container:
        if "maps.google.com" in i:
            text.append(i)
    
    
for i in text:
    print "Location link: " + i   
    
mapString = ""
for line in soup("img"):
    container = []
    container.append(str(line.get('src')))
    for i in container:
        if "maps" in i:
            mapString = i

print "Map String: " + mapString  

maplist = mapString.split("&")
latandlong = []

for i in maplist:
    if "markers=" in i:
        j = i.split("=")
        latandlong.append(j[1])

print latandlong

latitude = []
longitude = []

for i in latandlong:
    print i
    j = i.split(',')
    latitude.append(j[0])
    longitude.append(j[1])

print latitude
print longitude

print soup("a", class_="mobile-title")

BurgerPlaces = []

for text in soup("a", class_="mobile-title"):
    BurgerPlaces.append(text.get_text())

print BurgerPlaces
num = 0
for i in BurgerPlaces:
    print str(i) + ": " + str(latitude[num]) + ", " + str(longitude[num])
    num = num + 1
