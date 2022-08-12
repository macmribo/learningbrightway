#!/usr/bin/env python
# coding: utf-8

# # 3. &emsp; Inventory data from spreadsheets

# #### Setup new project

# In[1]:


import bw2data as bd
import bw2io as bi
import bw2calc as bc


# In[4]:


bd.projects.set_current('FGU-3-Inventory')


# In[5]:


bi.create_core_migrations()


# In[6]:


xl_importer = bi.ExcelImporter('lci-bike.xlsx')


# In[7]:


xl_importer.apply_strategies()


# In[8]:


xl_importer.statistics()


# In[9]:


for obj in xl_importer.unlinked:
    print(obj)


# In[10]:


xl_importer.match_database(fields=['name'])
xl_importer.statistics()


# In[11]:


xl_importer.write_database()


# In[13]:


bd.databases


# To do: Figure out how to play around and extract data properly

# In[ ]:




