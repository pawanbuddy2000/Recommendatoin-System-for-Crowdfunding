import pandas as pd
import numpy as np
from Kickstart import *
import CosineSim
from CosineSim import cosineSimilarity, text_to_vector

dataset = pd.read_csv('dataset/ks-projects-201801.csv')
social_dataset = pd.read_csv('dataset/social_friends_followers.txt')

crowdfunds = []

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
        
print(len(dataset))
strs = 'Product Design'
vector1 = CosineSim.text_to_vector(strs)
backstage_peoples = []
recommended_groups = []
for ks in crowdfunds:
    group = str(ks.getUser())+" "+str(ks.getFriends())+" "+str(ks.getProjectID())+" "+str(ks.getProject())+" "+str(ks.getDeadline())+" "+str(ks.getGoalAmount())
    vector2 = CosineSim.text_to_vector(group)
    cosine = CosineSim.cosineSimilarity(vector2, vector1)
    if cosine > 0.0:
        backstage_peoples.append(str(ks.getProjectID()))
        recommended_groups.append(str(ks.getFriends()))

print(backstage_peoples)
print(recommended_groups)        
