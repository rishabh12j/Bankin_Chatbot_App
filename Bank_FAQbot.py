import operator
import pickle
import random
import discord
import nltk
import numpy as np
import pandas as pd
from nltk.stem.lancaster import LancasterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split as tts
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.svm import SVC
client=discord.Client()
token ="DdL5vskiAPcpfTYpKfMupsHiJpTj6sta"
stemmer = LancasterStemmer()
def cleanup(sentence):
    word_tok = nltk.word_tokenize(sentence)
    stemmed_words = [stemmer.stem(w) for w in word_tok]

    return ' '.join(stemmed_words)


le = LE()

tfv = TfidfVectorizer(min_df=1, stop_words='english')

data = pd.read_csv('BankFAQs.csv')
questions = data['Question'].values

X = []
for question in questions:
    X.append(cleanup(question))

tfv.fit(X)
le.fit(data['Class'])

X = tfv.transform(X)
y = le.transform(data['Class'])


trainx, testx, trainy, testy = tts(X, y, test_size=.25, random_state=42)

model = SVC(kernel='linear')
model.fit(trainx, trainy)
print("SVC:", model.score(testx, testy))


def get_max5(arr):
    ixarr = []
    for ix, el in enumerate(arr):
        ixarr.append((el, ix))
    ixarr.sort()

    ixs = []
    for i in ixarr[-5:]:
        ixs.append(i[1])

    return ixs[::-1]



def chat(str):
    
    cnt = 0
    print("PRESS Q to QUIT")
    print("TYPE \"DEBUG\" to Display Debugging statements.")
    print("TYPE \"STOP\" to Stop Debugging statements.")
    print("TYPE \"TOP5\" to Display 5 most relevent results")
    print("TYPE \"CONF\" to Display the most confident result")
    print()
    print()
    DEBUG = False
    TOP5 = False

    print("Bot: Hi, Welcome to our bank!")
    # while True:
    usr = str
    t_usr = tfv.transform([cleanup(usr.strip().lower())])
    class_ = le.inverse_transform(model.predict(t_usr))
    questionset = data[data['Class']==class_[0]]
    cos_sims = []
    for question in questionset['Question']:
         sims = cosine_similarity(tfv.transform([question]), t_usr)
         cos_sims.append(sims)
            
    ind = cos_sims.index(max(cos_sims))
    if not TOP5:
         response=data['Answer'][questionset.index[ind]]
    print("\n"*2)
    print("response"+response)
    return response
        # if usr.lower() == 'yes':
        #     print("Bot: Yes!")
        #     continue

        # if usr.lower() == 'no':
        #     print("Bot: No?")
        #     continue

        # if usr == 'DEBUG':
        #     DEBUG = True
        #     print("Debugging mode on")
        #     continue

        # if usr == 'STOP':
        #     DEBUG = False
        #     print("Debugging mode off")
        #     continue

        # if usr == 'Q':
        #     print("Bot: It was good to be of help.")
        #     break

        # if usr == 'TOP5':
        #     TOP5 = True
        #     print("Will display 5 most relevent results now")
        #     continue

        # if usr == 'CONF':
        #     TOP5 = False
        #     print("Only the most relevent result will be displayed")
        #     continue

        # if DEBUG:
        #     print("Question classified under category:", class_)
        #     print("{} Questions belong to this class".format(len(questionset)))


        # if DEBUG:
        #     question = questionset["Question"][questionset.index[ind]]
        #     print("Assuming you asked: {}".format(question))
     
            #print("Bot:", data['Answer'][questionset.index[ind]])
    #  else:
    #       inds = get_max5(cos_sims)
    #       for ix in inds:
    #             print("Question: "+data['Question'][questionset.index[ix]])
    #             print("Answer: "+data['Answer'][questionset.index[ix]])
    #             print('-'*50)

     
        # outcome = input("Was this answer helpful? Yes/No: ").lower().strip()
        # if outcome == 'yes':
        #     cnt = 0
        # elif outcome == 'no':
        #     inds = get_max5(cos_sims)
        #     sugg_choice = input("Bot: Do you want me to suggest you questions ? Yes/No: ").lower()
        #     if sugg_choice == 'yes':
        #         q_cnt = 1
        #         for ix in inds:
        #             print(q_cnt,"Question: "+data['Question'][questionset.index[ix]])
        #             # print("Answer: "+data['Answer'][questionset.index[ix]])
        #             print('-'*50)
        #             q_cnt += 1
        #         num = int(input("Please enter the question number you find most relevant: "))
        #         print("Bot: ", data['Answer'][questionset.index[inds[num-1]]])
    

    
#chat()
@client.event
async def on_message(message):
    message_text=message.content.lower()
    #channel=client.get_channel(566507599101427712)
    #await client.send_message(message.channel, message_text)
    if message.author == client.user:
        return

    if message.content.startswith('!hello') or message.content.startswith('hi') or message.content.startswith('heythere'):
        msg = ' Hi {0.author.mention}, Welcome to our bank!'.format(message)
        await message.channel.send(msg)
        #await client.send_message(message.channel, msg)
    
    elif "bye" in message.content.lower():
        msg = 'Bye mate {0.author.mention}'.format(message)
        await message.channel.send(msg)
        await channel.close()
    else:
    #message.content.startswith('show'):  
        print(message.content.lower())
        result=chat(message.content.lower())
        await message.channel.send(result)

                
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('NTY2NTA3NTk5MTAxNDI3NzEy.XaF0Zg.M9KEqndO5v7NzHpikbUarLmyWsQ')
