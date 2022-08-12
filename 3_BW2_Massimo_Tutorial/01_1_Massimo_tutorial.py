#!/usr/bin/env python
# coding: utf-8

# # 1.1 &emsp; Creating a project and navigating though matrices and arrays

# This notebook intends to run Brightway2 based on the data from Hope's article. The intention is to learn Brightway2 and to compare results. I followed the tutorials by [Massimo Pizzol](https://github.com/massimopizzol/B4B).

# ### Let's get things started setting up the project!

# As with any Python package, let's start by importing the package of interest, `brightway2`. You may see import as bw in other tutorials, is comfortable so you don't have to add bw.SOMETHING  before calling a method.

# In[1]:


from brightway2 import *


# To check where the projects are saved, you can do it with the following command:

# In[2]:


projects.output_dir # Check were the projects path is.


# Here we see a bunch of folders ../.../Brightway3 and then `default.abunchofnumbers`, this is because when you run brightway2 for the first time in the kernel, it automatically places you in a `default` project folder. You can also check which folder you are in by typing this beautiful line:

# In[3]:


projects.current


# Magic! But, is there a way to check if we have more projects stored? OF COURSE. To list all the projects created you have two ways:

# In[4]:


projects.report() # See the projects already created.


# In[5]:


list(projects) # Another way!


# As you can see `.report()` gives you more information, more specifically, it gives you the amount of databases stored in each project!
# 
# Each project can have none, one or many databases inside. You can also check how many database dictionaries are inside the project you are already in (in this case `default`) you just call `databases`.

# In[6]:


databases # Check the database dictionaries stored in the project.


# Default is a pretty generic name, let's create our own project! 

# In[7]:


projects.set_current('1_1_Massimo') # Set the desired project, if it does not exist, it will create one.


# In[8]:


projects.output_dir # Check the directory where your project is stored.


# What an original name huh? Now, how can we play with projects a little more? Oh yeah! Copying and deleting projects!

# Let's make a copy of this project (you need to be inside the project you want to copy, to copy it!):

# In[9]:


projects.current # Double checking we are inside the project we want to make a copy of!


# In[10]:


projects.copy_project('la_copia')


# In[11]:


projects.report()


# Let's delete a project just for fun.

# In[12]:


projects.delete_project("la_copia", delete_dir=True) 


# <div class="alert alert-warning">
#       <i class="fa fa-exclamation-triangle" aria-hidden="true"></i>&nbsp;
#       If we don't set the argument <code>delete_dir=True</code>, Brightway won't delete the project completely. Meaning that, if you try to name a file with the same name, it will throw an error. You can see this by navigating to the Brightway3 projects path. The only thing that deleting without `delete_dir=True` does, is to remove it from the projects list. Also! If you want to rename a project, you need to copy the project you want to rename with a new name and the delete the other one. 
# </div>
# 
# 
# 

# Let's also pay attention to the fact that after deleting the copy, it took us to the default project folder. This is because when you copy a project, it automatically switches projects to the copied one, and when you delete it, it 'kicks you out'. EVERYTHING MAKES SENSE, HOORAY! 
# 
# Enough.  Let's go back to `1_1_Massimo`.

# ### Making a dataset

# In[33]:


projects.set_current('1.1_Massimo')


# In[34]:


projects.current


# Let's create a dataset!

# In[35]:


t_db = Database("testdb")


# Let's fill our dataset with two dummy unit processes and their respective exchanges (flows). Here is a diagram of what we will be adding to the dataset:
# 
# ![PROJECT:](images/massimo_example.jpg)
# 
# Cool huh? For further information about the vocabulary used, please refer to [BW_Manual](BW_Manual.ipynb), in there you can find a glossary with the definitions.

# In[36]:


t_db.write({
    ("testdb", "Electricity production"):{
        'name':'Electricity, low voltage',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('testdb', 'Fuel production'),
                'amount': 2,
                'unit': 'kg',
                'type': 'technosphere' # Technosphere types are inputs for the unit process
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
                'type': 'production' # Production is the output
            }]
        },
    ('testdb', 'Fuel production'):{
        'name': 'Refined fuel',
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
                'amount': -50, # Removal of oil from the natural environment so it is -
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Fuel production'),
                'amount': 1,
                'unit': 'kg',
                'type': 'production'
            }]
    },
    ('testdb', 'Carbon dioxide'):{            # These are the flows: CO2, SO2 and crude oil.
        'name': 'Carbon dioxide', 
        'unit':'kg', 
        'type': 'biosphere'}, 
    ('testdb', 'Sulphur dioxide'):{
        'name': 'Sulphur dioxide', 
        'unit':'kg', 
        'type': 'biosphere'},
    ('testdb', 'Crude oil'):{
        'name': 'Crude oil', 
        'unit':'kg', 
        'type': 'biosphere'}

    })


# We can check out activities using the method `.get()`.

# In[38]:


t_db.get('Fuel production')


# ### Let's run the LCA!

# In[39]:


functional_unit = {t_db.get("Electricity production") : 1}
lca = LCA(functional_unit) 
lca.lci()


# Let's reverse dictionary to return the row or column number of matrices and arrays that correspond to an activity, product, or elementary flow. This is NOT necessary for the calculations, is for visualization purposes mainly!

# In[40]:


rev_act_dict, rev_product_dict, rev_bio_dict = lca.reverse_dict()
print(rev_act_dict)


# `rev_act_dictrev_act_dict` stores the activities!

# In[41]:


print("Col. num."+ " " + "Activity")
[print(str(k)+" " + rev_act_dict[k][1]) for k in rev_act_dict]


# With `rev_product_dict` we can see the products generated by the activities.

# In[42]:


print("Row num."+" "+"Product")
[print(str(k)+" "+str(get_activity(rev_product_dict[k]))) for k in rev_product_dict]


# And with `rev_bio_dict` we can see the emission or resource flows!

# In[22]:


print("Row num."+" "+"Elementary flow")
[print(str(k)+" "+str(get_activity(rev_bio_dict[k]))) for k in rev_bio_dict]


# Now let's look at the technology matrix and the inventory matrix generated by `LCA`.

# In[23]:


tech_matrix=lca.technosphere_matrix.toarray()
print(tech_matrix)


# This means...

# In[24]:


for r in range(0,tech_matrix.shape[0]):
    for c in range(0,tech_matrix.shape[1]):
        if tech_matrix[r, c]>0:
            print(str(rev_act_dict[c][1])+" supplies "+ str(tech_matrix[r, c])+" of "+str(get_activity(rev_product_dict[r])))
        else:
            print(str(rev_act_dict[c][1])+" uses "+ str(tech_matrix[r, c])+" of "+str(get_activity(rev_product_dict[r])))


# $$ \begin{matrix} & Electricity\quad production & Fuel\quad production \\ E\quad(kWh) & 10 & 0 \\ F\quad(kg) & -2 & 1 \end{matrix}$$
# 
# Positive values from an activity means production and negative is the use of a natural resource (rows). This seems to correspond with the activities created.
# 
# Let's lool at the supply array: 
# 
# **Which activities supply to fulfill the functional unit (FU)? Let's find out!**

# In[25]:


supply_array=lca.supply_array.tolist()
for r in supply_array:
    print("{} supplies {}".format(rev_product_dict[supply_array.index(r)][1],supply_array[supply_array.index(r)]))


# Now, let's look at the calculated inventory and try to display the corresponding supplying activities as columns as the requested environmental flows as rows.
# The inventory given by the LCA object looks like the ouput of the cell below. It is hardly readable when it contains thousands of flows when we upload a giant dataset.
# 

# In[26]:


print(lca.inventory) # type(lca.inventory) = scipy.sparse._csr.csr_matrix


# Let's turn in into an array for easy access to the values.
# 

# In[43]:


inventory_matrix = lca.inventory.toarray()
inventory_matrix # What does this mean?


# What does this matrix mean? Let's turn it into a dataframe just to have a more visual aid to see what these terms are!

# In[44]:


import pandas as pd
inventory_matrix_df = pd.DataFrame(inventory_matrix)
inventory_matrix_df.columns = ['Electricity production', 'Fuel production']
rev_bio_dict_df = pd.DataFrame(rev_bio_dict)
rev_bio_dict_flow_index = rev_bio_dict_df.iloc[1, :]
rev_bio_dict_flow_index.rename('Resource and emission flows', inplace=True)
inventory_matrix_df = inventory_matrix_df.set_index(rev_bio_dict_flow_index)
inventory_matrix_df


# What is producing what and what is using what? Let's make some sense of these data looping through it and printing what we are seeing:

# In[46]:


for r in range(0,inventory_matrix.shape[0]):
    for c in range(0,inventory_matrix.shape[1]):
        if inventory_matrix[r, c]>0:
            print(str(rev_act_dict[c][1])+" emits "+ str(inventory_matrix[r, c])+" "+get_activity(rev_bio_dict[r])["unit"]+" of "+str(rev_bio_dict[r][1]))
        else:
            print(str(rev_act_dict[c][1])+" uses "+ str(inventory_matrix[r, c]*(-1))+" "+get_activity(rev_bio_dict[r])["unit"]+" of "+str(rev_bio_dict[r][1]))


# Now we create a list that with imaginary __characterization factors__:

# In[47]:


myLCIAdata = [[('testdb', 'Carbon dioxide'), 2.0], 
              [('testdb', 'Sulphur dioxide'), 2.0],
              [('testdb', 'Crude oil'), 2.0]]
type(myLCIAdata)


# And now we use the function `Method` to use the keys(?)

# In[48]:


method_key = ('simplemethod', 'imaginaryendpoint', 'imaginarymidpoint')
my_method = Method(method_key)
my_method


# Here we can connect the method we have created `my_method` with the characterization factors `myLCIAdata`, normally here is where ReCiPe, TRACI etc are used!

# In[ ]:


my_method.validate(myLCIAdata)
my_method.register() 
my_method.write(myLCIAdata)
my_method.load()


# Now let's do the calculations properly, here what we do is passing the `functional_unit` and the `method_key` (why the `method_key` and not `my_method` ? It gives and error, but why?)

# In[57]:


lca = LCA(functional_unit, method_key) #run LCA calculations again with method
lca


# In[58]:


lca.lci()
lca.lcia()
print(lca.inventory) # This one is output of LCI
print("")
print(lca.characterized_inventory)  # This one is output of LCIA


# In[59]:


print(lca.score)
print("")
print(sum(lca.characterized_inventory))
print("")
print(lca.score)


# Why is the score negative?

# In[ ]:




