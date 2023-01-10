#this is absolutely useless 



import random
import requests
from bs4 import BeautifulSoup

def quizlet_scraper(url):
  dict_scraped = {}
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
  soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
  for i, (question, answer) in enumerate(zip(soup.select('a.SetPageTerm-wordText'), soup.select('a.SetPageTerm-definitionText')), 1):
      dict_scraped[str(question.get_text(strip=True, separator='\n'))] = str(answer.get_text(strip=True, separator='\n'))
  return dict_scraped

idx = 0

def handle_response(message) -> str:
    p_message = str(message)
    if p_message == 'hello':
        return 'Hey there!'

    if p_message == 'roll':
        return str(random.randint(1, 6))

    if p_message == '!help':
        return "`This is a help message that you can modify.`"

    if p_message == 'quizlet':
        return "sounds good! send me a link to the flashcards and ill help you revise for them"

    if 'quizlet' in str(p_message):
        dict_with_words = quizlet_scraper(p_message)
        res_1 = list(dict_with_words.keys())
        res_2 = list(dict_with_words.values())
        return 'list has been created'
        alex = True




#i just understood why this code doesnt work, its cuz the function is called after every user message.




    #  return 'Yeah, I don\'t know. Try typing "!help".'
