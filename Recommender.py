from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from Kickstart import *
import CosineSim
from CosineSim import cosineSimilarity, text_to_vector

main = tkinter.Tk()
main.title("Collaborative Filter Based Group Recommendation Crowdfunding")
main.geometry("1300x1200")

global kickstart_filename
global social_filename
global crowdfunds
global recommend
recommend = 0

def uploadDataset():
    global kickstart_filename
    kickstart_filename = filedialog.askopenfilename(initialdir="dataset")
    pathlabel.config(text=kickstart_filename)
    text.delete('2.0', END)
    text.insert(END,kickstart_filename+" loaded\n");

def uploadSocialDataset():
    global social_filename
    social_filename = filedialog.askopenfilename(initialdir="dataset")
    pathlabel.config(text=social_filename)
    text.delete('2.0', END)
    text.insert(END,social_filename+" loaded\n");

def generateModel():
    text.delete('1.0', END)
    global crowdfunds
    crowdfunds = []
    dataset = pd.read_csv(kickstart_filename)
    social_dataset = pd.read_csv(social_filename)
    for i in range(len(dataset)):
        pid = dataset._get_value(i, 'ID')
        project = dataset._get_value(i, 'main_category')
        goalAmount = dataset._get_value(i, 'pledged')
        deadline = dataset._get_value(i, 'deadline')
        user = social_dataset._get_value(i, 'User_ID')
        friends = social_dataset._get_value(i, 'Social_Friends')
        if goalAmount > 0:
            ks = Kickstart()
            ks.setUser(user)
            ks.setFriends(friends)
            ks.setProjectID(pid)
            ks.setProject(project)
            ks.setDeadline(deadline)
            ks.setGoalAmount(goalAmount)
            crowdfunds.append(ks)
    text.insert(END,'Total number of successfull projects found in dataset are : '+str(len(crowdfunds))+"\n\n")            
    
def groupRecommendation():
    text.delete('1.0', END)
    global recommend
    recommend = 0
    input_data = simpledialog.askstring("Enter project name", "Enter project name",parent=main)

    vector1 = CosineSim.text_to_vector(input_data.lower())
    backers_peoples = []
    recommended_groups = []
    for ks in crowdfunds:
        group = str(ks.getUser()).lower()+" "+str(ks.getFriends()).lower()+" "+str(ks.getProjectID()).lower()+" "+str(ks.getProject()).lower()+" "+str(ks.getDeadline()).lower()+" "+str(ks.getGoalAmount())
        vector2 = CosineSim.text_to_vector(group)
        cosine = CosineSim.cosineSimilarity(vector2, vector1)
        if cosine > 0.0:
            backers_peoples.append(str(ks.getProjectID()))
            recommended_groups.append(str(ks.getFriends()))
    recommend = len(recommended_groups)
    text.insert(END,'Given project name : '+input_data+"\n")
    text.insert(END,'Total backers invested in this project is : '+str(len(backers_peoples))+"\n")
    text.insert(END,"Backers ID's invested in this project\n\n")
    text.insert(END,str(backers_peoples)+"\n\n")
    text.insert(END,'Number of groups recommended for this project is : '+str(recommend)+"\n\n")
    text.insert(END,'Group Details\n')
    for i in range(len(recommended_groups)):
        text.insert(END,'Group '+str((i + 1))+' user list : '+str(recommended_groups[i])+"\n")
        
    
def graph():
    height = [len(crowdfunds), recommend]
    bars = ('Total Projects', 'Recommended Group Size')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()
   
font = ('times', 24, 'bold')
title = Label(main, text='Collaborative Filter Based Group Recommendation Crowdfunding',anchor=CENTER, justify=CENTER)
title.config(bg='#2e6ce8', fg='white')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)


font1 = ('times', 16, 'bold')
upload = Button(main, text="Upload Kickstart Projects Dataset", command=uploadDataset)
upload.place(x=50,y=100)
upload.config(font=font1)  

pathlabel = Label(main)
pathlabel.config(bg='#2e6ce8', fg='white')  
pathlabel.config(font=font1)           
pathlabel.place(x=50,y=150)

socialButton = Button(main, text="Upload Social Relation Friends Dataset", command=uploadSocialDataset)
socialButton.place(x=50,y=200)
socialButton.config(font=font1)

modelButton = Button(main, text="Generate Model", command=generateModel)
modelButton.place(x=50,y=250)
modelButton.config(font=font1)

groupButton = Button(main, text="Group Recommendation", command=groupRecommendation)
groupButton.place(x=50,y=300)
groupButton.config(font=font1)

graphButton = Button(main, text="Total Projects Vs Group Recommendation Graph", command=graph)
graphButton.place(x=50,y=350)
graphButton.config(font=font1)

font1 = ('times', 15, 'bold')
text=Text(main,height=30,width=80)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=500,y=100)
text.config(font=font1)


main.config(bg='#71b4f0')
main.mainloop()
