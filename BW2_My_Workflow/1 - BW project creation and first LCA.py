#!/usr/bin/env python
# coding: utf-8

# # Brightway 2 - From Project creation to LCA

# ### 1 Project creation

# Import relevant packages. There are two ways to import Brightway2, `import brightway2 as bw` or, `from brightway2 import *`. The latter allows you to work without the `bw.` caller.

# In[1]:


import brightway2 as bw


# In[2]:


import os               # to use "operating system dependent functionality"
import numpy as np      # "the fundamental package for scientific computing with Python"
import pandas as pd     # "high-performance, easy-to-use data structures and data analysis tools" for Python


# Check project directory, current project, list projects and create/set a project folder, respectively:

# In[3]:


bw.projects.dir


# In[4]:


bw.projects.current


# In[5]:


bw.projects.report();


# In[6]:


bw.projects.set_current('MW_1')


# Setup biosphere and LCIA methods with `bw2setup()`.

# In[7]:


bw.bw2setup()


# In[8]:


bw.databases


# In[9]:


bw.Database('biosphere3')


# ### 2 Extracting and searching activities and exchanges

# Here you can see all the methods you can call on the bw object:

# In[10]:


dir(bw);


# Let's assign the database to a variable:

# In[11]:


my_bio = bw.Database('biosphere3')


# In[12]:


type(my_bio)


# In[13]:


len(my_bio)


# Let's check its properties and methods:

# In[14]:


dir(my_bio);


# Some of the more basic ones we will be using now are :  
#   - `random()` - returns a random activity in the database
#   - `get(*valid_exchange_tuple*)` - returns an activity, but you must know the activity key
#   - `load()` - loads the whole database as a dictionary.
#   - `make_searchable` - allows searching of the database (by default, it is already searchable)
#   - `search` - search the database  
#   
# Lets start with `random`:

# In[15]:


my_bio.random()


# It gives us a random bioosphere activity, to use it properly we need to assign it to a variable.

# In[16]:


random_biosphere = my_bio.random()
random_biosphere


# In[17]:


type(random_biosphere)


# The type is an **activity proxy**. Activity proxies allow us to interact with the content of the database. In the journey to and from the database, several translation layers are used:
# 
# SQLITE DATABASE *Binary tuples*
# 
# &#8595;
# 
# Peewee ORM *Python classs instance* (***ActivityDataset*** or ***ExchangeDataset***)
# 
# &#8595;
# 
# Brightway2 *Python class instance* (***Activity*** or ***Exchange***)

# BW *mostly* works with `Activity` or `Exchange`.
# 
# To see what the activity contains, we can convert it to a dictionary:

# In[18]:


random_biosphere.as_dict()


# Let's get some activities:

# In[19]:


my_bio.get(random_biosphere['code'])


# Activities can also be "gotten" via `get_activity`, but the argument is the activity **key**, consisting of a tuple with two elements: the database name, and the activity code.

# **Exercise:** Use `bw.get_activity()` to retrieve the random biosphere activity. 

# In[20]:


code = random_biosphere['code']
databasename = 'biosphere3'
random_biosphere_key = (databasename, code)
bw.get_activity(random_biosphere_key)


# You can always find the `key` to an activity using the `.key` property:

# In[21]:


random_biosphere.key


# Let's now search through our database!

# In[22]:


my_bio.search('carbon dioxide'); # You can also use bw.Database('biosphere3').search('carbon dioxide')


# We can also iterate over the database, this method uses [*list comprehension*]https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions which allow us to add filters and personalize the search.

# In[23]:


[act for act in my_bio if 'Carbon dioxide' in act['name'] 
                                            and 'fossil' in act['name']
                                            and 'non' not in act['name']
                                            and 'urban air close to ground' in str(act['categories'])
]


# Activities returned by searches or list comprehensions can be assigned to variables, but to do so, one needs to identify the activity by index. Based on the above, I can refine my filters to ensure the list comprehension only returns one activity, and then choose it without fear of choosing the wrong one.

# In[24]:


activity_I_want = [act for act in my_bio if 'Carbon dioxide' in act['name'] 
                                            and 'fossil' in act['name']
                                            and 'non' not in act['name']
                                            and 'urban air close to ground' in str(act['categories'])]
activity_I_want


# **Exercise:** Look for and assign to a variable an emission of nitrous oxide emitted to air in the "urban air" subcompartment.
# 

# In[25]:


exercise_activity = [act for act in my_bio if 'nitrogen' in act['name']
                                            and 'urban air' in str(act['categories'])]
exercise_activity


# Now we select the first one:

# In[26]:


exercise_activity = exercise_activity[0]
exercise_activity


# ### 3 Methods

# As mentioned before, we also installed methods:

# In[27]:


list(bw.methods)


# Select a random method:

# In[28]:


bw.methods.random()


# This is just an informative tuple, to get the actual method we use:

# In[29]:


bw.Method(bw.methods.random())


# Of course, a random method is probably not useful except to play around. To find an actual method, one can again use list comprehensions. Let's say I am interested in using the IPCC2013 100 years method:

# In[30]:


[m for m in bw.methods if 'IPCC' in str(m) and ('2013') in str(m) and '100' in str(m)]


# We can select the one we are interested in like we did before, assigning it to a variable and choose by subscripting. 

# In[31]:


select1 = [m for m in bw.methods if 'IPCC' in str(m) and ('2013') in str(m) and '100' in str(m)][0]
select1


# We can also refine searches:

# In[32]:


ipcc2013 = [m for m in bw.methods if 'IPCC' in m[0]
                    and ('2013') in str(m)
                    and 'GWP 100' in str(m)
                    and 'no LT' not in str(m)][0]
ipcc2013


# In[33]:


type(ipcc2013)


# In[34]:


ipcc_2013_method = bw.Method(ipcc2013)


# Let's check the methods associated with this method object:

# In[35]:


dir(ipcc_2013_method);


# In[36]:


ipcc_2013_method.name


# In[37]:


ipcc_2013_method.metadata;


# In[38]:


ipcc_2013_method.metadata['unit']


# **Question:** What is inside this method object? Let's check it out!

# In[39]:


ipcc_2013_method.load();


# This is a list of tuples of the database, code and the characterization factor.

# **Exercise:** Create a dictionary with `keys = elementary flow names` and `values = characterization factors `for the `TRACI` "respiratory effects, inorganics" method (including long-term emissions).  
# Bonus (optional): Generate a Pandas Series with the resulting dictionary. 

# In[48]:


# Query 1
[m for m in bw.methods if 'TRACI' in str(m)
                        and 'respiratory effects' in str(m)]


# Selecting:

# In[52]:


# Query 1
TRACI_resp_effect_tuple = [m for m in bw.methods if 'TRACI' in str(m)
                        and 'respiratory effects' in str(m)][0]
TRACI_resp_effect_tuple


# Now let's make a dictionary, let's assing the tuple to a `Method`:

# In[53]:


TRACI_resp_effect_method = bw.Method(TRACI_resp_effect_tuple)
TRACI_resp_effect_method


# In[54]:


TRACI_resp_effect_method.load()


# In[55]:


TRACI_resp_effect_dict = {bw.get_activity(ef[0])['name']:ef[1] for ef in TRACI_resp_effect_method.load()}
TRACI_resp_effect_dict


# In[57]:


# Bonus: put the whole thing in a neat Pandas series
pd.Series(TRACI_resp_effect_dict,
          name="{}, {}".format(TRACI_resp_effect_method.name, TRACI_resp_effect_method.metadata['unit']))


# In[ ]:




