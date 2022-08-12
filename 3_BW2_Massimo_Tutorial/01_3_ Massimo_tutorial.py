#!/usr/bin/env python
# coding: utf-8

# # 1.3 &emsp; Simple LCA - Alternative

# This [tutorial](https://github.com/massimopizzol/B4B/blob/main/01.2_Simple_LCA_alternative%20version.py) is the same as in the previous version (Simple_LCA.py) but this time I create two databases, one for product flows and one for environmental flows. Note how the two are linked and that you can't creatt the first without 
# creating the second first.
# 
# Here I won't be giving as many notes regarding the steps until I reach the different part. Lazy.

# In[9]:


from brightway2 import *


# In[10]:


projects.report()


# In[11]:


projects.set_current('1_3_Massimo')


# Do you see this number one next to the project 1.1 and 1.2? Remember, that's the amount of databases linked to the project. Our new one says 0! Let's change this.

# In[12]:


t_db = Database("testdb")


# In[13]:


t_db.write({
    ("testdb", "Electricity production"):{
        'name':'Electricity production',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('testdb', 'Fuel production'),
                'amount': 2,
                'unit': 'kg',
                'type': 'technosphere'
            },{
                'input': ('biosphere', 'Carbon dioxide'), #this is the KEY line, put biosphere to show that the flow is from the other database.
                'amount': 1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('biosphere', 'Sulphur dioxide'),
                'amount': 0.1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Electricity production'), #important to write the same process name in output
                'amount': 10,
                'unit': 'kWh',
                'type': 'production'
            }]
        },
    ('testdb', 'Fuel production'):{
        'name': 'Fuel production',
        'unit': 'kg',
        'exchanges':[{
                'input': ('biosphere', 'Carbon dioxide'),
                'amount': 10,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('biosphere', 'Sulphur dioxide'),
                'amount': 2,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('biosphere', 'Crude oil'),
                'amount': -50,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Fuel production'),
                'amount': 100,
                'unit': 'kg',
                'type': 'production'
            }]
    }})


# See the differences between this database and the one from the previous tutorial? We have **two**  main differences:
# 1) The `input` entry is written as a tuple, where the first term is the database we are connecting with, and the second one is the name of the flow.
# 2) We do not add flows to this database! We will create a separate flow `biosphere` database!!

# In[14]:


bs_db = Database('biosphere')
bs_db.write({
    ('biosphere', 'Carbon dioxide'):{'name': 'Carbon dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('biosphere', 'Sulphur dioxide'):{'name': 'Sulphur dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('biosphere', 'Crude oil'):{'name': 'Crude oil', 'unit':'kg', 'type': 'biosphere'}
    })


# Now we run the same code lines as the previous tutorial:

# In[15]:


functional_unit = {t_db.get("Electricity production") : 1000}
lca = LCA(functional_unit) 
lca.lci()
myLCIAdata = [[('biosphere', 'Carbon dioxide'), 2.0], 
              [('biosphere', 'Sulphur dioxide'), 2.0],
              [('biosphere', 'Crude oil'), 2.0]]

method_key = ('simplemethod', 'imaginaryendpoint', 'imaginarymidpoint')
my_method = Method(method_key)
my_method.validate(myLCIAdata)
my_method.register() 
my_method.write(myLCIAdata)
my_method.load()

lca = LCA(functional_unit, method_key) #run LCA calculations again with method
lca.lci()
lca.lcia()
print("Here is the inventory adjusted to the functional unit:")
print(lca.inventory)
print("Et voilà, the characterized inventory is multiplied by the CF we defined in the myLCIAdata (x2):")
print(lca.characterized_inventory)


# In[16]:


projects.report()


# Now 1_3_Massimo has two datasets! Because we made them! :D

# In[ ]:




