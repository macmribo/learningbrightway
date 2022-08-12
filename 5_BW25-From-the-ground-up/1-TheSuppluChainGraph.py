#!/usr/bin/env python
# coding: utf-8

# # 1 &emsp; The Supply Chain Graph 

# These set of tutorials follow the same tutorial made by [tngTUDOR](https://github.com/brightway-lca/from-the-ground-up). Teaching material for Brightway2.5, starting from the foundations. A different approach from the existing teaching material which describes how Bightway works, with a focus on why Brightway does what it does. These notebooks are designed to be used in class, so do not contain a ton of instruction.

# In[1]:


import bw2data as bd


# About bw2data: The first thing to learn about `bw2data` is the concept of projects. Each project is self-contained, and independent of other projects. Each has its own subdirectory. This can lead to data duplication, but helps keep each project safe from the changes in the others.
# 
# We start in the `default` project:

# In[2]:


bd.projects.current


# With directory:

# In[3]:


bd.projects.dir


# Make it easy to reset this project:

# In[4]:


try:
    bd.projects.delete_project("1 Supply Chain Graph", True)
except ValueError:
    pass


# Let's create a new project:

# In[5]:


bd.projects.set_current('1 Supply Chain Graph')
bd.projects.current


# A graph can have nodes of any type, but for the purposes of LCA it is convenient to separate activity nodes, product nodes, elementary flow nodes, and characterization nodes. We will also use a shortcut (for now) and assume that each activity produces exactly one product, so we can collapse activity and products nodes into a single node.
# 
# Let's think about a simple product system - a bike. Here is a graph:
# 
# <img src='images/simple-graph.png' width='400'>

# To enter this data into BW, we need to create the nodes, and then the edges. We will create these nodes in a `Database`. A database in BW is just a collection of nodes - it can be large or small, there aren't any general rules.

# In[6]:


db = bd.Database('bike')
db.register() # Let the metadata system know this database exists. Not necessary if using a `bw2io` importer.


# Our first node. We specify some additional data to make it easier to find or use this node later on.

# In[7]:


data = {
    'code': 'bike',
    'name': 'bike production',
    'location': 'DK',
    'unit': 'bike',
}

bike = db.new_node(**data)  # Here I needed to upgrade bw2data using conda upgrade bw2data
bike.save()


# In[8]:


data = {
    'code': 'ng',
    'name': 'natural gas production',
    'location': 'NO',
    'unit': 'MJ'
}

ng = db.new_node(**data)
ng.save()


# In[9]:


data = {
    'code': 'cf',
    'name': 'carbon fibre production',
    'location': 'DE',
    'unit': 'kg'
}

cf = db.new_node(**data)
cf.save()


# We can also define nodes like this. Note that this node has a `type`.

# In[10]:


co2 = db.new_node(
    code='co2', 
    name="Carbon Dioxide", 
    categories=('air',),
    type='emission',
    unit='kg'
)

co2.save()


# We also need to create edges between the nodes. We can do this in many ways here is one:

# In[11]:


bike.new_edge(
    amount=2.5, 
    type='technosphere',
    input=cf
).save()


# What about some uncertainty? We use [stats_arrays](https://stats-arrays.readthedocs.io/en/latest/) to model probability distribution functions.

# In[12]:


cf.new_edge(
    amount=237.3,  # plus 58 kWh of electricity, in ecoinvent 3.8 
    uncertainty_type=5, 
    minimum=200, 
    maximum=300, 
    type='technosphere',
    input=ng,
).save()


# In[13]:


cf.new_edge(
    amount=26.6, 
    uncertainty_type=5, 
    minimum=26,
    maximum=27.2, 
    type='biosphere',
    input=co2,
).save()


# Brightway will assume that the a `production` exchange of amount 1 in each node unless you tell it otherwise.
# 
# To define characterization nodes and edges, we use a difference data structure:
# 

# In[14]:


ipcc = bd.Method(('IPCC',))
ipcc.write([
    (co2.key, {'amount': 1, 'uncertainty_type': 3, 'loc': 1, 'scale': 0.05}),
])


# This is already enough to do an LCA. Let's check what our answer should be. Without uncertainty, to make one bike we need 2.5 kg of carbon fibre, and carbon fibre produces 26.6 kg CO<sub>2</sub> per kg of carbon fibre, so we are looking for around 60 kg CO<sub>2</sub>-eq, or more precisely we need 26.6x2.5= 66.5 kg CO<sub>2</sub>-eq.

# Let's load the calculation module `bw2calc` to run the LCA!lca = bc.LCA(demand={bike: 1}, method=('IPCC',))
# lca.lci()
# lca.lcia()
# lca.score

# In[15]:


import bw2calc as bc


# In[16]:


lca = bc.LCA(demand={bike: 1}, method=('IPCC',))
lca.lci()
lca.lcia()
lca.score


# Nice! Exactly as expected :)

# In[18]:


lca = bc.LCA(demand={bike: 1}, method=('IPCC',), use_distributions=True)
lca.lci()
lca.lcia()

for _ in range(10):
    next(lca)
    print(lca.score)


# To use uncertainty, we tell the `import pandas as pd
# ` object to use the probability distributions:

# In[19]:


import pandas as pd


# In[20]:


df_2 = pd.DataFrame([
    {
        'score': lca.score, 
        'inv': lca.inventory.sum(), 
        'char': lca.characterization_matrix.sum()
    } for _, _ in zip(lca, range(100))
])


# In[21]:


df_2.hist('score')


