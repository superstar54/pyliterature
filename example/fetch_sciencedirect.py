from pyliterature import Pyliterature
url = 'http://www.sciencedirect.com/science/article/pii/S1751616116301138'
keyword = 'CALPHAD'

liter = Pyliterature(url, keyword)
liter.parser()

print('=================key sentences==================================')
for keysent in liter.keysents:
    print(keysent)
    print('\n')