#This uses BeautifulSoup, the foundation for the DOM-searching part of Pattern
#I personally don't like the way Pattern implements BeautifulSoup, and prefer the original.  
#Get BeautifulSoup by running "pip install beautifulsoup4".  If you don't have pip, get it.

import sys
import urllib2
from pattern.web import URL, DOM, plaintext, strip_tags
from bs4 import BeautifulSoup

#This class will be replaced by database entry, but exists as a placeholder/proof-of-concept
class lab:
   def __init__(self):
      self.name=''
      self.email=''
      self.website=''
      self.title=''
      self.descrip=''
labs=[]     
      
#Gets all faculty page URLs
LINKS=[]
page = urllib2.urlopen('https://www.mcb.harvard.edu/mcb/faculty/profile-listing').read()
outersoup=BeautifulSoup(page)
for site in outersoup.find_all('a'):
   if "mcb/faculty/profile/" in str(site) and ("https://www.mcb.harvard.edu"+str(site.get('href'))) not in LINKS:
      LINKS.append("https://www.mcb.harvard.edu"+str(site.get('href')))
      



for link in LINKS:
   #Using a list of class instances in lieu of a database for now
   entry=lab()
   #Opens Page
   page = urllib2.urlopen(link).read()
   innersoup=BeautifulSoup(page)
   #Gets name and e-mail address
   entry.name=innersoup.h2.get_text(strip=True)
   entry.email=innersoup.find_all(class_="psrch_mlink2")[0].get_text(strip=True)
   #Gets lab description.  Long to deal with inconsistencies.
   for site in innersoup.find_all('a'):
      if ("Lab Website" in str(site)) or ("Lab Homepage" in str(site)):
         entry.website=str(site.get("href"))
   for tag in innersoup.find_all('h3'):
      if "Research" in str(tag):
         for sibling in tag.next_siblings:
            if "<p>" in str(sibling):
               if not any("<" in str(unicode(x).encode('ascii', 'ignore')) for x in sibling.contents):
                  entry.descrip=entry.descrip+"\n"+str(unicode(sibling.contents[0]).encode('ascii', 'ignore'))
               for paragraph in sibling.find_all('p'):
                  if not paragraph.b:
                     entry.descrip=entry.descrip+"\n"+str(unicode(paragraph.get_text()).encode('ascii', 'ignore')) #Harvard profs don't understand Unicode
                     
   #Adds the scraped results to the list of class instances
   labs.append(entry)



#Proof-of-concept:   
output=open("mcblabs.txt", 'w')   
for thelab in labs:
   output.writelines(thelab.name+"\n"+thelab.email+"\n"+thelab.website+"\n"+thelab.title+"\n"+thelab.descrip+"\n\n") 
output.close()
