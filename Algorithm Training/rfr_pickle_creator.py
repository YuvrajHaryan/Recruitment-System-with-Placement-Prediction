#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle


# In[11]:


df=pd.read_csv('student.csv')
df.head()


# In[12]:


from sklearn.model_selection import train_test_split


# In[13]:


X_train, X_test, y_train, y_test = train_test_split(df.drop(['Unnamed: 0','PLACED'],axis=1), df['PLACED'], test_size=0.4, random_state=101)


# In[14]:


from sklearn.ensemble import RandomForestRegressor
rfr = RandomForestRegressor()
rfr.fit(X_train, y_train)


# In[17]:


pickle.dump(rfr, open('RandomForestRegressor.pkl','wb'))


# In[ ]:




