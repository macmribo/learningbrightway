#!/usr/bin/env python
# coding: utf-8

# # 2 &ensp; Data input/output

# This notebook is based on the [Chris Mutel and Pascal Lesage notebook series from their seminar session day 2 in 2017](https://github.com/PoutineAndRosti/Brightway-Seminar-2017/blob/master/Day%201%20PM/Data%20IO.ipynb). The main difference is the use of free databases. They mostly use ecoinvent so I try to adapt the notebooks to have a complete open source verison.
# 
# At the end of this notebook, you will be able to:
# 
# * Learn how to input data in different ways:
#     - Programmatically, via dictionary creation.
#     - Excel/csv importers.
#     - SimaPro csv
#         * Two unit-process example
#         * Agribalyse
#     - Importing ecoSpold, ecoSpold2

# ## 2.1 &ensp; Project setup

# Import necessary packages.

# In[1]:


import brightway2 as bw
import os
import bw2calc as bc


# Setting the project. Let's copy the project from the previous tutorial.
# <div class="alert alert-block alert-warning">
# <b>Warning:</b> If you run this project before, skip the following line and run the next one (uncomment it!). Otherwise you will be recopying and creating a bit of a mess.
# </div>
# 

# In[2]:


bw.projects.dir


# In[3]:


# bw.projects.set_current("MW_1")
# bw.projects.copy_project('MW_2')


# In[5]:


bw.projects.set_current("MW_2")   # Run me if this is not the first time you use this notebook!


# In[6]:


bw.projects.current # Making sure we are in the right folder!


# In[7]:


bw.databases  # Check which databases are in the folder


# In[8]:


bio = bw.Database('biosphere3') # Biosphere database
fw = bw.Database('forwast')     # Technosphere database


# ## 2.3 &ensp; Creating a database programatically

# One can create a database via a database. This database would include activities that would contain information about the activities themselves as well as information about the exchanges that are output to this activity (although these get seperated out when the data is written to the actual `database.db`). Let's look at the components of a database for a random activity:

# In[9]:


random_act = fw.random()


# In[10]:


random_act.as_dict()


# Let's check its exchanges.

# In[11]:


len([exc for exc in random_act.exchanges()]) 


# In[12]:


[exc for exc in random_act.exchanges()][1].as_dict() 


# Looking at this layout we can create our own simple activities and run a simple LCA. The original notebook uses ecoinvent for background data, since we do not have that, we will try to substitute the exchanges with some forwast ones. 
# 
# Let's make an LCA for the activity of 'Drinking water from an aluminium bottle', FUN!

# Let's search the background activities that make sense:

# In[13]:


# Aluminium from technosphere
fw_alu = [act for act in fw if 'Aluminium' in act['name']][1]
fw_alu_input = (fw_alu['database'], fw_alu['code']) # I place these two in a tuple to add the to the "input" item within the exchange types.


# In[14]:


fw_alu


# Forwast database is not as complete as ecoinvent, but it is the database we have for our background processes. Therefore we will be very creative and instrad of using "Deformation stroke" for the aluminium water bottle LCA we will use "Fabricated metal products". 

# In[15]:


fw_metal = [act for act in fw if 'Fabricated metal products' in act['name'] and 'EU' in act['name']][0]
fw_metal_input = (fw_metal['database'], fw_metal['code'])


# In[16]:


fw_metal


# Setting the project. Let's copy the project from the previous tutorial.
# <div class="alert alert-block alert-warning"><b>Warning:</b> I tried to draw the 'water' flow from 'biosphere3' database and it threw me the following error: <code>NonsquareTechnosphere: Technosphere matrix is not square: 279 activities (columns) and 280 products (rows). Use LeastSquaresLCA to solve this system, or fix the input data.</code>  
# </div>
# 
# <div class="alert alert-block alert-info"><b>Tip:</b> For future conflicts, the following codes might help point out at the conflicting non-square database:
# </div>
# 
# * Option 1:
# ``` { .lang #example style="color: #333; background: #f8f8f8;" }
# for a in bw.Database("suspect_database"):
#     assert len(a.production()) == 1
# ```
# * Option 2:
# ``` { .lang #example style="color: #333; background: #f8f8f8;" }
# for ds in bw.Database("suspect_database"):
#     for prod_exc in ds.production():
#         if ((prod_exc['input'][1]) != ds['code']):
#             print((ds['name'],ds['code'],ds['location'],prod_exc['input'], prod_exc['name']))
# ```
# * Option 3:
# ``` { .lang #example style="color: #333; background: #f8f8f8;" }
# for ds in bw.Database('database_as_dictionary'):
#     for prod_exc in ds.production():
#         try : assert (prod_exc['name'] == ds['name'])
#         except : print(ds['name'])
# ```

# [Source](https://stackoverflow.com/questions/52421897/identify-which-activity-or-which-product-is-leading-to-a-non-square-technosphere). Thanks to this, specifically Option 1, informed me that it was `biosphere3` the database creating conflict!

# In[17]:


fw_water = [act for act in fw if 'Water, fresh, EU27' in act['name']][0] # Play around with keywords to find your activity, remember the search is CaSe SenSiTivE
fw_water_int = (fw_water['database'], fw_water['code'])


# In[18]:


fw_water


# In[19]:


database_as_dictionary = bw.Database("Database as dict")

water_bottle_data = {
    ("Database as dict", "Some code for the bottle production"): {
        "name": "Water bottle production",
        'unit': 'unit',
        'location': 'GLO',
        'categories': ("Some made up", "category here"),
        "exchanges": [{
            "amount": 0.33,
            "input": fw_alu_input, #Aluminium
            "type": "technosphere",
            "uncertainty type":0,
            "unit=": "kg"},
                      {
            "amount": 0.33,
            "input": fw_metal_input, #Fabricated metal products
            "type": "technosphere",
            "uncertainty type":0,
            "unit=": "kg"}
        ],
        },
    ("Database as dict", "Some code for drinking a bottle full of water"): {
        "name": "Water drinking",
        'unit': 'liter',
        'location': 'GLO',
        'categories': ("Another made up", "category here"),
        "exchanges": [{
            "amount": 1,
            "input": ("Database as dict", "Some code for the bottle production"), #Our water bottle
            "type": "technosphere",
            "uncertainty type":5,
            "loc":0.005,
            "minimum":0.0005,
            "maximum":0.05,
            "unit": "kg"},
                      {
            "amount": 1,
            "input": fw_water_int, #Water
            "type": "technosphere",
            "uncertainty type":0,
            "unit=": "kg"}],
        }
  

}


# After creating a database, we need to "write" it into the newly created database `database_as_dictionary`.

# In[20]:


database_as_dictionary.write(water_bottle_data)


# In[21]:


print('We have {} activities in our custom database.'.format(len(database_as_dictionary)))


# Let's assign the drinking activity to a variable. We do this to formulate the **functional unit**.

# In[22]:


drinking_act = [act for act in database_as_dictionary if "drinking" in act['name']][0]
drinking_act


# ## 2.4 &ensp; Running the LCA

# Check following this [stack overflow post](https://stackoverflow.com/questions/52421897/identify-which-activity-or-which-product-is-leading-to-a-non-square-technosphere) if you have conflicts!

# In[23]:


water_bottle_LCA_from_dict_input = bw.LCA({drinking_act:1}, ('IPCC 2013', 'climate change', 'GWP 100a'))


# In[24]:


water_bottle_LCA_from_dict_input.lci()
water_bottle_LCA_from_dict_input.lcia()
water_bottle_LCA_from_dict_input.score


# ## 2.5 &ensp; Imoprting from CSV or Excel

# ### 2.5.0 &ensp; Hard way or easy way?

# If you want to go for the easy way, skip to [Section 2.5.2](#easy). Otherwise, keep reading in order!

# ### 2.5.2 &ensp;  Hard way

# We will import a dataset in Excel, but this dataset has errors that we will have to fix (I modified this file so it fits with the forwast database). The excel we are importing looks like this:
# 
# ![excel_in:](2-BW2/excel_input_wrong.jpg)

# In[ ]:


imp = bw.ExcelImporter(os.path.join("2-BW2/files", "excel_importer_example_problems.xlsx"))


# In[ ]:


imp.apply_strategies()


# In[ ]:


imp.match_database(fields=('name', 'unit', 'location'))


# In[ ]:


imp.match_database("forwast", fields=('name', 'unit', 'location'))


# In[ ]:


imp.statistics()


# We have four unlinked exchanges.... Let's look at the file we just created. Navigate to the output path:

# In[ ]:


imp.write_excel()


# Looking inside this file:
# ![excel_out:](2-BW2/excel_output.jpg)

# We can see that the unlinked activities are the ones we created. And for some reason, our creation location is from CH and unliks the activities. This is because ion the 'other processes' tab, it is pointing at unkown activities. We can fix this by looking for existing processes in forwast.

# It looks like we have a few small inconsistencies, like the name of the processes or their locations. Try to fix these on your own, and re-run the code two cells above to get an idea of your progress. The attributes used for matching (fields) must match exactly, though they are case-insensitive.
# 
# If you can't get it to work, you can change the name of the import file to "excel_importer_example.xlsx"; this already has the necessary corrections, take a moment to spot the differences.
# 
# If you need to find the forwast processes, you can search forwast (as you should already know :) )

# After looking at the excel sheet, I fixed the sheet 'other processes' and changed the location to GLO instead of CH. Now e will use this database to fixed the unlinked problems.

# ### 2.5.2 &ensp;  Easy way <a id=easy />

# Import a file where everything should link without any problems. Faster, but you don't learn about how, why, and all those other silly questions. NO GUILT TRIP AT ALL!

# In[34]:


imp_2 = bw.ExcelImporter(os.path.join("2-BW2/files", "excel_importer_example.xlsx"))
imp_2.apply_strategies()
imp_2.match_database(fields=('name', 'location', 'unit')) # To link water I deleted matching 'unit' which will link everything
imp_2.match_database("forwast", fields=('name', 'location', 'unit'))
imp_2.statistics()


# In[28]:


#imp_2.write_excel()


# Now, if we navigate to the `write_excel()` path, we will not find any unlinked exchanges!

# ### 2.5.3 &ensp;  Writing the database

# Finally, we need to write this data to a new `Database`.

# In[35]:


imp_2.write_database()


# I am having problems with .write_database() and I am [not the only one](https://stackoverflow.com/questions/67318953/brightway2-write-database-keywords-must-be-strings). Deleting empty lines before `Activity` on the excel file worked!

# In[36]:


lca = bw.LCA(
    {("BW2 Excel water bottle import", "WriteSomeCode_UUID_isFineButNotNecessary"): 1}, 
    ('IPCC 2013', 'climate change', 'GWP 100a')
)
lca.lci()
lca.lcia()
lca.score


# In[ ]:




