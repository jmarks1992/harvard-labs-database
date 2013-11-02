#This uses BeautifulSoup, the foundation for the DOM-searching part of Pattern
#I personally don't like the way Pattern implements BeautifulSoup, and prefer the original.  
#Get BeautifulSoup by running "pip install beautifulsoup4".  If you don't have pip, get it.

import sys
import urllib2
from bs4 import BeautifulSoup, NavigableString, Tag
from pattern.web import URL, DOM, plaintext, strip_tags
import csv

labs=[]     
#Fields to fill:
fields=['PI_email', 'PI_name', 'building', 'department', 'funding_sources', 'lab_desc', 'lab_location', 'lab_name', 'lab_url', 'n_members', 'pubmed_name', 'tags']
#Gets all faculty page URLs
LINKS=[]
page = urllib2.urlopen('https://www.mcb.harvard.edu/mcb/faculty/profile-listing').read()
outersoup=BeautifulSoup(page)
for site in outersoup.find_all('a'):
   if "mcb/faculty/profile/" in str(site) and ("https://www.mcb.harvard.edu"+str(site.get('href'))) not in LINKS:
      LINKS.append("https://www.mcb.harvard.edu"+str(site.get('href')))
      



for link in LINKS:
   #Storing things in a dict for easy CSV writing
   entry={}
   entry["department"]="Molecular and Cellular Biology"
   entry["lab_desc"]="\""
   entry["lab_url"]=""
   #Opens Page
   page = urllib2.urlopen(link).read()
   innersoup=BeautifulSoup(page)
   #Gets name and e-mail address
   entry["PI_name"]=innersoup.h2.get_text(strip=True)
   entry["PI_email"]=innersoup.find_all(class_="psrch_mlink2")[0].get_text(strip=True)
   #Gets lab description.  Long to deal with inconsistencies.
   for site in innersoup.find_all('a'):
      if ("Lab Website" in str(site)) or ("Lab Homepage" in str(site)):
         entry["lab_url"]=str(site.get("href"))
   for tag in innersoup.find_all('h3'):
      if "Research" in str(tag):
         for sibling in tag.next_siblings:
            if "<p>" in str(sibling):
               if not any("<" in str(unicode(x).encode('ascii', 'ignore')) for x in sibling.contents):
                  entry["lab_desc"]=entry["lab_desc"]+str(unicode(sibling.contents[0]).encode('ascii', 'ignore'))+"\n"
               for paragraph in sibling.find_all('p'):
                  if not paragraph.b:
                     entry["lab_desc"]=entry["lab_desc"]+str(unicode(paragraph.get_text()).encode('ascii', 'ignore'))+"\n"
                     #Harvard profs don't understand Unicode
                        
   for br in innersoup.findAll('br'):
       next = br.nextSibling
       if not (next and isinstance(next,NavigableString)):
           continue
       next2 = next.nextSibling
       if next2 and isinstance(next2,Tag) and next2.name == 'br':
           text = str(unicode(next).encode('ascii', 'ignore')).strip()
           
           if "Biological" in text or "Northwest" in text or "Sherman Fairchild" in text:#Complete lack of regularities in building names besides everyone being in the same three buildings forced me to hardcode the names :( 
               entry["building"]=text
   entry["lab_desc"]=entry["lab_desc"]+"\""
                     
   #Adds the scraped results to the list of dicts
   labs.append(entry)
   
   
#CSV's
outfile=open('mcblabs.csv', 'w')
csvwriter=csv.DictWriter(outfile, fields, dialect='excel')
csvwriter.writeheader()
for thelab in labs:
      csvwriter.writerow(thelab)
outfile.close()


#Text file (for testing):
output=open("mcblabs.txt", 'w')   
for thelab in labs:
   output.writelines(thelab["PI_name"]+"\n"+thelab["PI_email"]+"\n"+thelab["lab_url"]+"\n"+thelab["lab_desc"]+"\n\n") 
output.close()
