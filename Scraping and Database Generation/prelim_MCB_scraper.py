#This uses BeautifulSoup, the foundation for the DOM-searching part of Pattern
#I personally don't like the way Pattern implements BeautifulSoup, and prefer the original.
# -- Jonathan: funny, I greatly prefer Pattern. It lets you do things like dom('CSS selector'),
#              which can make some things really easy. completely up to you though.  
#Get BeautifulSoup by running "pip install beautifulsoup4".  If you don't have pip, get it.

import sys
import urllib2
from pattern.web import URL, DOM, plaintext, strip_tags
from bs4 import BeautifulSoup
# I'm going to add this library too. It's great -- look it up. Powerful database-like tools in python
import pandas as pd

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

# Peter, I am going to add a bit of code to convert your class into a DataFrame.
labs_df = pd.DataFrame();
for lab in labs:
   single_df = pd.DataFrame({'PI_name': lab.name, 'PI_email': lab.email, 'lab_website': lab.website, 'lab_title': lab.title, 'lab_desc': lab.desc})
   pd.concat(single_df, labs_df)

# it's really much easier to run these things as a ipython notebook. Easier to explore the data.
labs_df.head(10)

labs_df.to_csv('mcb_labs')

#Proof-of-concept:   
'''
output=open("mcblabs.txt", 'w')   
for thelab in labs:
   output.writelines(thelab.name+"\n"+thelab.email+"\n"+thelab.website+"\n"+thelab.title+"\n"+thelab.descrip+"\n\n") 
output.close()
'''
