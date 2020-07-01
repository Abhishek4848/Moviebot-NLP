import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import pandas as pd
from imdb import IMDb
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            action = i['context'][0]
            break
    return (result,action)

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res




#Creating GUI with tkinter
import tkinter
from tkinter import *
import user_review
import movie_reccomendation_genre
import getMovieDetail
import moviereccomendertest
import UserreviewReccomender

user_name, user_id = user_review.entry()
action = ''
def reccomender_engine():
    msg = EntryBox.get('1.0','end-1c').strip()
    EntryBox.delete("0.0", END)
    if msg != '':
        global SendButton
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, user_name + ': ' + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        if('search_movie_by_name' == action):
                fail_test = moviereccomendertest.failsafe(msg)
                if fail_test!='Fail':
                    res = moviereccomendertest.cosine_recommendations(msg)
                    ChatLog.insert(END, "Bot:  \n\n")
                    for i in range(len(res)):
                        ChatLog.insert(END, res[i]+'\n')
                    global SendButton
                    SendButton.config(command = send)
                else:
                  
                    ia = IMDb()
                    exp_movie = ia.search_movie(msg)
                    l = []
                    try:
                        movie = ia.get_keyword(msg)
                        ChatLog.insert(END,'Bot: there you go...\n\n')
                        for movie in random.sample(movie, 5):
                            ChatLog.insert(END, f"{' '*5}{movie}\n")
                                    
                    except:
                        ChatLog.insert(END,"sorry nothing found\n\n")
                    SendButton.config(command = send)
        elif('get_movie_by_genre' == action):
            try:
                ChatLog.insert(END, "Bot: Here are some recomendations for you\n\n" )
                movie_list = movie_reccomendation_genre.searchbygenre(msg)
                for movie in random.sample(movie_list, 5):
                    ChatLog.insert(END, f"{' '*5}{movie}\n\n")
                ChatLog.insert(END, f"{' '*5}Are you satisfied with the suggestions ?\n\n")
                def recurr():
                    global SendButton
                    opt = EntryBox.get('1.0', 'end-1c').strip()
                    EntryBox.delete("0.0", END)
                    ChatLog.config(state = NORMAL)
                    ChatLog.insert(END, user_name+ ': ' + opt + '\n\n')
                    if 'y' in opt.lower():
                        ChatLog.insert(END, "Bot: Thats Great\n\n")
                        SendButton.config(command=send)
                    else:
                        ChatLog.insert(END, f"Bot: Hope you like these suggestions\n\n")
                        for movie in random.sample(movie_list, 5):
                            ChatLog.insert(END, f"{' '*5}{movie}\n\n")
                        ChatLog.insert(END, f"{' '*5}Are you satisfied with the suggestions ?\n\n")
                SendButton.config(command = recurr)
            except:
                ChatLog.insert(END,"Bot: sorry we ran into a problem please try again\n\n")
                SendButton.config(command = send)

        elif('get_review' == action):
                ChatLog.insert(END, "Bot: setting things up\n\n")
                mov_id, movie = user_review.movieIdFinder(msg)
                if(mov_id!=-1):
                    def review():
                        Review = EntryBox.get('1.0', 'end-1c').strip()
                        EntryBox.delete('0.0', END)
                        ChatLog.insert(END, user_name + ': ' + Review+'\n\n')
                        rat_user, pred = user_review.getreviewd(Review)
                        if pred == 1:
                            ChatLog.insert(END, 'Bot: Thank you for positive review we will consider this while reccomending you movies next time\n\n')
                        elif pred == 0:
                            ChatLog.insert(END, "Bot: Negative review detected , we will consider this while reccomending you movies next time")
                        ChatLog.insert(END, f"Bot: your predicted rating according to review : {rat_user}\n\n")
                        user_review.tableupdater(user_id, mov_id, rat_user)
                        global SendButton
                        SendButton.config(command = send)
                    def opt_():
                        opt = EntryBox.get('1.0', 'end-1c').strip()
                        EntryBox.delete("0.0", END)
                        ChatLog.config(state = NORMAL)
                        ChatLog.insert(END, user_name+': '+opt+'\n\n')
                        if 'y' in opt.lower():
                            ChatLog.insert(END, "Bot: Your review\n\n")
                            global SendButton
                            SendButton.config(command = review)
                        else:
                            ChatLog.insert(END,"Bot: redirecting back ...\n")
                            SendButton.config(command = send)
                    ChatLog.insert(END, f"Bot: {movie}, is this the movie (Yes/No)\n\n")
                    SendButton.config(command = opt_)
                else:

                    ia = IMDb()
                    m1 = ia.search_movie(msg)
                    l1 = []
                    for i in range(5):
                        l1.append(str(m1[i]))
                    df = pd.read_csv('movies.csv')
                    ind = df.shape[0]
                    for i in range(4):
                                l = []
                                movie = ia.get_movie(m1[i].movieID)
                                s = "|".join(movie['genres'])
                                l.append(ind + i)
                                l.append(l1[i])
                                l.append(s)
                                df.loc[ind+i] = l
                                df.to_csv('movies.csv',index_label=False)
                    ChatLog.insert(END,'Bot: no such movie found in our database.. did you mean:\n\n')
                    ChatLog.insert(END,"1. "+l1[0]+"\n")
                    ChatLog.insert(END,"2. "+l1[1]+"\n")
                    ChatLog.insert(END,"3. "+l1[2]+"\n")
                    ChatLog.insert(END,"4. "+l1[3]+"\n")
                    SendButton.config(command = send)

        elif('user_review_recc' == action):
                r,t = UserreviewReccomender.getmovieid(user_id)
                if r == []:
                    ChatLog.insert(END, "Bot: sorry could not get movies based on review history since you haven't reviewed any movie, getting movies that you might like\n\n")
                    SendButton.config(command = send)
                search = UserreviewReccomender.getgenre(t)
                movielist = moviereccomendertest.cosine_recommendations(search)
                ChatLog.insert(END, "Bot: Here are some recomendations for you:\n\n")
                for movie in random.sample(movielist, 5):
                    ChatLog.insert(END, f"{' '*5}{movie}\n\n")
                ChatLog.insert(END, f"{' '*5}Hope you like these suggestion\n\n")
                SendButton.config(command = send)
                

        elif('get_movie_detail' == action):
            ChatLog.insert(END, "Bot: Enter the name of the movie:\n\n")
            def search_movie():
                search = EntryBox.get('1.0', 'end-1c').strip()
                EntryBox.delete('0.0', END)
                ChatLog.config(state = NORMAL)
                ChatLog.insert(END, user_name+': ' + search + '\n\n')
                movdetails = getMovieDetail.searchbymovie(search)
                details = f'''*Title : {movdetails[0]}\
                \n*Rating : {movdetails[2]} \
                \n*Genre : {movdetails[3]} \
                \n*Year of release : {movdetails[1]}\
                \n*Language : {movdetails[4]}\
                \n*Director : {movdetails[5]}\
                \n*Actors : {movdetails[6]}\
                \n*Description : {movdetails[7]}'''
                ChatLog.insert(END, "Bot: Deatils of the movie: \n" + details + '\n\n')
                global SendButton
                SendButton.config(command = send)
            SendButton.config(command = search_movie)


        elif('blockbuster_movies' == action):
            ChatLog.insert(END, "Bot: Please enter the year :\n\n")
            def blockbustermovies():
                search = EntryBox.get('1.0', 'end-1c').strip()
                EntryBox.delete('0.0', END)
                ChatLog.config(state = NORMAL)
                ChatLog.insert(END, user_name+': ' + search + '\n\n')
                blocklist = getMovieDetail.blockbuster(int(search))
                if blocklist :
                    details = "\n>> ".join(str(x) for x in blocklist)
                    ChatLog.insert(END, "Bot: Blockbuster movies : "+" \n" + details + '\n\n')
                else :
                    details = "List will be updated soon ..."
                global SendButton
                SendButton.config(command = send)
            SendButton.config(command = blockbustermovies)

        elif('shutdown' == action):
                ChatLog.insert(END, "Bot: Alright goodbye....closing chatbot....\n\n")
                global base
                base.destroy()
                exit(1)
        
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    global user_name
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, user_name + ': ' + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        action_list = ['search_movie_by_name', 'get_movie_by_genre', 'get_review',
         'user_review_recc', 'get_movie_detail', 'shutdown','blockbuster_movies']
        
        res, act = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        if act == 'List_of_genre':
            Genre = '''>> Action \n>> Adult \n>> Adventure \n>> Animation \n>> Biography \n>> Comedy \n>> Crime \n>> Documentary \n>> Drama\
            \n>> Family \n>> Fantasy \n>> Film-Noir \n>> History \n>> Horror \n>> Mystery \n>> Reality-TV \n>> Romance \n>> Sci-Fi \n>> Sport \n>> Thriller \n>> War \n>> Western'''
            ChatLog.insert(END, "Bot: There you go\n" + Genre + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        if act in action_list:
            global SendButton, action
            action = act
            SendButton.config(command= reccomender_engine )
            

base = Tk()
base.title("Moviebot")
base.geometry("400x500")
base.resizable(width=False, height=FALSE)
#base = widget()
#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
# show user-name & id 
ChatLog.config(font = ("Arial",12))
ChatLog.insert(END, f'\t User Name: {user_name} \n\n\t User Id: {user_id}\n\n')
ChatLog.insert(END, f'Bot: Hi there {user_name} \n\n')

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=10, y=401, height=90, width=290)
SendButton.place(x=300, y=401, height=90, width = 90)

base.mainloop()
