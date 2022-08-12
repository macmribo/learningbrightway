#!/usr/bin/env python
# coding: utf-8

# # 1.2 Brightway 2 - From Project creation to LCA

# This is a continuation of the [Tutorial 1](1-BW_project_creation_and_first_LCA.ipynb). The reason to chamnge notebooks is to run it with [Brightway 2.5](https://github.com/brightway-lca/brightway25). Technically they can run together, but I had some library conflicts so I prefer to have both kernels separate. Let's move on with [Chris's Seminar](https://github.com/PoutineAndRosti/Brightway-Seminar-2017/blob/master/Day%201%20AM/2%20-%20BW%20structure%20and%20first%20LCAs.ipynb), I want to remind you that he uses ecoinvent LCI database, since I do not have it, I will be using `'US EEIO 1.1'` and the default `'biosphere3'` databases.

# In[1]:


import bw2data as bd
import bw2calc as bc
import bw2io as bi
import bw_processing as bwp

import matrix_utils as mu
import numpy as np
import seaborn as sb
import pandas as pd
import os               # to use "operating system dependent functionality"


# In[2]:


bd.projects.set_current('MW_1_5')


# In[16]:


if 'biosphere3' == bd.databases:
    print('Biosphere already in the project!')
else:
    bi.bw2setup()


# In[17]:


if 'US EEIO 1.1' == bd.databases:
    print('US EEIO 1.1 already in the project!')
else:
    bi.useeio11()


# In[27]:


# if 'forwast' in bd.databases:
#     print('Forwast already in the project!')
# else:
#     fw = SingleOutputEcospold1Importer("/Users/cmutel/Downloads/FORWAST-ecospold1", "forwast")
# ei.apply_strategies()
# ei.statistics()


# In[24]:


bd.databases


# Save both databases:

# In[36]:


bio = bd.Database('biosphere3')
useeio = bd.Database('US EEIO 1.1')
data_codes = (bio, useeio);
[print('The {} database has {} datapoints.'.format(data_codes[it].name,len(data_codes[it]))) for it in range(len(data_codes))];


# I am going to select an activity:

# In[47]:


glass = [act for act in useeio if 'glass' in act['name']][0]


# In[48]:


glass


# We can iterate over its emission/resource and technosphere exchanges:

# In[67]:


print('There are',str(len([exc for exc in glass.technosphere()])),'technosphere exchanges.')
print('There are',str(len([exc for exc in glass.biosphere()])),'biosphere exchanges.')
print('There are',str(len([exc for exc in glass.exchanges()])),'total exchanges.')




# There is one missing, which I assume it is glass itself.

# Let's learn more about a technosphere exchange!

# In[68]:


glass_tech_exch = [exc for exc in glass.technosphere()][0]
glass_tech_exch


# In[70]:


type(glass_tech_exch) # It is a proxy!


# In[82]:


print('Amount: ', glass_tech_exch.amount) # Amount, or weight of the edge
print('Input: ', glass_tech_exch.input) # Activity the exchange stems from
print('Output: ', glass_tech_exch.output) # Activity the exchange terminates in
print('As dictionary: ', glass_tech_exch.as_dict) # Exchange as a dictionary


# **Exercise:** Assign a biosphere flow to a variable, and check the following:
# 
# * Is the output the same as for the technosphere exchange?
# * From what database does the biosphere exchange come from?
# * What is the amount of the exchange (i.e. the weight of the edge connecting the two activities)?
# 
# *NOTE:* If you get a `list index out of range error` when trying to subscript your list comprehension, it means your list comprehension is empty, i.e. that there are no biosphere flows associated with the activity.
# 

# In[90]:


bio_rand_flow = [bio_flow for bio_flow in glass.biosphere()][0]
bio_rand_flow


# In[92]:


bio_rand_flow.output # Is the output the same as for the technosphere exchange? 


# In[95]:


bio_rand_flow.output == glass_tech_exch.output # YES IT IS!


# In[97]:


bio_rand_flow.input.key[0] # It comes from the 'US EEIO 1.1'


# In[99]:


bio_rand_flow['amount'] # Amount of the exchange


# #### Loaded LCI databases

# It is possible to load the entire database into a dictionary.
# This greatly speeds up work if you need to iterate over all activities or exchanges. The resulting object is quite big, so you should do this only if the gain in efficiency is worth it.
# 

# In[101]:


useeio_loaded = useeio.load()
len(useeio_loaded)


# ### 1.2 1 First LCA

# Brightway has a so-called `LCA` object.
# It is instantiated using `LCA(args)`.
# The only required argument is a **functional unit**, described by a dictionary with keys = activities and values = amounts ([more here](https://2.docs.brightway.dev/lca.html?highlight=functional+unit#specifying-a-functional-unit)).
# A second argument that is often passed is an LCIA method, passed using the method tuple.

# Let's create our first LCA object using our random activity and our IPCC method (which we need to select again!).

# In[141]:


new_act = [act for act in useeio if 'Veneer' in act['name']][0] # Here I selected wood because I felt like it
new_act


# In[142]:


ipcc2013 = [m for m in bd.methods if 'IPCC' in str(m) 
                                 and ('2013') in str(m) 
                                 and 'GWP 100' in str(m) 
                                 and 'climate change' in str(m) 
                                 and 'no LT' not in str(m)][0] # You need to add the [0] to get the tuple selection!


# In[143]:


ipcc2013


# In[144]:


functional_unit = {new_act:1} # We selected 1 kg of glass here


# In[145]:


myFirstLCA_quick = bc.LCA(functional_unit, ipcc2013)


# The steps to get to the impact score are as follows:

# In[147]:


myFirstLCA_quick.lci()    # Builds matrices, solves the system, generates an LCI matrix.
myFirstLCA_quick.lcia()   # Characterization, i.e. the multiplication of the elements 
                          # of the LCI matrix with characterization factors from the chosen method
myFirstLCA_quick.score    # Returns the score, i.e. the sum of the characterized inventory


# In[ ]:




