#!/usr/bin/env python
# coding: utf-8

# In[2]:


from flask import Flask,render_template,url_for,request
from string import punctuation
from heapq import nlargest
import os
from datetime import datetime
from datetime import date


legaltechfercx = Flask(__name__)
@legaltechfercx.route('/')
def home():
	return render_template('home.html')
    
@legaltechfercx.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        text = request.form['message']
        dates=[]
    seperated=text.split(",")
    for c in seperated:
        for u in range(10):
            if u==4 or u==7:
                if c[u]!="-":
                    my_prediction="Invalid input, please read the guide again."
                    return render_template('result.html',prediction = my_prediction)
            elif u!=4 or u!=7:
                try:
                    int(c[u])
                except ValueError:
                    my_prediction="Invalid input, please read the guide again."
                    return render_template('result.html',prediction = my_prediction)
        dates.append(datetime.strptime(c, "%Y-%m-%d").date())
    if len(dates)%2!=0:
        dates.append(date.today())
    d0=dates[0]
    d1=dates[1]
    backdate=dates[1]
    ino=[]
    rang = ((dates[len(dates)-1]-dates[0]).days)-1
    g=0
    for d in range(int(len(dates)/2)):
        d0=dates[g]
        d1=dates[g+1]
        delta = d1 - d0
        back=d0-backdate
        backdate=d1
        if g>0:
            for c in range(abs(back.days)):
                ino.append(1)
        for c in range(delta.days):
            ino.append(0)
        g=g+2
    fail=False
    i=0
    o=0
    for k in range(365):
        if ino[k]==0:
            i=i+1
        else:
            o=o+1
    for j in range(len(ino)-365):
        if ino[j+365]==0:# zero means in the UK
            i=i+1
            if i<185:
                fail=True
            if ino[j-364]==0:
                i=i-1
            else:
                o=o-1
        else:
            o=o+1
            if o>180:
                fail=True
            yr=364
            if ino[j]==1:
                o=o-1
            else:
                i=i-1
                
    if fail:
        my_prediction="You have broken continous residency"
    else:
        my_prediction="You have NOT broken continous residency"
    return render_template('result.html',prediction = my_prediction)
    

if __name__ == '__main__':
    legaltechfercx.run()
