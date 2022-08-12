#!/usr/bin/env python
# coding: utf-8

# # 4. LCA With Real Data

# Now that we are familiar with most of the terminology, we should move on to generate an LCA on REAL big databases. This notebook is based on [*Getting Started with Brightway2*](https://github.com/brightway-lca/brightway2/blob/master/notebooks/Getting%20Started%20with%20Brightway2.ipynb).
# 
# At the end of the notebook you will be able to:
# 
# * Import basic data like the biosphere database (this one gives you emision and resource flows!)
# * Import and explore the [FORWAST](http://forwast.brgm.fr/Overview.asp) database, dowload [here](https://lca-net.com/projects/show/forwast/)
# 
# Chris Mutel promises a kitten when you finish the notebook. In this notebook is a surprise!
# 

# ### Import packages and create a project
# 
# You know how this works, let's get to it!

# In[1]:


from brightway2 import *


# In[2]:


projects.set_current('Tut_4_RealLCA')


# ### Basic data!

# Let's import some basic data - a database of elementary flows, some LCIA methods, and some metadata used for importing other databases. These are inside Brightway2, so you don't need to download anything whohoo!
# 
# Running `bw2setup()` might take some time! Depending on your machine :D

# In[3]:


bw2setup()


# ### Biosphere

# The `'biosphere3'` database was installed with `bw2setup()`. It is called the biosphere3 database because elementary flow names are normalized to the ecoinvent 3 standard.
# 
# Let's see how many flows there are in this database, and then look at one random flow:

# In[4]:


db = Database("biosphere3")
print("Number of flows in `biosphere3`:", len(db))
random_flow = db.random()
print(random_flow)


# In[5]:


print(random_flow['name'])
print(random_flow['unit'])
print(random_flow['categories'])


# Brightway2 uses keys to identify datasets. Each dataset is identified by a combination of its database and some unique code. The code can be anything - a number, a UUID, or just a name. All of the following would be valid key codes:
# ```{python}
#     ("biosphere", "f66d00944691d54d6b072310b6f9de37")
#     ("my new database", "building my dream house")
#     ("skynet", 14832)
# ```

# In[6]:


random_flow.key


# When you are looking for a specific flow, it is better to idectify it by its `code` rather than the `name`. A `name` can point at numerous flows, but the `code` is unique to just one flow.

# ### An LCIA method dataset

# With `bw2setup()` we also installed a large number of LCIA methods:

# In[7]:


len(methods)


# Because LCIA methods have many different impact categories, they are identified not by a single label, but by a list of labels. Let's look at an example:

# In[8]:


method_key = methods.random()
method_key


# In this case, the LCIA method has three levels of specificity, from the general method name (first level) to the specific impact category (last level). There is nothing magic about three levels - you could have one, or one hundred - but Brightway2 expects that LCIA methods will be a list of text labels `('like', 'this')`.
# 
# Note that method identifiers need to be a special kind of list that uses () instead of []. These are called tuples. To create a tuple with only one element, you need to add a comma, to distinguish it from a set of parentheses:

# In[9]:


print (1 + 2)           # This is not a tuple
print (1,), type((1,))  # This is a tuple with one element


# Let's now look at the method data. Method data has the format:
# ```{python}
# biosphere flow, numeric value, location
# ```
# Where:
# 
# * `biosphere flow` is a dataset from any database which is used as a biosphere flow.
# * `numeric value` can be either a fixed number or an uncertainty distribution.
# * `location` is optional; the default value is that this characterization factor is valid everywhere.
# 
# The method data format is pretty flexible, and the following are all acceptable:
# ```
# [('biosphere', 'CO2'), 1.0],                                             # Default location
# [('biosphere', 'CO2'), 1.0, 'Australia, mate!'],                         # Custom location
# [('biosphere', 'CO2'), 1.0, ('Population density', 'Raster cell 4,2')],  # Location inside a geocollection
# [('biosphere', 'CO2'), {'amount': 1.0, 'uncertainty type': 0}],          # Uncertain characterization factor
# ```
# 
# [Geocollections](https://brightway2-regional.readthedocs.io/#spatial-scales-geocollections) are needed for regionalized LCA.
# 
# If you are wondering why we need to identify biosphere flows like `('biosphere', '2fe885840cebfcc7d56b607b0acd9359')`, this is a good question! The short answer is that there is no single field that uniquely identifies biosphere flows or activities. The longer answer is in the [manual](https://2.docs.brightway.dev/intro.html#uniquely-identifying-activities).
# 
# Brightway2 is designed to be flexible enough for many different problems. Therefore, there are no limits on what constitutes a biosphere flow. Rather, anything that is linked to in a biosphere exchange will be put in the biosphere matrix. We installed a database called `biosphere3`, but you can define new flows in a database alongside process datasets, or create your own biosphere database.
# 
# Ok let's look at that method data now! This is also what it's called 
# 

