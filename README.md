###pyliterature
A Pythonic wrapper for the scientific journal, including Nature, Science, ScienceDirect, Wiley, ACS publication, RSC publication and so on.



###Author
* Xing Wang  <xingwang1991@gmail.com>



###Dependencies

* Python >=26
* spynner
* BeautifulSoup
* nltk
* PyQt > 443


####Examples

```python
>>> from pyliterature import Pyliterature
>>> url = 'http://www.nature.com/nature/journal/v541/n7635/full/nature20782.html'
>>> keyword = 'DFT'
>>> liter = Pyliterature(url, keyword)
>>> liter.text
>>> liter.keysents
```

If you want to add features/improvement or report issues, feel free to send a pull request!


###TODO
* read bib list

