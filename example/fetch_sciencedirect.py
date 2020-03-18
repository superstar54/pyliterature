from pyliterature import Pyliterature
url = 'http://www.sciencedirect.com/science/article/pii/S1751616116301138'
keyword = 'CALPHAD'

liter = Pyliterature(url, keyword)
# load text from url html and parse the sentences including keyword
liter.parser()

print('=================article text==================================')
# print(liter.text)

print('=================key sentences==================================')
for keysent in liter.keysents:
    print(keysent)
    print('\n')