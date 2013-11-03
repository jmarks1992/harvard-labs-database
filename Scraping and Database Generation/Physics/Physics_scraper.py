#This uses BeautifulSoup, the foundation for the DOM-searching part of Pattern
#I personally don't like the way Pattern implements BeautifulSoup, and prefer the original.  
#Get BeautifulSoup by running "pip install beautifulsoup4".  If you don't have pip, get it.

import sys
import urllib2
from bs4 import BeautifulSoup, NavigableString, Tag
from pattern.web import URL, DOM, plaintext, strip_tags
import csv
import re

labs=[]     
#Fields to fill:
fields=['PI_email', 'PI_name', 'building', 'department', 'funding_sources', 'lab_desc', 'lab_location', 'lab_name', 'lab_url', 'n_members', 'pubmed_name', 'tags']
#Gets all faculty page URLs
LINKS=[]
page = urllib2.urlopen('https://www.physics.harvard.edu/research/facresearch').read()
outersoup=BeautifulSoup(page)
for site in outersoup.find_all('a'):
   if "people/facpages/" in str(site) and ("https://www.physics.harvard.edu/"+str(site.get('href'))) not in LINKS:
      LINKS.append("https://www.physics.harvard.edu/"+str(site.get('href')))
      
TEST=['https://www.physics.harvard.edu/people/facpages/georgi']


for link in LINKS:
   #Storing things in a dict for easy CSV writing
   entry={}
   entry["department"]="Physics"
   entry["lab_desc"]="\""
   entry["lab_url"]=""
   entry['PI_name']=str(link)
   entry['PI_email']=str(link)
   entry['building']=""
   #Opens Page
   page = urllib2.urlopen(link).read()
   innersoup=BeautifulSoup(page)
   #Gets name and e-mail address
   namepattern=re.compile(r'[A-Z][A-Z][A-Z. ]+')
   if re.search(namepattern, innersoup.title.get_text(strip=True)):
      entry["PI_name"]=re.search(namepattern, innersoup.title.get_text(strip=True)).group()
   emailpattern=re.compile(r'[A-Za-z.]+@[A-Za-z.]+.harvard.edu')
   if re.search(emailpattern, innersoup.get_text(strip=True)):
      entry["PI_email"]=re.search(emailpattern, innersoup.get_text(strip=True)).group()
   #Gets the building
      if len(innersoup.find_all('td'))>=3:
         if re.match(r'[A-za-z-]', unicode(innersoup.find_all('td')[2].get_text(strip=True)).encode('ascii', 'ignore').split()[0]):
            entry['building']=unicode(innersoup.find_all('td')[2].get_text(strip=True)).encode('ascii', 'ignore').split()[0]
   #Gets a description
   if len(innersoup.find_all('hr'))>=2:
      print innersoup.find_all('hr')[1]
      for paragraph in innersoup.find_all('hr')[1].next_siblings:
         if paragraph.name=='p':
            entry["lab_desc"]=entry["lab_desc"]+str(unicode(paragraph.get_text()).encode('ascii', 'ignore'))+"\n"
            print paragraph
         elif paragraph.name and paragraph.name!='p':
            break
   #Adds the scraped results to the list of dicts
   labs.append(entry)
   
   
#CSV's
outfile=open('physicslabs.csv', 'w')
csvwriter=csv.DictWriter(outfile, fields, dialect='excel')
csvwriter.writeheader()
for thelab in labs:
      csvwriter.writerow(thelab)
outfile.close()


#Text file (for testing):
output=open("physicslabs.txt", 'w')   
for thelab in labs:
  output.writelines(thelab["PI_name"]+thelab["PI_email"]+thelab['building']+thelab['lab_desc']+"\n")
 #output.writelines(thelab["PI_name"]+"\n"+thelab["PI_email"]+"\n"+thelab["lab_url"]+"\n"+thelab["lab_desc"]+"\n\n") 
output.close()
