#!/usr/bin/env python
# coding: utf-8

# In[2]:


import brightway2 as bw
# import bw2data as bd
# import bw2calc as bc
# import bw2io as bi
# import bw_processing
# import bw_migrations

import os
import numpy as np
import pandas as pd


# I am going to create the 'My little database' in brightway.
# LCI schema:
# ```
# {
#     Optional("categories"): Any(list, tuple),
#     Optional("location"): object,
#     Optional("unit"): basestring,
#     Optional("name"): basestring,
#     Optional("type"): basestring,
#     Optional("exchanges"): [exchange]
# }
# ```
# Where an exchange is:
# ```
# {
#     Required("input"): valid_tuple,
#     Required("type"): basestring,
#     Required("amount"): Any(float, int),
#     Optional("uncertainty type"): int,
#     Optional("loc"): Any(float, int),
#     Optional("scale"): Any(float, int),
#     Optional("shape"): Any(float, int),
#     Optional("minimum"): Any(float, int),
#     Optional("maximum"): Any(float, int)
# }
# ```
# 

# In[4]:


bw.projects.set_current('MLD_in_bw_2')


# In[5]:


db = bw.Database('My_little_database')


# In[7]:


db


# Remember: Processes and flows are both considered "activities" in Brightway2, the difference is that flows wont have exchanges.
# 
# Notes:
# * Activities always need a name, in a tuple `(database_json_import_name, filename_processes)`, let's see if I use the file .json file name.                      
# *  Category names are inside 'category' under the 'name' item, it is in a list form because you can add sub categories.
# * `'location': 'Djibouti'` locates the location using the whole country name, I will have to check, do I need the country code so everything has the same way of referring to countries? I think I need to call it DJ
# * The `'name'` item is the same as in the JSON-LD.
# *  In JSON-LD, `'units'` are not included here, they are included in the flows, I think this unit is the unit of the reference flow or 'quantitativeReference'
# * Exchanges - They always have to have 'input', 'amount' and 'type' minimum, you know outputs based on the sign, check out bw sign convention https://2.docs.brightway.dev/intro.html#getting-the-signs-right, I also need to see how to specify the reference flow

# In[203]:


db.write({
    # PROCESSES # They always need a name, in a tuple (database_json_import_name, filename_processes), let's see if I use the file .json file name                            
    ('My_little_database', '2fc6deea-6437-4b9f-bf91-89bca44d30f0'): {  
        'category': ['Manufacturers'],  # JSON-LD --> category, category names are insidide 'category' under the 'name' item, it is in a list form because you can add sub categories.
        'location': 'GLO', # This is how JSON calls it, I will have to check, do I need the country code so averything has the same way of referring to countries? I think I need to call it DJ
        'name': 'Plastic manufacturer',    #JSON-LD --> name                                          # Characteristic 1
        'code': '2fc6deea-6437-4b9f-bf91-89bca44d30f0', #JSON-LD --> @id
 #       'type': 'process',
        'unit': 'kg',      # In JSON-LD, units are not included here, they are included in the flows, I think this unit is the unit of the reference flow or 'quantitativeReference'
        'exchanges': [{    # Exchanges - They always have to have 'input', 'amount' and 'type' minimum, you know outputs based on the sign, check out bw sign convention https://2.docs.brightway.dev/intro.html#getting-the-signs-right, the reference flow is especified as 'production'
            'input': ('My_little_database', '62714200-1a0d-43fb-9b48-99df3f233c94'), # Input 1 -> Activity 2 same tuple as the activity, that's how they are linked
            'amount': 1,   # Positive amount in technosphere indicates 'output'                                           
            'name': 'Plastic', #name is not part of the bw schema, let's see if it breaks the code or not
            'type': 'production', # This one is converted to 'production' by mapping 'technosphere' with flowType: 'PRODUCT_FLOW',                                
        }, {
            'input': ('My_little_database', 'cd154d8f-0694-43b2-b4ab-e44101e122bd'),                         
            'amount': 2, # Emissions are positive, and negative emissions will be removing the emission from biosphere (e.g. carbon capture technologies, https://github.com/brightway-lca/brightway2/blob/master/notebooks/Negative%20Biosphere%20flows%20and%20CFs.ipynb)
            'name': 'Bad stuff',
            'type': 'biosphere', 
        }, {
            'input': ('My_little_database', '8849be54-1b13-4d7e-85f6-2297817333f2'),                                
            'amount': -1, # Negative because it is a resource, we 'steal' from earth
            'name': 'Crude oil',
            'type': 'biosphere',
        }]
    },
    ('My_little_database', '7e5ec332-09fd-4706-8373-3f140a539028'): {  
        'category': ['Manufacturers'],  
        'location': 'GLO', 
        'name': 'Stainless steel manufacturer',    
        'code': '7e5ec332-09fd-4706-8373-3f140a539028',
  #      'type': 'process',
        'unit': 'kg',      
        'exchanges': [{    
            'input': ('My_little_database', '3355a1b9-8fbf-40de-b449-ea6399a8a323'), 
            'amount': 1,
            'name': 'Stainless steel',
            'type': 'production', 
        }, {
            'input': ('My_little_database', '7528830a-7344-43be-b484-ac4dc625f272'),                         
            'amount': -1,
            'name': 'Virgin metals',
            'type': 'biosphere',
        }, {
            'input': ('My_little_database', 'cd154d8f-0694-43b2-b4ab-e44101e122bd'),                                
            'amount': 3,
            'name': 'Bad stuff',
            'type': 'biosphere',
        }]
    },
    ('My_little_database', 'fae6799b-7326-452c-92b3-76758bbcac22'): {  
        'category': ['Assemblers'],  
        'location': 'GLO', 
        'name': 'Bottle assembly',    
        'code': 'fae6799b-7326-452c-92b3-76758bbcac22',
   #     'type': 'process',
        'unit': 'number_of_items',      
        'exchanges': [{    
            'input': ('My_little_database', 'b806c2cd-d563-43c4-a0c9-9c7dd5d513d3'), 
            'amount': 1,
            'name': 'Bottle',
            'type': 'production', 
        }, {
            'input': ('My_little_database', '62714200-1a0d-43fb-9b48-99df3f233c94'),                         
            'amount': 0.25,
            'name': 'Plastic',
            'type': 'technosphere',
        }, {
            'input': ('My_little_database', '3355a1b9-8fbf-40de-b449-ea6399a8a323'),                                
            'amount': 0.3,
            'name': 'Stainless steel',
            'type': 'technosphere',
        }, {
            'input': ('My_little_database', 'cd154d8f-0694-43b2-b4ab-e44101e122bd'),                                
            'amount': 0.1,
            'name': 'Bad stuff',
            'type': 'biosphere',
        }]
    },
    # EXCHANGES #Since these are flows, they don't have exchanges.
    ('My_little_database', '62714200-1a0d-43fb-9b48-99df3f233c94'): { 
        'category': ['Technosphere flows', 'Manufacturers'], # To draw these names, I have to map them to categoryPath: 0: 'Technosphere flows', 1: 'Manufacturers'
        'code': '62714200-1a0d-43fb-9b48-99df3f233c94', 
        'name': 'Plastic',
        'type': 'product',
        'location': 'GLO', # I added this one, let's see how it behaves, consider eother changing this for full name or leaving country code as default            
        'unit': 'kg'},
    ('My_little_database', '3355a1b9-8fbf-40de-b449-ea6399a8a323'): {
        'category': ['Technosphere flows', 'Manufacturers'], 
        'name': 'Stainless steel',
        'type': 'product',
        'location': 'GLO',
        'unit': 'kg'},    
    ('My_little_database', 'b806c2cd-d563-43c4-a0c9-9c7dd5d513d3'): {
        'category': ['Technosphere flows', 'Assemblers'],
        'name': 'Bottle',
        'type': 'product',
        'location': 'GLO',
        'unit': 'number_of_items'}, 
    ('My_little_database', '7528830a-7344-43be-b484-ac4dc625f272'): {
        'category': ['Elementary flows', 'resources'],
        'name': 'Virgin metals',
        'type': 'biosphere',
        'location': 'GLO',
        'unit': 'kg'},          
    ('My_little_database', '8849be54-1b13-4d7e-85f6-2297817333f2'): {
        'category': ['Elementary flows', 'resources'],
        'name': 'Crude oil',
        'type': 'biosphere',
        'location': 'GLO',
        'unit': 'kg'}, 
    ('My_little_database', 'cd154d8f-0694-43b2-b4ab-e44101e122bd'): {
        'category': ['Elementary flows', 'emissions'], 
        'name': 'Bad stuff',
        'type': 'biosphere',
        'location': 'GLO',
        'unit': 'kg'}, 
})


# Let's define the functional unit: We want to know how much GWP does the assembly of 5 bottles produce.First we start by searching the unit process of interest `Bottle prodcution`:

# In[204]:


bottellita = db.search('Bottle')[0]
bottellita


# In[205]:


activity.exchanges()


# In[211]:


functional_unit = {db.search('Bottle')[0] : 5.0}


# Let's now try to add some lcia methods... [source](https://2.docs.brightway.dev/intro.html#lcia-method-documents), stackoverflow question about doing a manual input of lcia methods [here](https://stackoverflow.com/questions/41466234/create-very-simple-lcia-method-in-brightway2).

# In[212]:


myLCIAdata = [[(u'My_little_database', u'cd154d8f-0694-43b2-b4ab-e44101e122bd'), 2, u'GLO']] # A method list needs: a reference to the flow: tuple (database, 'code')), a characterization factor number, and localization (if no localization is given, 'GLO' is used)
method_key = ('MacIM', 'Global warming', 'total')
my_method = bw.Method(method_key)
my_method.validate(myLCIAdata)
my_metadata = {"unit": "kg CO2 eq"}
my_method.register(**my_metadata)
my_method.write(myLCIAdata)


# In[213]:


my_method.metadata


# Now we are ready to run the LCA!
# 

# In[214]:


lca = bw.LCA(functional_unit, method_key) #run LCA calculations again with method
lca.lci() # If it is not square, it fails here. Here it fails because Plastic and aluminium are in kg and bottle is is units. It is important to fix this because we won't always have square matrices or same units.
lca.lcia()
lca.score
print(lca.inventory)


# In[215]:


lca.score # If I add location, it braks the scores and it shows 0.0


# Where is the geolocation dictionary?

# In[ ]:





# Questions:
# * How does it know the allocation? Does it always generalize it?
# * Figure out how it maps country codes
# * Does the negative sign indicated resource?
# * How do I import the LCIA methods and categories?
# * Fix the non-unitary issue. 
# 
