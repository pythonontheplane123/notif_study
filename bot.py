import discord
import random
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import schedule
import time
import re
from PIL import Image
import io
import os
import itertools
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}



IB_Subject_Code = [75,79,81,87,117,113,91,544,543,119,93,95,122]


IB_subject_choices = ['Biology','Chemistry','Economics','Further Mathematics','Global Politics','Mathematical Studies','Mathematics','Mathematics AA','Mathematics AI','Philosophy','Physics','Psychology','World Religions']

ib_subject_choices = [ib_subject.lower() for ib_subject in IB_subject_choices]

BASE_URL = "https://www.exam-mate.com"
URL = 'https://www.exam-mate.com/topicalpastpapers/?cat=7&subject={}&years=&seasons=&paper=&zone=&chapter=&order=asc&offset={}'

def get_image_from_internet(url):
    data = requests.get(url).content
    img = Image.open(io.BytesIO(data))
    img.save(str(url[:5])+'.png')

def delete_image(url):
    os.remove(str(url[:5])+'.png')


def is_url_image(image_url):
    image_url = BASE_URL+image_url
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(image_url)
    if r.headers["content-type"] in image_formats:
      return image_url
    else:
        return 'No question/answer found'



def present_answer(URL):
    BASE_URL = "https://www.exam-mate.com"
    soup = BeautifulSoup((requests.get(URL)).content, "html.parser")
    questions_arr = []
    answers_arr = []

    sub1_question = "javascript:previewQuestion("
    sub2 = ');" style'
    sub1_answer = "javascript:previewAnswer("

    #scraping for questino links

    for tag in soup.select("td:nth-of-type(1) a"):
        test_str = str(tag)
        idx1_question = test_str.index(sub1_question)
        idx2_question = test_str.index(sub2)
        res = ''
        # getting elements in between
        for idx in range(idx1_question + len(sub1_question), idx2_question):
            res = res + test_str[idx]
        final_link = BASE_URL+res.split(',')[1][2:-1]
        questions_arr.append(final_link)



    for tag in soup.select("td:nth-of-type(2) a"):
        test_str = str(tag)
        idx1_answer = test_str.index(sub1_answer)
        idx2_answer = test_str.index(sub2)
        res = ''
        # getting elements in between
        for idx in range(idx1_answer + len(sub1_answer), idx2_answer):
            res = res + test_str[idx]
        final_answer = res.split(',')[1][2:]
        if len(final_answer) > 1:
            final_answer = BASE_URL + final_answer
            answers_arr.append(final_answer)
        else:
            answers_arr.append(final_answer)
    return questions_arr,answers_arr

def blocking_function():
    time.sleep(5)
    print('iterations')
    return

def combine_arrays(list1, list2):
    return [x for x in itertools.chain.from_iterable(itertools.zip_longest(list1, list2)) if x]


#scraping quizlet
def quizlet_scraper(url):
  dict_scraped = {}
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
  soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
  for i, (question, answer) in enumerate(zip(soup.select('a.SetPageTerm-wordText'), soup.select('a.SetPageTerm-definitionText')), 1):
      dict_scraped[str(question.get_text(strip=True, separator='\n'))] = str(answer.get_text(strip=True, separator='\n'))
  return dict_scraped



quizlet_list_created=False
index = 0
res_1 = []
res_2 = []
flow = False
past_paper_flow = False
advanced_flow_question = False
advanced_flow_answer = False
TOKEN = 'fuck u'
number = 0
general_array = []

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)


    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')


    @client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        global quizlet_list_created
        global index
        global res_1
        global res_2
        global flow
        global past_paper_flow
        global number
        global advanced_flow_question
        global advanced_flow_answer
        global past_paper_questions
        global past_paper_answers
        global general_array


        if message.author == client.user:
            return

        # Get data about the user
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")
        #instructions

        if 'past paper' in user_message.lower():
            await message.channel.send("what subject would you like to do?")
            past_paper_flow = True
            return
        if past_paper_flow and user_message.lower() in ib_subject_choices:
            index = ib_subject_choices.index(user_message.lower())
            subject_code = IB_Subject_Code[index]
            past_paper_questions,past_paper_answers = present_answer(URL.format(subject_code,0))
            await message.channel.send('type "start" to start reviewing')
            advanced_flow_question = True
            general_array = combine_arrays(past_paper_questions,past_paper_answers)
            print(number)
            return
        if advanced_flow_question:
            Internet_URL = general_array[number]
            if len(Internet_URL) == 1:
                await message.channel.send(str(Internet_URL))
            else:
                get_image_from_internet(Internet_URL)
                await message.channel.send(file = discord.File(str(Internet_URL[:5])+'.png'))
                delete_image(Internet_URL)
                print(number)
                number = number +1
            return


        #if advanced_flow_answer or advanced_flow_question and user_message.lower == 'end':
        #    number = 0
        #    advanced_flow_question = 0
        #    await message.channel.send('you have ended practice successfully!')





        #if past_paper_flow and user_message.lower() not in ib_subject_choices:
        #    await message.channel.send('that subject is either made up or not currently supported')
        #    return

        if user_message.lower() == 'quizlet':
            await message.channel.send("sounds good! send me a link to the flashcards and ill help you revise for them")

        #acc quizlet scraping




        if 'quizlet' in user_message:
            dict_with_words = quizlet_scraper(user_message)
            res_1 = list(dict_with_words.keys())
            res_2 = list(dict_with_words.values())
            quizlet_list_created = True
            print(str(res_1[0:5]))
            print(quizlet_list_created)
            flow = True
            await message.channel.send('list has been created. Type "start" to start revising')
            return



        if flow and user_message.lower() == 'start':
            await message.channel.send('practice has started')
            await message.channel.send('question ' + str(index+1) + ":" + str(res_1[index]))


            return

        if flow and user_message.lower() == 'end':
            quizlet_list_created = False
            await message.channel.send('okay, all data has been cleared')
            flow = False
            index = 0
            return

        if flow and user_message.lower != 'start':
            if flow and str(res_2[index]) == user_message:
                await message.add_reaction('✅')
                await message.add_reaction('😫')
                await message.channel.send('correct answer!')
                #for yede in range(int(10)):
                #    blocking_function()
                #    blocking_function()
                index += 1
                await message.channel.send('question ' + str(index + 1) + ":" + str(res_1[index]))
                return

            if flow and str(res_2[index]) != user_message:
                await message.add_reaction('💩')
                await message.channel.send('the answer is: ' + str(res_2[index]))
                #for yede in range(int(20/5)):
                #   blocking_function()
                #   blocking_function()
                index += 1
                await message.channel.send('question ' + str(index + 1) + ": " + str(res_1[index]))
                return

            if index == len(res_2):
                await message.channel.send('one cycle done')
                index = 0
                return



        #the return statement is a godly thing and also remove loop and just use rerturn statements.





            #make an on message function nested inside this. Loop is probably not neee
                # d , put it under the start function, basically check for the message thing while index < length of res_2 or 1 idk
                # i dont think that is possible

        # for changing something midflashcard, change the block functino to check if theres any input from the user,
        # if there is then act upon it during the waiting loop





        if user_message.lower() == 'start' and quizlet_list_created == False:
            await message.channel.send('send in a link before you say this')


        #HELP TAB
        if user_message.lower() == "help":
            await message.channel.send('')

    
    


        #add functionality to make quizlet_list_created == false once the idx reaches maximum limit ie all the flashcards have been exhausted.




        # If the user message contains a '?' in front of the text, it becomes a private message




    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)


