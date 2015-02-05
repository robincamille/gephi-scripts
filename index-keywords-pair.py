#!/usr/bin/env python
# -*- coding: utf-8 -*-

#scopus keywords
#see http://emerging.commons.gc.cuny.edu/2015/02/create-topic-map-institutions-publications-gephi for context

import itertools

infile = open('all-index-keywords-list.txt','r') #your file here
data = infile.readlines()
infile.close()

outfile = open('all-index-keywords_for-gephi.csv','w')

conn = [] #final connected keywords list)

for l in data:
    conni = [] #connected keywords for each article
    l = l.split('; ')
    c = itertools.combinations(l, 2) #connect keywords to others, 2 at a time
    for s in c:
        conni.append(s)
    conn.append(conni)

for ind in conn:
    for c in ind:
        line = c[0] + '\t' + c[1] + '\n'
        outfile.write(line)

print 'Done'
outfile.close
