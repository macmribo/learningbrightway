#!/usr/bin/env python
# coding: utf-8

# In[1]:


import openlca2bw as olca2bw
import brightway2 as bw

Zip_path = r'C:\Users\sayala\Documents\GitHub\Brightways\learningbrightway\7_BW2_Importing_USLCI\databases\FY22_Q2_01_Zolca_LCIA_methods_mapping_FEDEFL_3'


# In[2]:


olca2bw.load_openLCA_Json(path_zip=Zip_path,
                          project_name='USLCI',
                        #  user_databases={"DB1":'Process'},
                          overwrite = True)


# In[3]:


bw.databases


# ### Processes get loaded into the pre-named database "EcoInvent" (change name inside of package)
# ### Elements get loaded into the biosphere. Process flows are not loaded. 

# In[6]:


bio = bw.Database("biosphere3")
len(bio)


# In[7]:


db = bw.Database("EcoInvent")


# In[8]:


len(db)


# In[15]:


randomAct = db.random()
randomAct


# In[16]:


randomMethod = bw.methods.random()
randomMethod


# In[17]:


myFirstLCA_quick = bw.LCA({randomAct:1}, randomMethod)


# In[18]:


myFirstLCA_quick.lci()    # Builds matrices, solves the system, generates an LCI matrix.
myFirstLCA_quick.lcia()   # Characterization, i.e. the multiplication of the elements 
                          # of the LCI matrix with characterization factors from the chosen method
print(myFirstLCA_quick.score)    # Returns the score, i.e. the sum of the characterized inventory

