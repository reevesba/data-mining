# Coverts html to XML
import codecs
import json
import html2text
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# first import the html as a string
html = codecs.open("dat/tan-output.html", "r")

soup = BeautifulSoup(html, "html.parser")

# experiementing with soup
ul = soup.find("ul")
#print(soup.prettify(str(ul)))
#print(ul)

# find the first node
root = str(html).find("<UL>")
print(str(html))


#contents = ul.contents
#print(contents)

# create the file structure
#data = ET.Element("data")

#i = 0
#for child in ul.children:
    #print("Child" + str(i) + ": " + str(child))
    #i = i + 1

#item1 = ET.SubElement(ul, 'item')
#item2 = ET.SubElement(ul, 'item')

#item1.set('name','item1')
#item2.set('name','item2')
#item1.text = 'item1abc'
#item2.text = 'item2abc'

# create a new XML file with the results
#mydata = ET.tostring(data)
#myfile = open("items2.xml", "wb")
#myfile.write(mydata)