# In addition to storing and using nodes and edges, our graph database can be searched in different ways. Let's show this with a larger database, more specifically with the [US Environmentally-Extended Input-Output (USEEIO)](https://www.epa.gov/land-research/us-environmentally-extended-input-output-useeio-technical-content).
# 
# We can use a shortcut to install some data:

# In[22]:


import bw2io as bi
bi.useeio11()


# In[23]:


bd.databases


# Now we can see out bike together with a larger database.

# In[24]:


db = bd.Database("US EEIO 1.1")
db.name


# This database has processes **and** products. What would this mean for drawing a graph?

# In[25]:


{node['type'] for node in db}


# We can search with the `search` function and play with it. Here we select the first entry when searching for the word `()'amusement')[0]`, and alocate it to the variable `fun`. Then we change the name from `'Amusement parks and arcades'` to `'fun'`. We then save to save changes.

# In[62]:


fun = db.search('amusement')[0]
fun['name'] = 'fun'              # You can change the name of the activity
fun.save()                       # This one I saves it into the database


# In[63]:


db.search('amusement')


# Ok, let's change it back!

# In[64]:


fun['name'] = 'Amusement parks and arcades'              # You can change the name of the activity
fun.save()


# In[65]:


db.search('amusement') # Isn't it fun


# We can also list all the nodes in the database. Go ahead and play around with other node types such as 'emission', 'process' and 'product'.

# In[119]:


{node['name'] for node in db if node['type'] == 'product'}; # This is a very long list, if you want to see the result, remove the ';'.


# In[120]:


sum([o['amount'] for o in edge.output.technosphere()])


# ### Interacting with the graph

# In[35]:


moo = db.get(name='Cattle ranches and feedlots', type='product')


# In[72]:


type(moo) == bd.Node


# In[74]:


moo['categories']


# In[75]:


moo['location']


# In[76]:


moo['unit']


# Here we can see the upstream edges or exchanges:

# In[77]:


for edge in moo.upstream():
    print(edge)


# In[84]:


sum([o['amount'] for o in edge.output.technosphere()])


# In[141]:


for o in edge.output.technosphere():
    print(o['name'],': ', o['amount'], o['unit'])


# ### Brightway capabilities

# Let's show a little bit of what Brightway can do. We can compare the correlation of LCA scores across a variety of categories.
# 
# There is an atuomatic way to do this in Brightway, but we can also program it manually to see how it works.
# 
# Stop for a bit and think about what one would need to calculate LCA scores for 380 products and ~10 impact categories.

# In[146]:


products_in_order = [obj for obj in db if obj['type'] == 'product']
categories_in_order = [method for method in bd.methods if method[0] == 'Impact Potential']


# In[148]:


len(products_in_order)


# In[149]:


len(categories_in_order)


# In[191]:


import numpy as np

results = np.zeros((len(products_in_order), len(categories_in_order))) # Create a 388 x 10 matrix of zeroes where the results will be stored

def get_lcia_scores(products, categories, results):
    lca = bc.LCA({products[0]: 1}, categories[0])  # First argument is the functional unit, the second is the impact category methods, starts calculating for the first product of each list
    lca.lci() # Runs the lci and lcia
    lca.lcia()
    
    method_matrices = [lca.characterization_matrix.copy()]  # Generates characterization matrices
    
    for other_method in categories[1:]:                     # Now this is the interesting part, here it loops over all categories and all methods
        lca.switch_method(other_method)
        method_matrices.append(lca.characterization_matrix.copy())
    
    for i, product in enumerate(products):
        lca.redo_lci({product.id: 1})                                        # Here it re-does the lci 
        for j, characterization_matrix in enumerate(method_matrices):
            results[i, j] = (characterization_matrix * lca.inventory).sum()
    
    return results


# Let's see how long it takes to run this beast:

# In[192]:


from time import time

start = time()
results = get_lcia_scores(products_in_order, categories_in_order, results)
print(time() - start)


# That was nothing! Ok, let's make some sense of what we have done:

# In[193]:


from scipy import stats

def create_correlation_matrix(scores_array):
    num_methods = scores_array.shape[1]
    correlations = np.zeros((num_methods, num_methods))

    for row in range(num_methods):
        for col in range(num_methods):
            if col <= row:
                continue                               # Only need to compute correlation once
            dataset_1 = scores_array[:, row]
            dataset_2 = scores_array[:, col]
            mask = (dataset_1 != 0) * (dataset_2 != 0) # Ignore activities that have zero score
            corr = stats.kendalltau( # Get tau value, drop p-statistic
                dataset_1[mask], 
                dataset_2[mask]
            )[0]
            if np.isnan(corr):
                correlations[row, col] = 0
            else:
                correlations[row, col] = corr

    correlations = correlations + correlations.T       # Make sorting easier by adding filling in lower left triangle
    return correlations


# Let's see how the impact factors correlate.

# In[194]:


correlation_matrix = create_correlation_matrix(results)


# In[195]:


correlation_matrix


# In[196]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[197]:


import matplotlib.pyplot as plt

fig = plt.gcf()
fig.set_size_inches(12, 12)

masked_correlation = np.ma.array(correlation_matrix, mask=correlation_matrix == 0).T
plt.pcolor(masked_correlation, cmap=plt.cm.cubehelix_r)
plt.colorbar()
plt.ylim(None, correlation_matrix.shape[1])
plt.xlim(None, correlation_matrix.shape[0])
plt.xticks(np.arange(0.5, 10), [obj[1] for obj in categories_in_order])
plt.yticks(np.arange(0.5, 10), [obj[1] for obj in categories_in_order])
plt.tight_layout()


# In[203]:


for category in categories_in_order:
    print(category[1], bd.methods[category]['description'], '\n')


# In[ ]:





# In[ ]:




