#!/usr/bin/env python
# coding: utf-8

# # My little database JSON-LD import

# ## 1 Import relevant packages

# In[1]:


import bw2data as bd
import bw2calc as bc
import bw2io as bi
import bw_processing
import bw_migrations
from bw2io.importers.json_ld_lcia import JSONLDLCIAImporter

import os
import numpy as np
import pandas as pd


# ## 2 Create/set the working folder

# In[2]:


bd.projects.dir


# In[3]:


bd.projects.set_current('MLD_JSON_001') # Set the project name you want!


# ## 3 Import JSON-LD LCI

# In[4]:


path = '../7_BW2_Importing_USLCI/databases/My_little_database' # For some reason if I use the relative path it throws me an error
mld = bi.importers.JSONLDImporter(
    path, 
    "My_little_dataset_v0", 
    preferred_allocation="PHYSICAL_ALLOCATION"
)


# ### 3.1 Apply strategies to map JSON-LD to Brightway2 schema

# In[5]:


mld.apply_strategies()


# ### 3.2 Check database dictionaries

# In[6]:


bd.databases # As expected, nothing was written.


# ### 3.3 Write the biosphere database

# In[7]:


mld.write_separate_biosphere_database()


# Check that the database was written in the database dictionary.

# In[8]:


bd.databases


# Save the biosphere database in a variable for easy use.

# In[9]:


bio = bd.Database('My_little_dataset_v0 biosphere')


# ### 3.4 Write the technosphere database

# In[10]:


mld.write_database()


# <div class="alert alert-block alert-warning">
# <b>To fix:</b>
#     <li>The importer does not recognize the geolocations.</li>
# </div>

# Check that the database was written in the database dictionary.

# In[11]:


bd.databases


# In[12]:


db = bd.Database('My_little_dataset_v0')


# ## 4 Import the LCIA methods

# In[13]:


mld_methods = bi.importers.JSONLDLCIAImporter(path)


# In[14]:


mld_methods.apply_strategies()


# In[15]:


mld_methods.match_biosphere_by_id('My_little_dataset_v0 biosphere')


# In[16]:


mld_methods.statistics()


# In[17]:


mld_methods.data


# In[18]:


[things['name'] for things in mld_methods.data]


# In[19]:


if [things['name'] for things in mld_methods.data][0] in bd.methods:
    print('Method already loaded!')
else:
    mld_methods.write_methods()


# In[20]:


mld_methods


# In[21]:


bd.databases


# ## 5 Activity querying

# ### 5.1 Check the biosphere activities

# In[22]:


[act for act in bio]


# ### 5.2 And now let's look at the our processes and products:

# In[23]:


[(act.as_dict(), act['unit']) for act in bio]


# In[24]:


[(act, act['type'], act['unit']) for act in db]


# In[25]:


[(act['name'],[exc for exc in act.exchanges()]) for act in db if act['type'] == 'process']


# In[26]:


[(act['name'],[exc for exc in act.exchanges()]) for act in db if act['type'] == 'process']


# ### 5.3 Which ones are processes and which ones are products? Let's also get their codes:

# In[27]:


[(act['name'], act['type'], act['code']) for act in db]


# ### 5.4 Exploring the LCIA methods

# #### 5.4.1 How to manually add a LCIA method
# Before I figured out how to add LCIA methods I wrote them manually, this is how it is done (uncomment if you want to run this).

# In[28]:


bad_flow = [act for act in bio if act['name'] == 'Bad stuff'][0]
bad_flow.as_dict()


# In[29]:


myLCIAdata = [[(bad_flow['database'], bad_flow['code']), 2.0]] # A method list needs: a reference to the flow: tuple (database, 'code')), a characterization factor number, and localization (if no localization is given, 'GLO' is used)
method_key_manual = ('MacIM_manual', 'Global warming')
my_method_manual = bd.Method(method_key_manual)
my_method_manual.validate(myLCIAdata)
my_method_manual.register()
my_method_manual.write(myLCIAdata)


# #### 5.4.2 Search through our JSON-LD imported methods

# In[30]:


bd.methods


# Search works the same as before, we just need to use line comprehension as before.

# In[31]:


[method for method in bd.methods]


# In[32]:


method_key = [method for method in bd.methods][0] # [0] selects the method
method_key


# In[33]:


my_method = bd.Method(method_key)


# In[34]:


my_method.name


# In[35]:


my_method.metadata['unit']


# In[36]:


my_method.load()


# ## 6 Running the LCA!

# ### 6.1 Define the functional unit:
# Our functional unit here is **Impact of assembling 5 bottles**, so we need to select the flow coming out of the `Bottle assembly` activity, i.e. `Bottle`, which is a `product` not a `process`.

# In[37]:


activity = [act for act in db if act['type'] == 'product' and act['name'] == 'Bottle'][0]
activity


# In[38]:


functional_unit = {activity : 50} #Impact of 5 bottles


# ### 6.2 Run the LCA!

# Let's run the LCA with the imported and manually created LCIA method.

# In[39]:


lca = bc.LCA(functional_unit, method_key) 


# In[40]:


lca_manual = bc.LCA(functional_unit, method_key_manual) 


# In[41]:


print(len(dir(lca)))
print(len(dir(lca_manual)))


# In[42]:


lca.lci()   # Builds matrices, solves the system, generates an LCI matrix.
lca_manual.lci()


# In[43]:


print(len(dir(lca)))
print(len(dir(lca_manual)))


# In[44]:


lca.lcia()  # Characterization, i.e. the multiplication of the elements  
            # of the LCI matrix with characterization factors from the chosen method
lca_manual.lcia() 


# In[45]:


print(len(dir(lca)))
print(len(dir(lca_manual)))


# In[46]:


print(lca.score )   # Returns the score, i.e. the sum of the characterized inventory
print(lca_manual.score)


# BEAUTIFUL!

# There is a bug though, if you re-run this code in the same project folder, the lca.score will be 0. I don't know why jet!

# In[ ]:




