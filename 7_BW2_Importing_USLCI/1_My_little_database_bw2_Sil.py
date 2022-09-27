#!/usr/bin/env python
# coding: utf-8

# In[1]:


import brightway2 as bw
import os
import numpy as np
import pandas as pd


# In[2]:


bw.projects.set_current('MLD_SO')


# In[ ]:


#bw.bw2setup()


# In[3]:


bw.databases


# In[4]:


db = bw.Database('My_little_database')
bio = bw.Database('my_biosphere')


# In[5]:


# FLows
flows = {('my_biosphere', '7528830a-7344-43be-b484-ac4dc625f272'): {
        'category': ['Elementary flows', 'resources'],
        'name': 'Virgin metals',
        'type': 'biosphere',
        'location': 'GLO',
        'unit': 'kg'},

        ('my_biosphere', '8849be54-1b13-4d7e-85f6-2297817333f2'): {
        'category': ['Elementary flows', 'resources'],
        'name': 'Crude oil',
        'type': 'biosphere',
        'location': 'GLO',
        'unit': 'kg'},

         ('my_biosphere', 'cd154d8f-0694-43b2-b4ab-e44101e122bd'): {
        'category': ['Elementary flows', 'emissions'], 
        'name': 'Bad stuff',
        'type': 'biosphere',
        'location': 'GLO',
        'unit': 'kg'}}


# In[18]:


# PROCESS
processes = { ('My_little_database', '2fc6deea-6437-4b9f-bf91-89bca44d30f0'): {  
        'name': 'Plastic manufacturer',    #JSON-LD --> name                                          # Characteristic 1
        'reference product':'Plastic',
        'unit': 'kg',      # In JSON-LD, units are not included here, they are included in the flows, I think this unit is the unit of the reference flow or 'quantitativeReference'
        'location': 'GLO', # This is how JSON calls it, I will have to check, do I need the country code so averything has the same way of referring to countries? I think I need to call it DJ
        'category': ['Manufacturers'],  # JSON-LD --> category, category names are insidide 'category' under the 'name' item, it is in a list form because you can add sub categories.
        'code': '2fc6deea-6437-4b9f-bf91-89bca44d30f0', #JSON-LD --> @id
 #       'type': 'process',
        'exchanges': [{    # Exchanges - They always have to have 'input', 'amount' and 'type' minimum, you know outputs based on the sign, check out bw sign convention https://2.docs.brightway.dev/intro.html#getting-the-signs-right, the reference flow is especified as 'production'
            'name': 'Plastic manufacturer', #name is not part of the bw schema, let's see if it breaks the code or not
            'product': 'Plastic',
            'input': ('My_little_database','2fc6deea-6437-4b9f-bf91-89bca44d30f0'), # Input 1 -> Activity 2 same tuple as the activity, that's how they are linked
            'amount': 1,   # Positive amount in technosphere indicates 'output'                                           
            'type': 'production', # This one is converted to 'production' by mapping 'technosphere' with flowType: 'PRODUCT_FLOW',                                
        }, {
            'input': ('my_biosphere', 'cd154d8f-0694-43b2-b4ab-e44101e122bd'),                         
            'amount': 2, # Emissions are positive, and negative emissions will be removing the emission from biosphere (e.g. carbon capture technologies, https://github.com/brightway-lca/brightway2/blob/master/notebooks/Negative%20Biosphere%20flows%20and%20CFs.ipynb)
            'name': 'Bad stuff',
            'type': 'biosphere', 
        }, {
            'input': ('my_biosphere', '8849be54-1b13-4d7e-85f6-2297817333f2'),                                
            'amount': -1, # Negative because it is a resource, we 'steal' from earth
            'name': 'Crude oil',
            'type': 'biosphere',
        }]
    },

    ('My_little_database', '7e5ec332-09fd-4706-8373-3f140a539028'): {  
        'name': 'Stainless steel manufacturer',    
        'reference product':'Stainless steel',
        'category': ['Manufacturers'],  
        'location': 'GLO', 
        'code': '7e5ec332-09fd-4706-8373-3f140a539028',
  #      'type': 'process',
        'unit': 'kg',      
        'exchanges': [{    
            'name': 'Stainless steel manufacturer',
            'product': 'Stainless steel',
            'input': ('My_little_database', '7e5ec332-09fd-4706-8373-3f140a539028'), 
            'amount': 1,
            'type': 'production', 
        }, {
            'input': ('my_biosphere', '7528830a-7344-43be-b484-ac4dc625f272'),                         
            'amount': -1,
            'name': 'Virgin metals',
            'type': 'biosphere',
        }, {
            'input': ('my_biosphere', 'cd154d8f-0694-43b2-b4ab-e44101e122bd'),                                
            'amount': 3,
            'name': 'Bad stuff',
            'type': 'biosphere',
        }]
    },

    ('My_little_database', 'fae6799b-7326-452c-92b3-76758bbcac22'): {  
        'name': 'Bottle assembly',    
        'reference product':'Bottle',
        'category': ['Assemblers'],  
        'location': 'GLO', 
        'code': 'fae6799b-7326-452c-92b3-76758bbcac22',
   #     'type': 'process',
        'unit': 'number_of_items',      
        'exchanges': [{    
            'name': 'Bottle assembly',
            'product': 'Bottle',
            'input': ('My_little_database', 'fae6799b-7326-452c-92b3-76758bbcac22'), 
            'amount': 1,
            'type': 'production', 
        }, {
            'input': ('My_little_database', '2fc6deea-6437-4b9f-bf91-89bca44d30f0'),                         
            'amount': 0.25,
            'name': 'Plastic',
            'type': 'technosphere',
        }, {
            'input': ('My_little_database', '7e5ec332-09fd-4706-8373-3f140a539028'),                                
            'amount': 0.3,
            'name': 'Stainless steel',
            'type': 'technosphere',
        }, {
            'input': ('my_biosphere', 'cd154d8f-0694-43b2-b4ab-e44101e122bd'),                                
            'amount': 1,
            'name': 'Bad stuff',
            'type': 'biosphere',
        }]
    }}


# In[19]:


bio.write(flows)


# In[20]:


db.write(processes)


# In[21]:


bottellita = db.search('Bottle')[0]
bottellita


# In[22]:


functional_unit = {db.search('Bottle')[0] : 5.0}
functional_unit


# In[23]:


myLCIAdata = [[(u'my_biosphere', u'cd154d8f-0694-43b2-b4ab-e44101e122bd'), 2, u'GLO']] # A method list needs: a reference to the flow: tuple (database, 'code')), a characterization factor number, and localization (if no localization is given, 'GLO' is used)
method_key = ('MacIM', 'Global warming', 'total')
my_method = bw.Method(method_key)
my_method.validate(myLCIAdata)
my_metadata = {"unit": "kg CO2 eq"}
my_method.register(**my_metadata)
my_method.write(myLCIAdata)


# In[24]:


my_method.metadata


# In[25]:


lca = bw.LCA(functional_unit, method_key) #run LCA calculations again with method


# In[26]:


lca.lci() 


# In[27]:


lca.lcia()
lca.score
print(lca.inventory)


# In[16]:


lca.score 


# In[17]:


bw.databases


# Questions:
# 
# * Figure out how it maps country codes. WCheckout the geocollection dictionary.
# 
# 

# In[ ]:




