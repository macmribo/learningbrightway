#!/usr/bin/env python
# coding: utf-8

# # USLCI JSON-LD import

# ## 1. Import relevant packages

# In[1]:


import bw2data as bd
import bw2calc as bc
import bw2io as bi
import bw_processing # Not sure yet if I need this
import bw_migrations # Not sure yet if I need this
from bw2io.importers.json_ld_lcia import JSONLDLCIAImporter

import os
import numpy as np
import pandas as pd


# ## 2. Create/set the working folder:

# In[2]:


bd.projects.dir


# In[3]:


bd.projects.set_current('USLCI_FY22_Q2_4')


# In[ ]:





# Exporter import

# In[4]:


from bw2io.extractors.json_ld import JSONLDExtractor


# In[5]:


path0 = '../7_BW2_Importing_USLCI/databases/FY22_Q2_01_Zolca_LCIA_methods_mapping_FEDEFL_3' # For some reason if I use the relative path it throws me an error
data = JSONLDExtractor.extract(path0)


# In[ ]:





# ## 3. Import JSON-LD:

# In[6]:


path = '../7_BW2_Importing_USLCI/databases/FY22_Q2_01_Zolca_LCIA_methods_mapping_FEDEFL_3'
uslci = bi.importers.JSONLDImporter(
    path, 
    "USLCI_FY22_Q2_1", 
    preferred_allocation="PHYSICAL_ALLOCATION" # Most USLCI allocations are based on physical allocations (source: Rebe Feraldi)
)


# ### 3.1 Debugging the processes that have AvoidedProduct = True and input = True

# OpenLCI sets avoided products (AvoidedProducts = True) as inputs (input = True) and they are always outputs. This issue gives an error while applying strategies `apply_strategies()`, specifically it gives the error using the function `json_ld_label_exchange_type`, this is fixed in cell [7].

# In[ ]:


uslci.data.keys()

#[e for e in uslci.data if e['name'] == 'Electricity, at eGrid, SRVC, 2010'][0]


# In[ ]:


for i, l in enumerate(uslci.data['processes']['2a78de43-fdf2-4c5f-b527-89db6568ace8']['exchanges'][:2]):
    if l['avoidedProduct'] == True:
        print(i, l['flow']['name'])
        l['input'] = False
        uslci.data['processes']['2a78de43-fdf2-4c5f-b527-89db6568ace8']['exchanges'][i] = l


# In[ ]:


for process_key, process_values in uslci.data['processes'].items():
    for i, exchange in enumerate(process_values['exchanges']):
        if (exchange['avoidedProduct'] == True) & (exchange['input'] == True):
            print(exchange['input'], exchange['flow']['name'])
            exchange['input'] = False
            uslci.data['processes'][process_key]['exchanges'][i] = exchange


# ### 3.2. Checking the number of processes and flows in the USLCI

# I use these cells to investigate and count flows and processes. I need to know how many processes, elemental, waste and production flows there are because even though I fixed the JSON-LD importer and managed to import USLCI and link the activities, it cannot run the LCA because the matrix is not square. There are 566 processes and 927 processes. I believe the extra processes are mislabeled flows.

# In[ ]:


len(uslci.data['processes']), len(uslci.data['flows'])


# In[ ]:


total_prod =0
for process_key, process_values in uslci.data['processes'].items():
    prod_n = 0
    for i, exc in enumerate(process_values['exchanges']):
        if (exc["flow"]["flowType"] == "PRODUCT_FLOW") & (~exc["input"]) & (exc.get('quantitativeReference') is True):
            prod_n += 1
    if prod_n > 1:
        print('{} has {} products'.format(process_values['name'], prod_n))
    total_prod += prod_n

    #print('{} has {} products'.format(process_values['name'], prod_n))
print('There are {} products'.format(total_prod))


# So, according to this, we have 454 products and productions. So the matrix should be square! Brightway is adding more production flows than it should. Let us fix that! I am suspecting the dummy flows are the issue. Also, it seems like waste flows are labeled as production.

# Now let's check how many processes has waste as output:

# In[ ]:


process_n = 0
for process_key, process_values in uslci.data['processes'].items():
    prod_n = 0
    for i, exc in enumerate(process_values['exchanges']):
        if (exc["flow"]["flowType"] == "WASTE_FLOW") & (~exc["input"]):
            prod_n += 1
    if prod_n > 0:
        process_n += 1
        print('{} has {} output waste flows.'.format(process_values['name'], prod_n))
print('There are {} processes that have waste as outputs.'.format(process_n))


# Not necessary but let's check how many processes has waste as input:

# In[ ]:


process_n = 0
for process_key, process_values in uslci.data['processes'].items():
    prod_n = 0
    for i, exc in enumerate(process_values['exchanges']):
        if (exc["flow"]["flowType"] == "WASTE_FLOW") & (exc["input"]):
            prod_n += 1
    if prod_n > 0:
        process_n += 1
        print('{} has {} input waste flows.'.format(process_values['name'], prod_n))
print('There are {} processes that have waste as inputs.'.format(process_n))


# Is any of these flows labeled as quantitativeReference?

# In[ ]:


total_waste =0
for process_key, process_values in uslci.data['processes'].items():
    prod_n = 0
    for i, exc in enumerate(process_values['exchanges']):
        if (exc["flow"]["flowType"] == "WASTE_FLOW") & (~exc["input"]) & (exc.get('quantitativeReference') is True):
            prod_n += 1
    if prod_n > 0:
        print('{} has {} waste flows'.format(process_values['name'], prod_n))
    total_waste += prod_n

    #print('{} has {} products'.format(process_values['name'], prod_n))
print('There are {} waste flows as quantitativeReference'.format(total_waste))


# No, awesome! Let's check how many flows are biosphere:

# In[ ]:


elem_n = 0
for key, values in uslci.data['flows'].items():
    if values['flowType'] == 'ELEMENTARY_FLOW':
        elem_n += 1
print('There are {} elementary flows in total'.format(elem_n))


# I think I need to look at the Brightway imported file and check how many processes have more than 1 production flows and which are these processes. Keep running these cells and I will see you back in section ADD SECTION

# ## 4. Apply strategies to map JSON-LD to Brightway2 schema:

# These strategies adapts the JSON-LD schema with the Brightway2 schema.

# In[7]:


uslci.apply_strategies()


# ### 4.1. I did some debugging in the background...

# What a beautiful feeling, all strategies were applied with no issues. I had to fix certain bugs mostly:
# 
# - `Applying strategy: json_ld_location_name`, error `KeyError: ['location']`, not all processes have locations, since Brightway2 requires locations it throws an error because it does not find the needed key. I identified these processes and set the location 'Northern America'. This might not be the right solution since it requires changing the database. I will contact Rebe Feraldi and inquiry about some of the processes not having location. It might be wiser to change the BW2 code so it does not require location.
# - `Applying strategy: json_ld_location_name`, There was also a weird bug, where some of the locations were set as `None` and the 
# - `Applying strategy: json_ld_add_activity_unit`, throws an error `AssertionError: Failed allocation`. This function identifies `PRODUCT_FLOW` in the outputs so it can get the units of the reference flow, however, there are processes with more than one `PRODUCT_FLOW`. I think what it is forcing is to have one as the "reference flow" thus it might be confusing reference flow with production flow. I changed the code increasing the `if` statement adding `quantitativeReference`, so it knows that which flow is the reference product to 'borrow' its units. The fix: added `& (exc.get('quantitativeReference') is True`.
# - `Applying strategy: json_ld_label_exchange_type`, gives me `ValueError: Avoided products are outputs, not inputs.` while applying strategy json_ld_label_exchange_type (solved in section 3.1).This error comes up again, because
# - `Applying strategy: json_ld_label_exchange_type`, giver the error `ValueError: Inputs must be products`, this is not necessarily true, because there are some `WASTE_FLOWS` that are inputs, so I add `WASTE_FLOWS` to be technosphere inputs!

# ### 4.2. Create dummy processes to link processes

# Now let's check some statistics, what we mostly care about is that everything is linked!

# In[ ]:


uslci.statistics()


# This is expected, there are certain exchanges unlinked because the are production flows that go nowhere. Only emissions and resources are entitled to do this. So, what do we do? We assign dummy processes. There is a function in the brightway-io package, but I had to tweak it to make it work (`if "input" not in exc or "amount" not in exc:` added because it was throwing me a weird error). After fixing it, let's apply the dummy-maker strategy:

# In[ ]:


uslci.apply_strategy(bi.strategies.special.add_dummy_processes_and_rename_exchanges)


# Let's apply the statistics again and...uslci.statistics()

# In[ ]:


uslci.statistics()


# Boom! No unlinked exchanges.

# ## 5. Writing and saving the database

# ### 5.1. Check database dictionaries:

