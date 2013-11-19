# 2013-11-13
# Robin Camille Davis

# This script associates John Jay-affiliated authors from Scopus with the index keywords
# as assigned by Scopus. Authors and keywords are nodes with attributes Type (FacultyName, IndexKeyword)
# and Occurrence (how often each shows up).

# The data is limited to science and social science publications, as indexed by Scopus.
# Scopus CSV should be structured as Authors,Year,Link,Affiliations,Authors with affiliations,Index Keywords
# or else you'll need to edit row counts.

from csv import reader

data = reader(open('scopus-auth-indexkeyword-affil-only.csv')) #file called twice = see below

outfile = open("scopus-auth-indexkeyword-affil-JJonly_1118_2.gexf","w")
outfile.write('<?xml version="1.0" encoding="UTF-8"?> \
<gexf xmlns="http://www.gexf.net/1.1draft" version="1.1" xmlns:viz="http://www.gexf.net/1.1draft/viz" \
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.1draft \
http://www.gexf.net/1.1draft/gexf.xsd">\
<meta lastmodifieddate="2013-11-18">\n\
<creator>Robin Davis</creator>\n\
<description>github.com/robincamille</description>\n</meta> \n \
<graph>\n \
<attributes class="node" mode="static"> \n\
<attribute id="attr_type" title="Type" type="string"></attribute>\n \
<attribute id="global_occurrences" title="Occurrences Count" type="integer"></attribute>\n \
</attributes>\n<nodes\n>')

idcounter = 0
keywordlist = []
namelist = []

print 'Indexing John Jay-affiliated authors and keywords of their publications'

for row in data: #this indexes faculty names and Scopus keywords
    affil = row[4].split('; ') #double-check the columns in your exported Scopus CSV
    indexkey = row[5].split('; ')
    
    for s in affil: #names in 'affiliation' column
        if 'John Jay College' in s: #some are short title only
            name = s.split(',') 
            jjname = name[1] + ' ' + name[0]
            jjname = jjname[1:]
            namelist.append(jjname)
            #print jjname
        else:
            pass
        
    for s in indexkey:  #index keyword
        if s == "":
            pass
        else:
            keywordlist.append(s)


print 'Listing each faculty member as a node'           

namecountlist = [] #count occurrence of faculty names, list as node once
for name in namelist:
    if name in namecountlist:
        pass
    else: #write all faculty names as nodes
        namecountlist.append(name)
        namecounter = namelist.count(name) + 1
        outfile.write('<node id="' + name + '" label="' + name + '">\n<attvalues> \n \
<attvalue for="attr_type" value="FacultyName" />\n\
<attvalue for="global_occurrences" value="' + str(namecounter) + '" />\
</attvalues>\n</node>' + '\n')

print 'Listing each keyword as a node'

keywordcountlist = [] #count occurrence of keyword, list as node once
for key in keywordlist:
    key = key.lower()
    if key in keywordcountlist:
        pass
    else: #write all index keys as nodes
        keywordcountlist.append(key)
        keycounter = keywordlist.count(key) + 1
        outfile.write('<node id="' + key + '" label="' + key + '">\n<attvalues> \n \
<attvalue for="attr_type" value="IndexKeyword" />\n \
<attvalue for="global_occurrences" value="' + str(keycounter) + '" />\
\n</attvalues>\n</node>\n \n')


outfile.write('</nodes>\n \n <edges>\n')


data = reader(open('scopus-auth-indexkeyword-affil-only.csv')) #start at top


print 'Printing faculty names and indexed keywords as edges to file'

    
for row in data:
    affil = row[4].split('; ')
    indexkey = row[5].split('; ')
    for s in affil:
        if 'John Jay College' in s: #some are short title only
            name = s.split(',') 
            jjname = name[1] + ' ' + name[0]
            jjname = jjname[1:]
            for key in indexkey:
                if key == "": #if keyword not blank
                    pass
                else:
                    #print jjname, key
                    idcounter = idcounter + 1
                    key = key.lower()
                    outfile.write('<edge id="' + str(idcounter) + '" ' + 'source="' + jjname + '" target="' + key + '"></edge>' + '\n')
            
        else:
            pass



outfile.write('</edges>\n</graph>\n</gexf>')
outfile.close()
print "Done \n\nYour file has been written to %s" %(outfile)