# In[10]:


method_data = Method(method_key).load()
print("Number of CFs:", len(method_data))
method_data[:20]


# ### Importing the FORWAST LCI database

# We will use the FORWAST database, as it is both a high quality, comprehensive LCI database, and freely available. [FORWAST](http://forwast.brgm.fr/Overview.asp) is a physical MRIO table for Europe. It can be downloaded directly from the [2.-0 website](https://lca-net.com/projects/show/forwast/).
# 
# The following cell will download and install the FORWAST database. Note that an internet connection is required.

# In[92]:


import zipfile
import os
from bw2data.utils import download_file
from pathlib import Path


# In[96]:


## I commented this because I already donwloaded it!
# filepath = download_file("forwast.bw2package.zip", url="http://lca-net.com/wp-content/uploads/")
# dirpath = os.path.dirname(filepath)
# zipfile.ZipFile(filepath).extractall(dirpath)
# BW2Package.import_file(os.path.join(dirpath, "forwast.bw2package"))


# ### Searching datasets

# By default, every database is added to a search engine powered by [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html). Searching covers the following data fields:
# 
# * `name`
# * `comment`
# * `product`
# * `categories`
# * `location`
# 
# Searching is done by using the `Database.search` method.

# In[13]:


Database("forwast").search("food")


# Searches can also be filtered—where only the results that meet the specified criteria are *included*,  or masked—where results that meet the specified criteria are *excluded*.
# 
# By default we return 25 search results, but this can be changed by specifying the `limit` keyword argument.
# 
# You can also use `*` wild cards in search queries:

# In[14]:


Database("biosphere3").search("carb*", limit=10)


# You can specify inclusion or exclusion criteria for fields with `filter` and `mask`:

# In[15]:


Database("biosphere3").search("carbon", filter={"categories": 'forestry'})


# In[16]:


Database("biosphere3").search("carbon", limit=10, mask={"categories": 'forestry'})


# Finally, you can facet search results by another field. This is a bit complicated, so test your queries before assuming certain behaviour.

# In[17]:


sr = Database("biosphere3").search("carbon", facet="categories")
for key, value in sr.items():
    print("Facet term:", key, "\n\t", value[:2], "\n")


# ### Changing iteration order

# You can also change the way that processes are iterated over in the database. The default order is random:

# In[18]:


db = Database("forwast")

def print_10(db):
    for i, x in enumerate(db):
        if i < 10:
            print(x)
        else:
            break
            
print_10(db)


# You can sort by `location`, `name`, `product` (reference product), or `type`, by specifying the `order_by` property.

# In[19]:


db.order_by = "name"
print_10(db)


# If the above seems wrong, remember that the names start with `100`, `101`, etc.
# 
# Set `.order_by = None` to remove any ordering.
# 

# In[20]:


db.order_by = None


# Because accessing activities in the database is quite fast, you can also filter the activities you want by just iterating over the entire database:

# In[21]:


my_activities = [x for x in db if 'Electr' in x['name']]
my_activities


# ### Basic LCA calculations

# Let's pick a process and LCIA method. The original tutorial uses random everything and I was unlucky enough that my LCA score was 0. Let's try to select specific processes and methods. The next [notebook](BW_Tutorial_5_Calculation_Setups.ipybn) will show how to select a non-zero random method. For now, I just place one that I know it works.

# In[28]:


process = Database('forwast').random()
print(process)
method_key = ('EDIP (superseded)',
 'environmental impact',
 'photochemical ozone formation, low NOx POCP')
print(method_key)


# *A brief review of LCA calculations:*
# 
# In matrix-based LCA, we construct a **technosphere matrix**, which describes the inputs needed to produce different products (e.g. cars need metal and electricity), and a **biosphere matrix**, which describes the emissions and resource consumption associated with the production of each product (e.g. car manufacturing releases air emissions). These two matrices come from the life cycle inventory database(s). We also have a **functional unit**, which is what we are trying to assess, e.g. one car. 
# 
# So, to calculate the **life cycle inventory (LCI)** we need to (1) solve the linear system of the technosphere matrix and the functional unit, and (2) multiply it by the biosphere matrix.
# 
# To do **life cycle impact assessment (LCIA)**, we multiply the life cycle inventory by a **matrix of characterization factors**, which tell how bad different emissions and resource consumptions are.
# 
# For more details on the math, see the [manual](https://2.docs.brightway.dev/lca.html).
# 
# So, our first step is to specify the **functional unit**, which is relatively easy:
# 

# In[29]:


functional_unit = {process: 1}


# We can then instantiate our LCA object.

# In[30]:


lca = LCA(functional_unit, method_key)


# And do the LCI and LCIA calculations:

# In[31]:


lca.lci() # This one adjusts matrixes to their functional unit
lca.lcia() # This onemultiplies the LCI with the characterization factors


# 
# 
# Finally, we can print the LCA score:
# 

# In[32]:


lca.score


# You can reuse the same matrices but change the functional unit by using the `redo_lci` and `redo_lcia` functions:

# In[33]:


new_process = Database("forwast").random()
print(new_process)
lca.redo_lcia({new_process: 1})
lca.score


# ### Looking into the LCA object

# Looking into the LCA object. Wrap the following lines to see the items printed. If you want more detailed explanation of what these matrices mean, refer to the *Massimo Tutorial 1* found in the folder *BW2_Massimo_Tutorial*.

# In[46]:


lca.inventory # This is incomplete in the original notebook, I decided to see the inventory object.


# Let's see what is in this LCA thing, anyway.

# * The technosphere matrix

# In[47]:


lca.technosphere_matrix


# * The biosphere matrix

# In[48]:


lca.biosphere_matrix


# * The characterization matrix

# In[49]:


lca.characterization_matrix


# ### Graphing matrices

# To further understand what we just did, let's visualize the calculation results.

# In[59]:


import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10, 5]


# There might be warnings here, but you can ignore them.

# In[60]:


from bw2analyzer.matrix_grapher import SparseMatrixGrapher


# First, let's look at the technosphere matrix.
# 
# You can pass in a filename to get a higher resolution figure saved as a file.

# In[68]:


SparseMatrixGrapher(lca.technosphere_matrix).ordered_graph(width=10, height=10)


# Not so interesting - I am sure your inventory data will be much nicer. The problem is that this is an IO matrix, so there is a value at each point, even if it is small, and this graph only shows where values are or aren't zero. 

# ### Contribution analysis

# We can calculate the most important activities and biosphere flows.

# In[71]:


from bw2analyzer import ContributionAnalysis


# Most important activities.

# In[84]:


ContributionAnalysis().annotated_top_processes(lca)


# In[ ]:





# Most important biosphere flows:

# In[81]:


ContributionAnalysis().annotated_top_emissions(lca)


# In[82]:


len(ContributionAnalysis().annotated_top_emissions(lca))


# ### Monte Carlo LCA

# Unfortunately, the FORWAST database doesn't include uncertainty. Let's put some in anyways, using the utility function `uncertainify`.

# In[85]:


from bw2data.utils import uncertainify
from stats_arrays import NormalUncertainty


# In[86]:


uncertain_db = Database("forwast uncertain +")
uncertain_db.write(
    uncertain_db.relabel_data(
        uncertainify(
            Database("forwast").load(), 
            NormalUncertainty
        ), 
        "forwast uncertain +" 
    )
)


# We can now calculate some Monte Carlo iterations for a random activity.

# In[87]:


mc = MonteCarloLCA(demand={uncertain_db.random(): 1}, method=method_key)
mc.load_data()
for x in range(10):
    print(next(mc))


# That's it! Here is your surprise! 

# In[89]:


from IPython.display import Image
dimensions = sorted((int(random.random() * 600 + 200), int(random.random() * 600 + 200)))
Image(url="https://magazine.washington.edu/columns_wordpress/wp-content/uploads/2018/06/Narwhal375.jpg")


# It is not a kitten. I know. But this is  narwhal. Narwhals are the unicorns of the sea. Have a wonderful day.

# Ok. Here is also a kitten.

# In[90]:


dimensions = sorted((int(random.random() * 600 + 200), int(random.random() * 600 + 200)))
Image(url="http://placekitten.com/{}/{}/".format(*dimensions))


# In[ ]:




