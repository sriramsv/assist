"""
SBU California == 3798544
Shubhada == 384159
Neeraj == 703008
Carlyle == 3247435
9nirmit9 == 2901708
Sriram == 3471404
Pavan == 3471405
Mondrita == 1575995
9nirmit9 == 2901708"""

DICT_ID = {

	'nirmit' : 2901708,
	'shubhada' : 384159,
	'carlyle' : 3247435,
	'sriram' : 3471404,
	'pavan' : 3471405
}

def getSplitwiseId(name):
	if not name:
		print "Name cannot be empty"
		exit()
	return DICT_ID[name.lower()]
