#!/usr/bin/env python
# coding: utf-8

# # 3. Databases

# How to work with database classes. This tutorial is a copy of the oficial [tutorial](https://github.com/brightway-lca/brightway2/blob/master/notebooks/Databases.ipynb), this tutorial is a copy of the oficial one with some additional information that I need to further understand certain concepts.

# In[2]:


from brightway2 import *


# Let's be tidy and create a project for this notebook:

# In[4]:


projects.set_current('Tut_3_Databases')


# For further information on what a database is, refer to the previous tutorials or read about [inventory databases](https://2.docs.brightway.dev/intro.html#inventory-databases) in the official documentation page.

# ### An example database

# Let's define an example dataset as shown in [Tutorial 1](BW_Manual.ipynb).

# In[6]:


db = Database('example')

example_data = {
  ('example', 'A'): {
      'name': 'A',
      'unit': 'kilogram',
      'location': 'hare',
      'categories': ('very', 'interesting'),
      'exchanges': [{
        'amount': 1.0,
        'input': ('example', 'B'),
        'type': 'technosphere'
      }]
  },
  ('example', 'B'): {
      'name': 'B',
      'unit': 'microgram',
      'location': 'there',
      'categories': ('quite', 'boring'),
      'exchanges':[],
  }
}


# Let's make a doodle to understand this dataset:
# ![PROJECT:](images/t_3_doodle.jpg)
# This is quite a simple example - two activities, one of whom has no inputs. In fact, this example dataset has only a few fields. Actually, there are *no required fields* in datasets, only some suggested ones, and general guidelines on how to use those suggested fields. It's like not wearing underwear - Brightway2 gives you the freedom to do it, but most people you are interacting with would prefer that you didn't.
# 
# * If you are using `Activity` proxies, then the `'name'` field is required.
# 
# Let's talk a bit about the fields in example_data:
# 
# * `name`: This one is pretty easy :)
# * `exchanges`: This is a list of inputs and outputs, like how much energy or material is needed for this dataset's production. Every exchange is an intput, unless it has the value type = "production". A production exchange defines how much of the output is produced. Most of the time, you can ignore this, as the default value is one - this is what we do in the example data. However, sometimes it is useful to define a dataset that produces more.
# 
# See also: [What happens with a non-unitary production amount in LCA?](https://chris.mutel.org/non-unitary.html)
# 

# ### Write data to dataset

# Now let's add this add this data to the created dataset:

# In[7]:


db.write(example_data)


# ### Get a random activity

# The `random()` method is a nice way of getting an activity if you just need an example:

# In[5]:


db.random()


# ### Examining database data

# We can also loop over our database, and try to get some useful information. For example, say we were interested in the number of exchanges in each activity:

# In[8]:


num_exchanges = [(activity, len(activity.exchanges())) for activity in db]
num_exchanges


# ### Searching databases

# In[9]:


db.search("*")


# ### Deleting databases

# You delete databases by deleting them from the databases object. If we look at the projects `report()` we can s

# In[ ]:


projects.report()


# In[11]:


del databases[db.name]


# In[12]:


projects.report()


# See `'Tut_3_Databases'` Now it does not store any database!

# In[ ]:




