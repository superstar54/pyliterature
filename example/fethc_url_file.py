from pyliterature import Pyliterature

urls = []
file = open('urls.dat')
lines = file.readlines()
for line in lines:
    urls.append(line)

keyword = 'DFT'
liter = Pyliterature()
for url in urls:
	liter.url = url
	print(url + '\n\n')
	liter.parser()
#
liter.url = None
liter.keyword = keyword
# print(liter.text)
liter.parser()
print('===================================================')
for keysent in liter.keysents:
    print(keysent)
    print('\n')