# Now that we have uploaded the USLCI database, let's write the databases dictionary. If you paid attention, after applying the strategies, there is a message at the end of the output that reads the following:
# 
# ```
# Created 2879 biosphere flows in separate database 'USLCI_FY22_Q2_1 biosphere'.
# Use either `.merge_biosphere_flows()` or `.write_separate_biosphere_database()` to write these flows.
# ```
# 
# This means that it has splitted the USLCI into a different database. This is because it will use this database to generate the biosphere matrix. It also makes easier to query processes and flows.
# You can check which databases are within the project using `bd.databases`. If this is the first time you run this code, there should be 0 objects in the database dictionary, if there are already written databases.

# In[ ]:


bd.databases # If this is the first time you run this code, there should be 0 objects in the database dictionary:


# Let's fill out our project folder with some databases!

# #### 5.1.1. Write the biosphere database:

# In[ ]:


uslci.write_separate_biosphere_database()


# #### 5.1.2.Write the technosphere database:

# In[ ]:


uslci.write_database()


# <div class="alert alert-block alert-warning">
# <b>To fix:</b>
# <code>
# Not able to determine geocollections for all datasets. This database is not ready for regionalization.
# </code>
# Indicates that the locations given are not within the brightway2 geocollections. This is a problem for future Mac, but it needs to be fixed, probably by mapping the location names properly with brightway location dictionary.
# </div>

# Now you should see the uploaded database dictionaries:

# In[ ]:


bd.databases


# ### 5.2. Saving the databases

# Hoorraaay! Now let's be tidy and save them in variables for easy access:

# In[ ]:


bio = bd.Database('USLCI_FY22_Q2_1 biosphere')


# In[ ]:


db = bd.Database('USLCI_FY22_Q2_1')


# ## 6 Import the LCIA methods

# In[ ]:


uslci_methods = bi.importers.JSONLDLCIAImporter(path)


# In[ ]:


uslci_methods.apply_strategies()


# In[ ]:


uslci_methods.match_biosphere_by_id('USLCI_FY22_Q2_1 biosphere')


# In[ ]:


uslci_methods.statistics()


# These are the available methods:

# In[ ]:


if [things['name'] for things in uslci_methods.data][0] in bd.methods:
    print('Method already loaded!')
else:
    uslci_methods.write_methods()


# In[ ]:


list(bd.methods)


# In[ ]:


uslci.statistics()


# In[ ]:





# ## 7 Querying the databases

# ### 7.1 Let's look at the biosphere database:

# You can search activities using list comprehension:

# In[ ]:


carbon_query = [bio_flow for bio_flow in bio if bio_flow['name'].lower().startswith('carbon')] # Use .lower() to make it non-case sensitive
carbon_query; # Remove ';' if you want to reveal the output!


# In[ ]:


print('There are {} carbon-related flows!'.format(len(carbon_query)))


# You can also use `.search()` to find the flow:

# In[ ]:


bio.search('carbon dioxide')


# Let's refine our search and save one of these in a variable:

# In[ ]:


carboncete = [act for act in bio if 'Carbon dioxide' in act['name']
                                            and 'Elementary Flows' in str(act['categories'])
                                            and 'emission' in str(act['categories'])
                                            and 'ground' in str(act['categories'])][0]


# #### 5.3.2. Now let's look at our technosphere database

# The technosphere database is composed of activities thaat can be processes (they have exchanges, input and output flows) and product flows (these can be outputs or inputs). Let's explore a different way to select an activity... let's say I am just testing and I just want a random activity. Can I do it? Selvfølgelig! Actio `.random()`!!

# In[ ]:


random_act = db.random()
random_act


# Let's look at it with more intensity...

# In[ ]:


random_act.as_dict();


# Looking at this closely, you can see that there are no exchanges, this is because these are saved in a different location. Let's now look at a specific process:

# In[ ]:


db.search('corn')


# In[ ]:


len(db.search('corn'))


# You can also filter your search:

# In[ ]:


db.search('corn', filter={'categories': 'Technosphere'}) # Here I show the flows


# You can also `mask`!

# In[ ]:


db.search('corn', mask={'categories': 'Technosphere'}) # Here I show the processes


# It is also important to stress the importance of filtering, because the `search` function returns a maximum of 25 possible candidates. This is why I prefer list comprehension.

# In[ ]:


len([act['code'] for act in db if '.' in act['code']])


# In[ ]:


len([act['code'] for act in db if '.' not in act['code']])


# 168 of them are behaving weird 1635 of them are normal. They did not drop many of the category names that are not necessary, on top of that, their code name is merges with a flow. Questions:
# - What do these processes have in common?
# - Why do they have double codes?
# - Why aren't they dropping come of the items?
# 
# Let's start if all of them have `allocationFactors`

# In[ ]:


len([act['allocationFactors'] for act in db if '.' in act['code']])


# All of these have allocationFactors. Sanity check!

# In[ ]:


len([act for act in db if 'allocationFactors' in act])


# Ok, so these weirdos are the ones that have the key `allocationFactor`

# Here I filter for the processes that have more than 15 entries and do not have a '.' in the code. I want to check if these are normal processes and why do they have so many entries:

# In[ ]:


len([act for act in db if len(act) > 15 and '.' not in act['code']])


# In[ ]:


[act.as_dict() for act in db if len(act) > 15 and '.' not in act['code']];


# Ok, these processes did not drop some of the entries... so something does not work in the JSON-LD importer, these processes are escaping the mapping for some reason. However, their code is normal.

# In[ ]:


len([act.as_dict() for act in db if len(act) > 15])


# 198 processes have a looot of entries, the average entry number should be:

# In[ ]:


np.median([len(act.as_dict()) for act in db]), np.mean([len(act.as_dict()) for act in db]), np.std([len(act.as_dict()) for act in db])


# 10

# Let's be more specific:

# In[ ]:


activity_list = []
for entries in range(5, 19):
    activities = len([act.as_dict() for act in db if len(act) == entries])
    print('# of activities with {} entries: {}'.format(entries, activities))
    activity_list.append(activities)


# Let's check out the 7 entry process, it does not have a unit... why?

# In[ ]:


[act.as_dict() for act in db if len(act) == 7];


# In[ ]:


dummy = [act for act in db if len(act) == 7][0]
dummy


# In[ ]:


[exc for exc in dummy.exchanges()]


# Aaah it is the dummy process. Ok, it does not need units.

# To drop some of these entries I just have to modify the functiondef json_ld_remove_fields(db) in the `brightway2-io/strategies/json_ld`

# In[ ]:


len([act for act in db if 'corn' in act['name'].lower()])


# See? 42 entries now! Looking at this list, you can see that this search mixes processes and flows, let's find the process flows:

# I will come back to this later...

# ### Let's add an LCIA method

# In[ ]:


method_gw = [act for act in bd.methods if 'Global warming' in str(act) and 'TRACI' in str(act)][0]
method_key = method_gw
my_method = bd.Method(method_key)


# #### Now we define a functional unit:
# I will select `Aluminium, extrusion, at plant`

# In[ ]:


alu = [act for act in db if act['name'].lower().startswith('aluminium, extrusion')][0]
print(alu.as_dict()['id'])
alu.as_dict()


# In[ ]:


functional_unit = {alu : 5}


# In[ ]:


type(functional_unit)


# #### Run the LCA!

# In[ ]:


lca = bc.LCA(functional_unit, method_key) 


# In[ ]:


#bc.LeastSquaresLCA(lca)


# In[ ]:


lca.lci() 
lca.lcia()
lca.score
print(lca.inventory)


# In[ ]:


962 - 601


# ## 

# In[ ]:


n_process = len([act for act in db if act['type'] == 'process'])
n_process


# In[ ]:


n_prod = len([act for act in db if act['type'] == 'product'])
n_prod


# In[ ]:


techno_shape = lca.technosphere_matrix.todense().shape
techno_shape[0]


# In[ ]:


print('We have a total of {} products, {} processes, and the technosphere has {} product in it.\nWhat are those {} extra products in the matrix?\nWhat are the {} excluded then?'.format(n_prod, n_process, techno_shape[0], techno_shape[0]-n_process, n_prod-techno_shape[0]))


# Ok... I think those are the products that don't have a process related to it... these could be waste technosphere flows. Let's check it out.

# In[ ]:


prod_count = 0
waste_count = 0
techno_count = 0
type_list = []
for act in db:
    if act['type'] == 'process':
        for exc in act.exchanges():
            type_list.append(exc['type'])


# In[ ]:


len(type_list)


# In[ ]:


type_set = set(type_list)


# In[ ]:


type_set


# In[ ]:


pd.value_counts(np.array(type_list))


# Are there processes without production?

# In[ ]:


for act in db:
    prod_counter = 0
    for exc in act.exchanges():
        if exc['type'] == 'production':
            prod_counter += 1
            
            


# In[ ]:


listita = []
for act in db:
    if '.' in act['code']:
        print(act['code'])
        listita.append(act)


# In[ ]:


[[act for act in db if act['code'] == '0e42a306-ee2d-362e-8bc3-580000096459.fa5304ba-de40-35cf-a5d6-3e09d9b79205'][0].exchanges()]


# In[ ]:




