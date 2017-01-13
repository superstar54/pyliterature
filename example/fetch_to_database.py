from pyliterature import Pyliterature
"""
load html every time is very slow, it's better to save the text we have into a database.
we can read text from the database next time.

"""
#----------------------------------------
# read old database file
keyword = 'DFT'
liter = Pyliterature()
liter.read_database(keyword)
for url in liter.url_list:
	print(url)

urls = [
    'http://science.sciencemag.org/content/355/6320/49.full', 
    'http://www.nature.com/nature/journal/v541/n7635/full/nature20782.html', 
    'http://www.sciencedirect.com/science/article/pii/S1751616116301138', 
    'http://pubs.acs.org/doi/full/10.1021/acscatal.6b02960', 
]
# find new url not in the database
urls_new = []
for url in urls:
	if url not in liter.url_list:
		urls_new.append(url)

#-----------------------------------
# load text from new url html
for url in urls_new:
	liter.url = url
	print(url + '\n\n')
	liter.parser()

# parser keyword from all text
liter.url = None
liter.keyword = keyword
liter.parser()
liter.save_database()
print('===================================================')
for keysent in liter.keysents:
    print(keysent)
    print('\n')