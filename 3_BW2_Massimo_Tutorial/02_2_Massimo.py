#!/usr/bin/env python
# coding: utf-8

# # 2.2 &emsp; Simple LCA — Co-products

# Here is the original [code](https://github.com/massimopizzol/B4B/blob/main/02.2_Simple_LCA_co_products.py)!
# Let's set up the project as we have done before, this time we will be adding more spice to our database adding heat production (yay!)

# In[4]:


from brightway2 import *
projects.set_current('2_2_Massimo')


# In[5]:



t_db1 = Database("testdb")

t_db1.write({
    ("testdb", "Electricity production"):{
        'name':'Electricity production',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('testdb', 'Fuel production'),
                'amount': 2,
                'unit': 'kg',
                'type': 'technosphere'
            },{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 0.1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Electricity production'), #important to write the same process name in output
                'amount': 10,
                'unit': 'kWh',
                'type': 'production'
            },{
                'input': ('testdb', 'Heat production'),
                'amount': -3,
                'unit': 'MJ',
                'type': 'technosphere'
            }]
        },
    ('testdb', 'Fuel production'):{
        'name': 'Fuel production',
        'unit': 'kg',
        'exchanges':[{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 10,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 2,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Crude oil'),
                'amount': -50,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Fuel production'),
                'amount': 100,
                'unit': 'kg',
                'type': 'production'
            }]
        },
    ('testdb', 'Heat production'):{
        'name': 'Heat production',
        'unit': 'MJ',
        'exchanges':[{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 10000, # some exaggerated nr...
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Heat production'),
                'amount': 3,
                'unit': 'MJ',
                'type': 'production'
            }]
        },
    ('testdb', 'Carbon dioxide'):{'name': 'Carbon dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testdb', 'Sulphur dioxide'):{'name': 'Sulphur dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testdb', 'Crude oil'):{'name': 'Crude oil', 'unit':'kg', 'type': 'biosphere'}

    })


# In[6]:



t_db2 = Database("testdb")

t_db2.write({
    ("testdb", "Electricity production"):{
        'name':'Electricity production',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('testdb', 'Fuel production'),
                'amount': 2,
                'unit': 'kg',
                'type': 'technosphere'
            },{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 0.1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Electricity production'), #important to write the same process name in output
                'amount': 10,
                'unit': 'kWh',
                'type': 'production'
            },{
                'input': ('testdb', 'Heat production'),
                'amount': 3,
                'unit': 'MJ',
                'type': 'substitution'  # Check this out! a new type!!
            }]
        },
    ('testdb', 'Fuel production'):{
        'name': 'Fuel production',
        'unit': 'kg',
        'exchanges':[{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 10,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 2,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Crude oil'),
                'amount': -50,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Fuel production'),
                'amount': 100,
                'unit': 'kg',
                'type': 'production'
            }]
        },
    ('testdb', 'Heat production'):{
        'name': 'Heat production',
        'unit': 'MJ',
        'exchanges':[{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 10000, # some exaggerated number to see how this affect
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Heat production'),
                'amount': 3,
                'unit': 'MJ',
                'type': 'production'
            }]
        },
    ('testdb', 'Carbon dioxide'):{'name': 'Carbon dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testdb', 'Sulphur dioxide'):{'name': 'Sulphur dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testdb', 'Crude oil'):{'name': 'Crude oil', 'unit':'kg', 'type': 'biosphere'}

    })


# These two dataset are very similar, but not the same:

# In[8]:


t_db1 == t_db2


# See? And you did not believe me. If you look closely, you will see that the first dataset adds 3 MJ of heat as `'type': 'substitution'` as `Electricity production` exchange. Whereas the second database adds -3 MJ of heat as `'type': 'technosphere'`. Let's check what are the differences.

# Let's create our LCA method. You already know how this works!

# In[9]:


myLCIAdata = [[('testdb', 'Carbon dioxide'), 2.0], 
              [('testdb', 'Sulphur dioxide'), 2.0],
              [('testdb', 'Crude oil'), 2.0]]

method_key = ('simplemethod', 'imaginaryendpoint', 'imaginarymidpoint')
my_method = Method(method_key)
my_method.validate(myLCIAdata)
my_method.register() 
my_method.write(myLCIAdata)
my_method.load()


# And now the fun part!!! To the comparison chamber!

# In[11]:


functional_unit1 = {t_db1.get("Electricity production") : 1000}
lca1 = LCA(functional_unit1, method_key) 
lca1.lci()
lca1.lcia()
print(lca1.inventory)
print(" ")
print(lca1.score)


# In[12]:


functional_unit2 = {t_db1.get("Electricity production") : 1000}
lca2 = LCA(functional_unit2, method_key) 
lca2.lci()
lca2.lcia()
print(lca2.inventory)
print(" ")
print(lca2.score)


# In[13]:


lca1.score == lca2.score


# MWAHAHAHA!! I tricked you! They are exactly the same! So... what is the difference between setting the heat exchange type as `'type': 'substitution'` and `'type': 'technosphere'`?

# No $%#@@% clue.

# In[ ]:




