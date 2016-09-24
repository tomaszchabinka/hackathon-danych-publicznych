# -*- coding: utf-8 -*-
import csv
import re
atostring = "W tym celu .* powinien odesłać towar w stanie nienaruszonym.*na adres.*"
#pattern = re.match(atostring)



bebe = re.match(atostring,"W tym celu Janusz powinien odesłać towar w stanie nienaruszonym na adres ")
print bebe

if bebe is not None:
	print 'Euroeka'

'''
with open('/Users/mikolajmierzejewski/hak/hackathon-danych-publicznych/data/only100latest.csv') as csvfile:
	regexdata = csv.reader(csvfile, strict=True)
	for i in regexdata:
		pattern = re.compile(i[3], re.IGNORECASE)
'''