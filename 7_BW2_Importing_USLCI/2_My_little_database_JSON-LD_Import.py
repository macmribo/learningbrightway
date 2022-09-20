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


bd.projects.set_current('MLD_JSON_2')


# #### Import JSON-LD:

# In[4]:


path = '../7_BW2_Importing_USLCI/databases/My_little_database' # For some reason if I use the relative path it throws me an error
mld = bi.importers.JSONLDImporter(
    path, 
    "My_little_dataset_v0", 
    preferred_allocation="PHYSICAL_ALLOCATION"
)


# #### Apply strategies to map JSON-LD to Brightway2 schema:

# In[5]:


mld.apply_strategies()


# #### Check database dictionaries:

# In[6]:


bd.databases # As expected, nothing was written.


# #### Write the biosphere database:

# In[7]:


mld.write_separate_biosphere_database()


# In[8]:


bd.databases


# #### Write the technosphere database:

# In[9]:


bio = bd.Database('My_little_dataset_v0 biosphere')


# In[10]:


mld.write_database()


# <div class="alert alert-block alert-warning">
# <b>To fix:</b>
#     <li>The importer does not recognize the geolocations.</li>
#     <li>The importer does not import the LCIA methods. <i>Hint:</i> Check bw2setup() function, this one loads LCIAs and biosphere flows.</li>
# </div>

# In[11]:


bd.databases


# In[12]:


db = bd.Database('My_little_dataset_v0')


# #### Let's look at the biosphere flows:

# In[13]:


[act for act in bio]


# #### And now let's look at the our processes and products:

# In[14]:


[(act.as_dict(), act['unit']) for act in bio]


# In[15]:


[(act, act['type'], act['unit']) for act in db]


# In[16]:


[(act['name'],[exc for exc in act.exchanges()]) for act in db if act['type'] == 'process']


# In[17]:


[(act['name'],[exc for exc in act.exchanges()]) for act in db if act['type'] == 'process']


# #### Which ones are processes and which ones are products? Let's also get their codes:

# In[18]:


[(act['name'], act['type'], act['code']) for act in db]


# ### Let's manually add a LCIA method
# This importer does not recognize the LCIA methods, therefore we need to add them manually. I will debug this later!
# 
# First, let's find the `Bad stuff` biosphere flow.

# In[19]:


bad_flow = [act for act in bio if act['name'] == 'Bad stuff'][0]
bad_flow.as_dict()


# In[20]:


myLCIAdata = [[(bad_flow['database'], bad_flow['code']), 2.0]] # A method list needs: a reference to the flow: tuple (database, 'code')), a characterization factor number, and localization (if no localization is given, 'GLO' is used)
method_key = ('MacIM', 'Global warming', 'total')
my_method = bd.Method(method_key)
my_method.validate(myLCIAdata)
my_method.register()
my_method.write(myLCIAdata)


# #### Now we define a functional unit:
# This one might be a bit counterintuitive, our functional unit here is **Impact of assembling 5 bottles**, intuintively one would select the activity, but bw2 selects the flow coming out of the `Bottle assembly` activity (i.e. `Bottle`, which is a `product` not a `process`).

# In[21]:


activity = [act for act in db if act['name'] == 'Bottle'][0]


# In[22]:


functional_unit = {activity : 5} #Impact of 5 bottles


# #### Run the LCA!

# In[23]:


lca = bc.LCA(functional_unit, method_key) 


# In[24]:


lca.lci()   # Builds matrices, solves the system, generates an LCI matrix.


# In[27]:


lca2 = bc.LCA(functional_unit, method_key) 


# In[29]:


len(dir(lca2))


# In[30]:


len(dir(lca))


# In[31]:


lca.lcia()  # Characterization, i.e. the multiplication of the elements  
            # of the LCI matrix with characterization factors from the chosen method


# In[32]:


lca.score    # Returns the score, i.e. the sum of the characterized inventory


# In[35]:


lca2.lcia()


# In[38]:


dir(lca2)


# Scoooooooore!!!
