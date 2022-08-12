#!/usr/bin/env python
# coding: utf-8

# # 7. Uploading US LCI - Not working (Yet)

# As the title of this notebook states, this notebook will go step by step to upload US LCIto a project.

# ### Setting up the project

# In[1]:


from brightway2 import *


# In[2]:


projects.set_current('Tut_7_Uploading_US_LCI')


# Let's load a biosphere:

# In[3]:


bw2setup()


# US LCI dataset downloaded from [here](https://github.com/uslci-admin/uslci-content/blob/dev/docs/release_info/release-downloads.md) in Table 1.
# <div class="alert alert-danger" role="alert">
#   <i class="fa fa-exclamation-triangle" aria-hidden="true"></i>
# According to the official Github US LCA page, ecospold format only contains processes, however, I do not know how updated this statement is. I will see how it affects results.
# </div>

# I hadproblems uploading the right data type. Those files finishing in `.spold` seem to be accepted by `SingleOutputEcospold2Importer`. However, the code breaks after running `.apply_strategies()`. 
# 
# I tried every single ecospold and ecospold2 file in the repository and the most promising one is [FY20.Q3.02 Olca 1.10.3](https://github.com/uslci-admin/uslci-content/blob/dev/downloads/uslci_fy20_q3_02_olca1_10_3_ecospold.zip). It has 1897 datasets, let's see if it works.

# In[4]:


sp = SingleOutputEcospold1Importer(
    "/Users/mmendez/Documents/Postdoc/Software_dev/databases/US LCI/uslci_fy20_q3_02_olca1_10_3_ecospold/EcoSpold01", 
    "NREL-USLCI"
)


# [Chris Mutel's tutorial](https://github.com/brightway-lca/brightway2/blob/master/notebooks/IO%20-%20Importing%20the%20US%20LCI%20database.ipynb) has 702 datasets. He does not specify which file he is using. 

# In[5]:


sp.apply_strategies()


# OK, our first error. There are two process datasets that have the same process name - in this case, it looks like one was a first draft, and the other is the final dataset. One file is called `EcoSpold_631_processes_2020-09-20T05-43-42.xml`, and the other is called `EcoSpold_633_processes_2020-10-28T06-01-13.xml`. They are basically the same and there are three of them (note the one with the `'(missing)'` filename, so we will ignore them.

# In[6]:


ecospoldfiles = ('/Users/mmendez/Documents/Postdoc/Software_dev/databases/US '
              'LCI/uslci_fy20_q3_02_olca1_10_3_ecospold/EcoSpold01') # Here is where the files are saved, this is just for me to make the link smaller later

bad_file = (ecospoldfiles+'/coSpold_633_processes_2020-10-29T03-27-30.xml')
sp.data = [obj for obj in sp.data if obj.get('filename') != bad_file]


# In[ ]:





# In[7]:


sp.apply_strategies(sp.strategies[-2:])


# It threw me an error again, let's see what happens if I continue.

# The US LCI has "dummy" processes - links to activities which are real inputs, but which aren't modeled in the database. We need to add these dummy processes as real activities (even if they don't have any inputs themselves).

# In[8]:


from bw2io.strategies import *


# In[9]:


sp.apply_strategy(special.add_dummy_processes_and_rename_exchanges)


# Let's see how things look. In an ideal dataset, everything would already be linked, but we know that this is not yet true for the US LCI.

# In[10]:


sp.statistics()


# We are now ready to start internally linking the database.
# 
# First, we migrate some names for biosphere flows.

# In[11]:


sp.migrate("biosphere-2-3-names")
sp.migrate("biosphere-2-3-categories")
sp.migrate('default-units')


# Then, we try to internally link the database. We call the match_database method with two arguments. The first is `None`, i.e. we are not linking against another database, but only doing internal linking. Because the US LCI doesn't use categories in exchange definitions consistently, we also `ignore_categories`.

# In[12]:


sp.match_database(None, ignore_categories=True)


# Similar error as before, let's ignore the older files.

# In[13]:


bad_file = (ecospoldfiles+'/EcoSpold_633_processes_2020-10-29T03-27-30.xml')
sp.data = [obj for obj in sp.data if obj.get('filename') != bad_file]


# In[14]:


sp.match_database(None, ignore_categories=True)


# 
# 
# We have done the internal linking that we can - now we need to link the biosphere flows. This looks complicated, but is just a fancy way of linking the biosphere flows by their names, units, and categories.
# 

# In[15]:


import functools
f = functools.partial(link_iterable_by_fields,
    other=Database(config.biosphere),
    kind='biosphere'
)
sp.apply_strategy(f)


# Let's see how far we have got:

# In[16]:


sp.statistics()


# JAJAJAJJAJAJJAJJAJA WHAT? Horrible.

# In[ ]:




