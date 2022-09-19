#!/usr/bin/env python
# coding: utf-8

# ## My little database JSON-LD import

# #### Import relevant packages

# In[1]:


import bw2data as bd
import bw2calc as bc
import bw2io as bi
import bw_processing
import bw_migrations

import os
import numpy as np
import pandas as pd


# #### Create/set the working folder:

# In[2]:


bd.projects.dir


# In[3]:


bd.projects.set_current('MLD_JSON_0')


# #### Import JSON-LD:

# In[6]:


path = '/Users/mmendez/Documents/Postdoc/Software_dev/Brightway/Brightway_US/US_LCI_BW_Project/notebooks/databases/My_little_database/JSON-LD/My_little_database'
mld = bi.importers.JSONLDImporter(
    path, 
    "My_little_dataset_v0", 
    preferred_allocation="PHYSICAL_ALLOCATION"
)


# #### Apply strategies to map JSON-LD to Brightway2 schema:

# In[6]:


mld.apply_strategies()


# #### Check database dictionaries:

# In[7]:


bd.databases # As expected, nothing was written.


# #### Write the biosphere database:

# In[8]:


mld.write_separate_biosphere_database()


# In[9]:


bd.databases


# #### Write the technosphere database:

# In[10]:


bio = bd.Database('My_little_dataset_v0 biosphere')


# In[11]:


mld.write_database()


# <div class="alert alert-block alert-warning">
# <b>To fix:</b>
#     <li>The importer does not recognize the geolocations.</li>
#     <li>The importer does not import the LCIA methods. <i>Hint:</i> Check bw2setup() function, this one loads LCIAs and biosphere flows.</li>
# </div>

# In[12]:


bd.databases


# In[13]:


db = bd.Database('My_little_dataset_v0')


# #### Let's look at the biosphere flows:

# In[14]:


[act for act in bio]


# #### And now let's look at the our technosphere processes and products:

# In[15]:


[act for act in db]


# #### Which ones are processes and which ones are products? Let's also get their codes:

# In[16]:


[(act['name'], act['type'], act['code']) for act in db]


# ### Let's manually add a LCIA method
# This importer does not recognize the LCIA methods, therefore we need to add them manually. I will debug this later!
# 
# First, let's find the `Bad stuff` biosphere flow.

# In[17]:


bad_flow = [act for act in bio if act['name'] == 'Bad stuff'][0]
bad_flow.as_dict()


# In[18]:


myLCIAdata = [[(bad_flow['database'], bad_flow['code']), 2.0]] # A method list needs: a reference to the flow: tuple (database, 'code')), a characterization factor number, and localization (if no localization is given, 'GLO' is used)
method_key = ('MacIM', 'Global warming', 'total')
my_method = bd.Method(method_key)
my_method.validate(myLCIAdata)
my_method.register()
my_method.write(myLCIAdata)


# #### Now we define a functional unit:
# This one might be a bit counterintuitive, our functional unit here is **Impact of assembling 5 bottles**, intuintively one would select the activity, but bw2 selects the flow coming out of the `Bottle assembly` activity (i.e. `Bottle`, which is a `product` not a `process`).

# In[19]:


activity = [act for act in db if act['name'] == 'Bottle'][0]


# In[20]:


functional_unit = {activity : 5}


# #### Run the LCA!

# In[21]:


lca = bc.LCA(functional_unit, method_key) 
lca.lci() 
lca.lcia()
lca.score
print(lca.inventory)


# In[22]:


lca.score


# In[ ]:





# In[ ]:





# In[23]:


mld.data


# In[ ]:




