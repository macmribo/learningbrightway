#!/usr/bin/env python
# coding: utf-8

# # 1.2 &emsp; Simple LCA

# This is the [second tutorial](https://github.com/massimopizzol/B4B/blob/main/01.1_Simple_LCA.py) based on a .py code Massimo wrote.

# ### Project setup and database creation
# 
# ___

# In[16]:


from brightway2 import *


# Setup the project and check where it is saved:

# In[17]:


list(projects) # How many projects have I hoarded?
projects.set_current('1_2_Massimo')  # I create Massimo and set as current project ~ WEEEE
projects.output_dir # Ahá! There you are...


# Let's create a dummy database:

# In[18]:


t_db = Database("testdb")


# In[19]:


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
    ('testdb', 'Carbon dioxide'):{'name': 'Carbon dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testdb', 'Sulphur dioxide'):{'name': 'Sulphur dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testdb', 'Crude oil'):{'name': 'Crude oil', 'unit':'kg', 'type': 'biosphere'}

    })


# ### LCA calculations
# ___

# Let's find out the scores for 1000 kWh of produced electricity.
# 
# First, we need a reference, thus we need to define ...drum roll... the functional unit!

# In[20]:


functional_unit = {t_db.get("Electricity production") : 1000}


# Now that we have a functional unit we run the LCA function so we can get the LCI (Life Cycle Inventory) by running the lci() function on the LCA object lca.

# In[21]:


lca = LCA(functional_unit) 
lca.lci()
print(lca.inventory)


# I am going to revert the LCA results, so we can visualize them and make some sense of these results. This is not necessary to obtain results!

# In[22]:


rev_act_dict, rev_product_dict, rev_bio_dict = lca.reverse_dict()


# Let's find out the scores for 1000 kWh of produced electricity.
# 
# First, we need a reference, thus we need to define ...*drum roll*...  the __functional unit__! 

# Let's look at the __technology matrix__ to see what this means for easy visualization (worry not, once you get used to this I'll stop doing it!).

# In[23]:


tech_matrix=lca.technosphere_matrix.toarray()
print(tech_matrix)
for r in range(0,tech_matrix.shape[0]):
    for c in range(0,tech_matrix.shape[1]):
        if tech_matrix[r, c]>0:
            print(str(rev_act_dict[c][1])+" supplies "+ str(tech_matrix[r, c])+" of "+str(get_activity(rev_product_dict[r])))
        else:
            print(str(rev_act_dict[c][1])+" uses "+ str(tech_matrix[r, c])+" of "+str(get_activity(rev_product_dict[r])))


# This is the supply array.
# 
# <div class="alert alert-warning">
#       <i class="fa fa-question-circle-o" aria-hidden="true"></i>&nbsp;
#       Figure out what the <code>supply_array</code> is.
# </div>

# In[24]:


supply_array=lca.supply_array.tolist()
print(supply_array)
for r in supply_array:
    print("{} supplies {}".format(rev_product_dict[supply_array.index(r)][1],supply_array[supply_array.index(r)]))


# And now let's explore the __inventory matrix__, which shows which flows are __used__ and __produced__ by each unit process.

# In[25]:


inventory_matrix = lca.inventory.toarray()
print(inventory_matrix)
for r in range(0,inventory_matrix.shape[0]):
    for c in range(0,inventory_matrix.shape[1]):
        if inventory_matrix[r, c]>0:
            print(str(rev_act_dict[c][1])+" emits "+ str(inventory_matrix[r, c])+" "+get_activity(rev_bio_dict[r])["unit"]+" of "+str(rev_bio_dict[r][1]))
        else:
            print(str(rev_act_dict[c][1])+" uses "+ str(inventory_matrix[r, c]*(-1))+" "+get_activity(rev_bio_dict[r])["unit"]+" of "+str(rev_bio_dict[r][1]))


# Let's give imaginary characterization factors to our resource and emission flows:

# In[26]:


myLCIAdata = [[('testdb', 'Carbon dioxide'), 2.0], 
              [('testdb', 'Sulphur dioxide'), 2.0],
              [('testdb', 'Crude oil'), 2.0]]


# 
# 
# <div class="alert alert-warning">
#       <i class="fa fa-question-circle-o" aria-hidden="true"></i>&nbsp;
#       Figure out what Method does with the <code>method_key</code> tuple.
# </div>

# In[27]:


method_key = ('simplemethod', 'imaginaryendpoint', 'imaginarymidpoint')
my_method = Method(method_key)
my_method.validate(myLCIAdata)
my_method.register() 
my_method.write(myLCIAdata)
my_method.load()


# In[28]:


type(method_key)


# In[29]:


lca = LCA(functional_unit, method_key) #run LCA calculations again with method
lca.lci()
lca.lcia()
print(lca.inventory)
print("")
print(lca.characterized_inventory)


# In[41]:


print('The total CO2 kg-eq is: \n', lca.score,'\n') # Score is the total CO2 kg-eq

print('The CO2 kg-eq in each activity is (first row is electricity and second is the fuel): \n', sum(lca.characterized_inventory), '\n') 


# `sum(lca.characterized_inventory)` adds the factors for each production. Electricity: 200 + 20 = 220, and Fuel: -200 + 8 + 40 = 152

# The point with score is that what Chris Mutel calls a method is an "impact category", so he then assumes (correctly) everything is summed up.

# The total score adds the characterized inventory values and calculates the total CO<sub>2</sub> kg-eq production.

# I still don't get the negative values though...

# In[ ]:




