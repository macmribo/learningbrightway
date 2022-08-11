#!/usr/bin/env python
# coding: utf-8

# # 5. Using Calculation Setups

# Calculation setups are a way to efficiently do LCA calculations for multiple functional units and methods at the same time.
# 
# This notebook builds on the [Tutorial 4 - LCA with real data](BW_Tutorial_4_LCA_Real_Data.ipynb) notebook, or its original version by Chris Mutel [Getting Started with Brightway2](https://github.com/brightway-lca/brightway2/blob/master/notebooks/Getting%20Started%20with%20Brightway2.ipynb), and won't work if you haven't done that notebook yet. This is because we will be using the same database loaded in that project.

# In[1]:


from brightway2 import *


# Let's copy the project from the previous tutorial. Here I copy the project _I_ made, if you are following Chris Mutel's tutorial use his project naming do there is no confusion!

# In[8]:


if "Tut_5_Calculation_Setups" not in projects:
    projects.set_current("Tut_4_RealLCA")
    projects.copy_project("Tut_5_Calculation_Setups")
else:
    projects.set_current("Tut_5_Calculation_Setups")


# ### Defining a calculation setup

# A calculation setup is defined by three things:
# * A name.
# * A list of functional units.
# * A list of LCIA methods.
# 
# In this example, we will choose both activities and methods at random.

# In[14]:


functional_units = [{Database('forwast').random(): 1} for _ in range(20)] # Here we select 20 random functional units.


# 
# As said in the previous tutorial, we can't choose methods completely at random, since the FORWAST database doesn't have as many biosphere flows as ecoinvent, so many methods will only characterize flows that aren't provided anywhere in FORWAST. So lets only choose from the methods which will have a non-zero LCA score:

# In[15]:


import random

all_forwast_flows = {exc.input for ds in Database("forwast") for exc in ds.biosphere()}
suitable_methods = [method 
                    for method in methods 
                    if {cf[0] for cf in Method(method).load()}.intersection(all_forwast_flows)]

print("Can use {} of {} LCIA methods".format(len(suitable_methods), len(methods)))
chosen_methods = random.sample(suitable_methods, 8)


# A calculation setup is a normal Python dictionary, with keys `inv` and `ia`, for the functional units and LCIA methods, respectively.

# In[16]:


my_calculation_setup = {'inv': functional_units, 'ia': chosen_methods}


# You define a calculation setup by name in the metadata store `calculation_setups`, similar to the way that LCIA methods are defined.

# In[32]:


calculation_setups['some random stuff'] = my_calculation_setup


# In[35]:


calculation_setups['some random stuff']


# The normal create, update, and delete machanisms apply:
# 
# * To create a new calculation setup, assign by name, as in cell above
# * To replace a calculation setup, just assign new data, i.e. `calculation_setups['some random stuff'] = some_new_stuff`.
# * To delete a calculation setup, use `del`, i.e. `del calculation_setups['some random stuff']`.
# 

# ### Using a calculation setup

# Use the `MultiLCA` class to get LCA results for a calculation setup. Note that this class does all the calculations as soon as you create it.

# In[37]:


mlca = MultiLCA('some random stuff')
mlca.results


# ### Visualizing the results

# There isn't any code built into Brightway2 yet, but [Seaborn](http://seaborn.pydata.org/index.html) has some great visualizations for this type of result array. You will need to install Seaborn in your environment if you don't have it already!

# In[38]:


get_ipython().run_line_magic('matplotlib', 'inline')


# Ignore them warnings.

# In[40]:


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[79]:


# From https://stanford.edu/~mwaskom/software/seaborn/tutorial/color_palettes.html
cmap = sns.cubehelix_palette(8, start=.5, rot=-.75, as_cmap=True) 
sns.set(rc = {'figure.figsize':(15,8)})  # Heatmap size
sns.heatmap(
    mlca.results / np.average(mlca.results, axis=0), # Normalize to get relative results
    annot=True, 
    linewidths=.05, 
    cmap=cmap, 
    xticklabels=["\n".join(x) for x in mlca.methods],
    yticklabels=[y for y in mlca.func_units]
)
plt.xticks(rotation=70); 


# In[52]:


print(dir(mlca))


# In[73]:


mlca.func_units[:]


# In[74]:


mlca.methods


# In[ ]:




