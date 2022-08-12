#!/usr/bin/env python
# coding: utf-8

# # 1. Activities and exchanges

# How to use `Activity` and `Exchange` classes. This tutorial is a copy of the oficial [tutorial](https://github.com/brightway-lca/brightway2/blob/master/notebooks/Activities%20and%20exchanges.ipynb) with some additional information for a more comprehensive learning experience.with some additional information for a more comprehensive learning experience. See [this](https://github.com/brightway-lca/brightway2/blob/master/notebooks/Parameters%20-%20manual%20creation.ipynbhttps://github.com/brightway-lca/brightway2/blob/master/notebooks/Parameters%20-%20manual%20creation.ipynb) Notebook for additional ways of creating activities and exchanges.

# Methods used throughout this tutorial:
# 
# * `projects.set_current('project_name')`: Create a new project.
# 
# * `Database('database_name')`: Create a new database.
# 
# * `db.write({})`: Data insert (see below for further data structure for the dictionary).
# 
# * `db.get('activity_name')`: Extract activity(s) from the database. This is saved into a variable, e.g. `activity_var_name`.
# 
# * `activity_var_name.save()`: Save changes.
# 
# * `activity_var_name.key`: See the activity name.
# 
# * `activity_var_name.exchanges()`: When used in a `for` loop, it extracts the exchanges.
# 
# * `activity_var_name.technosphere()`: When used in a `for` loop, it extracts the technosphere exchanges.
# 
# * `activity_var_name.biosphere()`: When used in a `for` loop, it extracts the biosphere exchanges.
# 
# * `activity_var_name.production()`: When used in a `for` loop, it extracts the production exchanges.
# 
# * `len(input)`: Counts the number of items of the input.
# 
# * `db.new_activity(code='activity_code', name='activity_name')`: Create a new activity. It generates the code by default if the attribute is not specified. If only code is defined, it will not be able to save. An activity always needs a name. This is normally saved into a new varable, e.g. `new_activity_var_name`.
# 
# * `new_activity_var_name.new_exchange(input='input_activity', amount=1, type='whatever_type')`: Create new exchanges for the newly created activity. The `amount` can also be 0 if the amount is calculated bases on preceeding activities and exchanges calculations (see [here](https://github.com/brightway-lca/brightway2/blob/master/notebooks/Parameters%20-%20manual%20creation.ipynbhttps://github.com/brightway-lca/brightway2/blob/master/notebooks/Parameters%20-%20manual%20creation.ipynb) for such calculations). This is normally saved into a new varable, e.g. `new_exchange_var_name`.
# 
# * `new_exchange_var_name.input` and `new_exchange_var_name.output` will return activities
# 
# * `new_exchange_var_name.unit`: Returns the units of the exchange.
# 
# * `new_exchange_var_name.amount`: Returns the amount of the exchange.
# 
# * `new_exchange_var_name.uncertainty_type`: If the uncertainty was calculated, it will return the type uncertainy of the exchange. See below how to set the uncertainty.
# 
# * `new_exchange_var_name.uncertainty`: If calculated, it returns the uncertinty.
# 
# * `new_exchange_var_name.random_sample(n=size of the sample)`: For now I am not sure what is this randomization, but I assume it is the uncertainty.
# 
# * `activity_you_copied_from.copy(name='name of the new activity', code='chosen code')`: Copy activities and exchanges with a new name and code. It does not copy upstreams.
# 
# * `activity.upstream()`: Shows the upstream of an activity.
# 
# * `activity.delete()`: Deletes the activity.
# 

# Start Brightway2:

# In[1]:


from brightway2 import * # Start Brightway2


# Create a new project:

# In[2]:


projects.set_current("Tut_1_Activities_Exchanges") # Create a new project


# Create a new database:

# In[3]:


db = Database('a_e')


# Let's insert some basic data:

# In[4]:


db.write({
    ('a_e', 'cat'): {                                          # Actrivity 1 - They always need a name!                            
        'name': 'cat',                                             # Characteristic 1
        'unit': 'kilogram',                                        # Characteristic 2
        'color': 'black',                                          # Characteristic 3
        'exchanges': [{                                            # Exchanges - They always have to have 'input', 'amount' and 'type' minimum
            'input': ('a_e', 'cat food'),                              # Input 1 -> Activity 2
            'amount': 10,                                              
            'type': 'technosphere'                                    
        }, {
            'input': ('a_e', 'kitty litter'),                          # Input 2 -> Activity 3
            'amount': 10,
            'type': 'technosphere'
        }, {
            'input': ('a_e', 'smell'),                                 # Input 3 -> Activity 4
            'amount': 1,
            'type': 'biosphere'
        }]
    },
    ('a_e', 'kitty litter'): {'name': 'yuk'},                    # Activity 2, since these are flows, they don't have exchanges.
    ('a_e', 'cat food'): {'name': 'yum'},                        # Activity 3
    ('a_e', 'smell'): {'name': 'stinky', 'type': 'biosphere'},   # Activity 4
})


# Let's get an activity with `.get()`:

# In[5]:


act = db.get('cat')
act


# The `cat` process has no categories or location so far. Let's change that:

# In[6]:


act['location'] = 'inside'
act['categories'] = ['felis', 'catus']
act


# Let's save:

# In[7]:


act.save()


# Let's iterate over the available data with a `for` loop:

# In[8]:


for key in act:
    print(key, ':', act[key])


# Note that the fields `database` and `code` were automatically added.
# Let's see the some methods for an activity.

# In[9]:


act.key # See the activity key


# In[10]:


for exc in act.exchanges(): # Iterate over exchanges
    print(exc)


# In[11]:


print('Technosphere exchanges:') # Let's see specific exchanges
for exc in act.technosphere():
    print(exc)
print('Biosphere exchanges:')
for exc in act.biosphere():
    print(exc)
print('Production exchanges:')
for exc in act.production():
    print(exc)


# In[12]:


len(act.exchanges())  # Count exchanges


# In this case, there was not a production exchange — Brightway2 sets production to 1 when building the technosphere matrix in no production exchange is given.
# 
# Let's look at upstream exchanges — those that consume this activity's reference product. Since we don't have any yet, let us create an new activity:

# In[13]:


na = db.new_activity("dog") # "dog" is set as 'code' by default
na.save()


# Aha! An error! Why? Well, activities must have names!! Let's fix that:

# In[ ]:


na['name'] = 'fido' # Another route, is to define the new activity attributes within the .new_activity() method, e.g.: db.new_activity(code='dog', name='fido')
na.save()


# We will also have a friendly error message if we dare to insert an invalid new exchange:

# In[14]:


na.new_exchange().save()


# Let's add a link to the cat process. 

# In[15]:


new_exc = na.new_exchange(input=act, amount=1, type='technosphere')
new_exc.save()


# We can nos see `fido`'s link to `cat`:    

# In[16]:


for exc in na.technosphere():
    print(exc)


# In[ ]:


for exc in act.upstream():
    print(exc)


# `exc.input` and `exc.output` will return activities:

# In[ ]:


new_exc.input, new_exc.output


# More methods for exchanges:

# In[ ]:


new_exc.unit, new_exc.amount, new_exc.uncertainty_type


# Let's add some [uncertainty](https://stats-arrays.readthedocs.io/en/latest/)!

# In[ ]:


from stats_arrays import NormalUncertainty

new_exc['uncertainty type'] = NormalUncertainty.id
new_exc['loc'], new_exc['scale'] = 1, 0.25
new_exc.save()


# We can not get an uncertainty dictionaty for use in `stats_arrays` fuctions:

# In[17]:


new_exc.uncertainty


# Let's get a random sample:

# In[18]:


new_exc.random_sample(n=10) # Are these random uncertainties?


# We can also copy activities, this also copies the activities exchanges:

# In[19]:


kudu = act.copy(name='kudu', code='antelope')
kudu, act


# In[20]:


for key in kudu:
    print(key, ':', kudu[key])


# In[21]:


for exc in kudu.exchanges():
    print(exc)


# Upstream exchanges are not copied:

# In[22]:


for exc in kudu.upstream():
    print(exc)


# In[23]:


for exc in act.upstream():
    print(exc)


# It is possible to delete some or all activities' exchanges:

# In[24]:


print('Before:', len(kudu.exchanges()))
kudu.biosphere().delete()
print('After:', len(kudu.exchanges()))


# You can also delete activities:

# In[25]:


kudu.delete()


# This new activity is no longer in the database:

# In[26]:


kudu in db


# In[27]:


act3 = db.new_activity('name' == 'mouse')


# In[28]:


act3


# In[29]:


act4 = db.new_activity('human')


# In[30]:


act4['name'] = 'Peter'


# In[31]:


act4


# In[39]:


import pandas as pd


# In[40]:


df = pd.DataFrame(db)


# In[ ]:





# In[ ]:





# In[ ]:




