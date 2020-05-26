import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime
import json
import pickle
import matplotlib.pyplot as plt
with open('result.pickle', 'rb') as handle:
    b = pickle.load(handle)
a=[]
m={}
for i in b:
	a.append(b[i])
	m[i]=b[i].days
result=[]
for i in a:
	result.append(i.days)
final = sorted(m.items(),key=lambda kv:(kv[1],kv[0]),reverse =True)
print(final[:10])
x = [0,200,400,600,800,1000,1200,1400,1600,1800,2000]
plt.xticks(x)
plt.hist(result,bins=x,rwidth=0.9)
plt.xlabel('Lag in Days')
plt.ylabel('Frequency')
plt.savefig('image.jpg')
plt.show()


