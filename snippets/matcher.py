def matcher(textline):
	import re
	import csv
	with open('data/only100latest.csv') as csvfile:
		regexdata = csv.reader(csvfile, strict=True)
		for i in regexdata:
			if re.match(i[3], textline) is not None:
				return i[2]
			return	None		 

	
	
