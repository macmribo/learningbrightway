#!/usr/bin/env python
# coding: utf-8

# # 1 &ensp; From project creation to LCA calculations

# These series of notebooks replicate those from [Brightway Seminar 2017 by Chris Mutel and Pascal Lesage](https://github.com/PoutineAndRosti/Brightway-Seminar-2017). Please go there for a full experience. This one is a more 'in a nutshell' version. I used the FORWAST database. An extra feature of this notebook is that all the links are updated to the [new official documentation page](https://2.docs.brightway.dev/index.html).
# 
# Use this notebook if you don't have ecoinvent, otherwise go to Chris Mutel's!
# 
# At the end of this notebook you will be able to:
# * Create a project.
# * Import databases.
# * Extract, search, manipulate and understand: activities, exchanges and methods.
# * Understand how the LCI and LCIA matrices are derived.
# * Calculate LCA of single functional units.
# * Compare multiple LCAs.
# * Run multiple LCAs.

# ## 1.1 &ensp; Project creation

# Import relevant packages. There are two ways to import Brightway2, `import brightway2 as bw` or, `from brightway2 import *`. The latter allows you to work without the `bw.` caller.

# In[1]:


import brightway2 as bw


# In[2]:


import os               # to use "operating system dependent functionality"
import numpy as np      # "the fundamental package for scientific computing with Python"
import pandas as pd     # "high-performance, easy-to-use data structures and data analysis tools" for Python


# Check project directory, current project, list projects and create/set a project folder, respectively:

# In[3]:


bw.projects.dir


# In[4]:


bw.projects.current


# In[5]:


bw.projects.report();


# In[6]:


bw.projects.set_current('MW_1')


# Setup biosphere and LCIA methods with `bw2setup()`.

# In[7]:


bw.bw2setup()


# In[8]:


bw.databases


# In[9]:


bw.Database('biosphere3')


# ## 1.2 &ensp; Extracting and searching activities and exchanges

# Here you can see all the methods you can call on the bw object:

# In[10]:


dir(bw);


# Let's assign the database to a variable:

# In[11]:


my_bio = bw.Database('biosphere3')


# In[12]:


type(my_bio)


# In[13]:


len(my_bio)


# Let's check its properties and methods:

# In[14]:


dir(my_bio);


# Some of the more basic ones we will be using now are :  
#   - `random()` - returns a random activity in the database
#   - `get(*valid_exchange_tuple*)` - returns an activity, but you must know the activity key
#   - `load()` - loads the whole database as a dictionary.
#   - `make_searchable` - allows searching of the database (by default, it is already searchable)
#   - `search` - search the database  
#   
# Lets start with `random`:

# In[15]:


my_bio.random()


# It gives us a random bioosphere activity, to use it properly we need to assign it to a variable.

# In[16]:


random_biosphere = my_bio.random()
random_biosphere


# In[17]:


type(random_biosphere)


# The type is an **activity proxy**. Activity proxies allow us to interact with the content of the database. In the journey to and from the database, several translation layers are used:
# 
# SQLITE DATABASE *Binary tuples*
# 
# &#8595;
# 
# Peewee ORM *Python classs instance* (***ActivityDataset*** or ***ExchangeDataset***)
# 
# &#8595;
# 
# Brightway2 *Python class instance* (***Activity*** or ***Exchange***)

# BW *mostly* works with `Activity` or `Exchange`.
# 
# To see what the activity contains, we can convert it to a dictionary:

# In[18]:


random_biosphere.as_dict()


# Let's get some activities:

# In[19]:


my_bio.get(random_biosphere['code'])


# Activities can also be "gotten" via `get_activity`, but the argument is the activity **key**, consisting of a tuple with two elements: the database name, and the activity code.

# ##### **Exercise 1.2.1:** Use `bw.get_activity()` to retrieve the random biosphere activity. 

# In[20]:


code = random_biosphere['code']
databasename = 'biosphere3'
random_biosphere_key = (databasename, code)
bw.get_activity(random_biosphere_key)


# You can always find the `key` to an activity using the `.key` property:

# In[21]:


random_biosphere.key


# Let's now search through our database!

# In[22]:


my_bio.search('carbon dioxide'); # You can also use bw.Database('biosphere3').search('carbon dioxide')


# We can also iterate over the database, this method uses [*list comprehension*]https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions which allow us to add filters and personalize the search.

# In[23]:


[act for act in my_bio if 'Carbon dioxide' in act['name'] 
                                            and 'fossil' in act['name']
                                            and 'non' not in act['name']
                                            and 'urban air close to ground' in str(act['categories'])
]


# Activities returned by searches or list comprehensions can be assigned to variables, but to do so, one needs to identify the activity by index. Based on the above, I can refine my filters to ensure the list comprehension only returns one activity, and then choose it without fear of choosing the wrong one.

# In[24]:


activity_I_want = [act for act in my_bio if 'Carbon dioxide' in act['name'] 
                                            and 'fossil' in act['name']
                                            and 'non' not in act['name']
                                            and 'urban air close to ground' in str(act['categories'])]
activity_I_want


# ##### **Exercise 1.2.2:** Look for and assign to a variable an emission of nitrous oxide emitted to air in the "urban air" subcompartment.
# 

# In[25]:


exercise_activity = [act for act in my_bio if 'nitrogen' in act['name']
                                            and 'urban air' in str(act['categories'])]
exercise_activity


# Now we select the first one:

# In[26]:


exercise_activity = exercise_activity[0]
exercise_activity


# ## 1.3 &ensp; Methods

# As mentioned before, we also installed methods:

# In[27]:


list(bw.methods);


# Select a random method:

# In[28]:


bw.methods.random()


# This is just an informative tuple, to get the actual method we use:

# In[29]:


bw.Method(bw.methods.random())


# Of course, a random method is probably not useful except to play around. To find an actual method, one can again use list comprehensions. Let's say I am interested in using the IPCC2013 100 years method:

# In[30]:


[m for m in bw.methods if 'IPCC' in str(m) and ('2013') in str(m) and '100' in str(m)]


# We can select the one we are interested in like we did before, assigning it to a variable and choose by subscripting. 

# In[31]:


select1 = [m for m in bw.methods if 'IPCC' in str(m) and ('2013') in str(m) and '100' in str(m)][0]
select1


# We can also refine searches:

# In[32]:


ipcc2013 = [m for m in bw.methods if 'IPCC' in m[0]
                    and ('2013') in str(m)
                    and 'GWP 100' in str(m)
                    and 'no LT' not in str(m)][0]
ipcc2013


# In[33]:


type(ipcc2013)


# In[34]:


ipcc_2013_method = bw.Method(ipcc2013)


# Let's check the methods associated with this method object:

# In[35]:


dir(ipcc_2013_method);


# In[36]:


ipcc_2013_method.name


# In[37]:


ipcc_2013_method.metadata;


# In[38]:


ipcc_2013_method.metadata['unit']


# **Question:** What is inside this method object? Let's check it out!

# In[39]:


ipcc_2013_method.load();


# This is a list of tuples of the database, code and the characterization factor.

# ##### **Exercise 1.3.1:** Create a dictionary with `keys = elementary flow names` and `values = characterization factors `for the `TRACI` "respiratory effects, inorganics" method (including long-term emissions).  
# Bonus (optional): Generate a Pandas Series with the resulting dictionary. 

# In[40]:


# Query 1
[m for m in bw.methods if 'TRACI' in str(m)
                        and 'respiratory effects' in str(m)]


# Selecting:

# In[41]:


# Query 1
TRACI_resp_effect_tuple = [m for m in bw.methods if 'TRACI' in str(m)
                        and 'respiratory effects' in str(m)][0]
TRACI_resp_effect_tuple


# Now let's make a dictionary, let's assing the tuple to a `Method`:

# In[42]:


TRACI_resp_effect_method = bw.Method(TRACI_resp_effect_tuple)
TRACI_resp_effect_method


# In[43]:


TRACI_resp_effect_method.load()


# In[44]:


TRACI_resp_effect_dict = {bw.get_activity(ef[0])['name']:ef[1] for ef in TRACI_resp_effect_method.load()}
TRACI_resp_effect_dict


# In[45]:


# Bonus: put the whole thing in a neat Pandas series
pd.Series(TRACI_resp_effect_dict,
          name="{}, {}".format(TRACI_resp_effect_method.name, TRACI_resp_effect_method.metadata['unit']))


# ## 1.4 &ensp; LCI datasets

# There is a lot of information about LCI database in Brightway 2 and its structure in the [official documentation](https://2.docs.brightway.dev/intro.html#inventory-databases). But the best way to learn is to check one out!

# Chris uploads ecoinvent, since that is a licensed database, we will be using a different one: FORWAST, you can download it [here](https://lca-net.com/projects/show/forwast/).

# In[46]:


import zipfile
import os
from bw2data.utils import download_file
from pathlib import Path

if 'forwast' in bw.databases:
    print('Database has already been imported!')
else:
    filepath = ("database/forwast.bw2package.zip")
    dirpath = os.path.dirname(filepath)
    zipfile.ZipFile(filepath).extractall(dirpath)
    bw.BW2Package.import_file(os.path.join(dirpath, "forwast.bw2package"))


# Since this is a `bw2.package` you don't have to do anything else. Now, when you import other database like an `excel`, `xml` or `ecospold` types of databases, you need to run the following commands:
# * `your_database.apply_strategy()`:
# * `your_database.statistics()`: Check for unlinked activities.
# * `your_database.write_database()`:
# 
# After doing this, just save your database with a variable using  `db = bw.Database('name of the database')` so you can interact with it as a database object :)

# In[47]:


bw.databases


# Now we have two databases!

# In[48]:


fw = bw.Database('forwast')


# In[49]:


len(fw)


# ### 1.4.1 &ensp; LCI activities

# In the context of LCI databases, activities are the nodes "within the technosphere". They are therefore the columns in the technosphere matrix .
# There are different ways to get access to an activity. Let's use the `random()` method for now to explore a random activity in the forwast database.

# In[50]:


random_act = fw.random()
random_act


# To see what is stored in an activity object, let's convert our random act in a dictionary:

# In[51]:


random_act.as_dict()


# Notice one important thing: **no exchanges**!  
# Indeed, the exchanges and the activities are stored in two different tables of the `databases.db` database.  
# It is possible, however, to iterate through the exchanges of the activities.

# #### 1.4.1.1 &ensp; Searching and getting LCI activities

# This step is the same as the way we did it with the biosphere3 database.

# In[52]:


fw.search('glass', filter={'name':'waste'})


# In[53]:


random_act['location']


# In[54]:


# Using list comprehensions:
[act for act in fw if 'Recycling of glass' in act['name']
                    and 'DK' in act['name']
                    and 'GLO' in act['location']
][0]


# ##### **Exercise 1.4.1:** Return an activity for electricity production, steam and hot water power plants in Denmark.

# In[55]:


[act for act in fw if 'Electricity' in act['name']
                    and 'steam' in act['name']
                    and 'Denmark' in act['categories'][1]
][0] # Don't forget to select!
# Caution, capitalization (or lack of!) might affect the search query!


# ### 1.4.2 &ensp; LCI Exchanges

# **Exchanges** are the edges between nodes.
# 
# These can be:
# 
# * an edge between two activities within the *technosphere* (an element $a_{ij}$ of matrix $A$)
# 
# * edges between an activity in the *technosphere* and an activity in the *biosphere* (an element of the biosphere $b_{kj}$ matrix $B$)
# 
# One can iterate through all exchanges that have a given activity as `output` (uncomment if you want to see the output, it long).
# 

# In[56]:


# for exc in random_act.exchanges(): 
#     print(exc)


# 
# 
# One can also iterate through subsets of the exchanges:
# 
# * Technosphere exchanges: exchanges linking to other activities in the technosphere, `activity.technosphere()`
# * Biosphere exchanges: AKA elementary flows, linking to activities in the biosphere database `activity.biosphere()`
# * Production exchange: the reference flow of the activity `activity.production`
# 
# Let's assign a **technosphere exchange** to a variable to learn more about it:
# 

# In[57]:


random_techno_exchange = [exc for exc in random_act.technosphere()][0]
random_techno_exchange


# In[58]:


type(random_techno_exchange)


# Again, the type is a proxy (refer to the diagram above about the different translation layers).

# In[59]:


print('Amount: ', random_techno_exchange.amount) # Amount, or weight of the edge
print('Input: ', random_techno_exchange.input) # Activity the exchange stems from
print('Output: ', random_techno_exchange.output) # Activity the exchange terminates in
print('As dictionary: ', random_techno_exchange.as_dict) # Exchange as a dictionary


# Let's now look at a production exchange.

# ##### **Exercise 1.4.2:** Assign a biosphere flow to a variable, and check the following:

# * Is the output the same as for the technosphere exchange?
# * From what database does the biosphere exchange come from?
# * What is the amount of the exchange (i.e. the weight of the edge connecting the two activities)?
# 
# *NOTE:* If you get a `list index out of range error` when trying to subscript your list comprehension, it means your list comprehension is empty, i.e. that there are no biosphere flows associated with the activity.

# In[60]:


# Assign the exchange to a variable:
random_bio_exchange = [exc for exc in random_act.biosphere()][0]
random_bio_exchange


# In[61]:


# Output of biosphere exchange
random_bio_exchange.output


# In[62]:


# Is it the same as the output of the technosphere exchange? It should be!
random_bio_exchange.output == random_techno_exchange.output


# In[63]:


# Database of the random biosphere exchange input - `.input`directly returns the activity proxy!
random_bio_exchange.input.key[0]


# In[64]:


# Amount of exchange
random_bio_exchange['amount']


# ### 1.4.3 &ensp; Loaded LCI databases

# It is possible to load the entire database into a dictionary.
# 
# This greatly speeds up work if you need to iterate over all activities or exchanges. The resulting object is quite big, so you should do this only if the gain in efficiency is worth it.

# In[65]:


fw_loaded = fw.load()
fw_loaded; # As always, get rid of the ';' to see the output, it might take some time to load all!


# ## 1.5 &ensp; First LCA

# Brightway has a so-called `LCA` object. It is instantiated using `LCA(args)`.
# 
# The only required argument is a **functional unit**, described by a dictionary with keys = activities and values = amounts ([more here](https://2.docs.brightway.dev/lca.html?highlight=functional+unit#specifying-a-functional-unit)).
# 
# A second argument that is often passed is an LCIA method, passed using the method tuple.

# ### 1.5.1 &ensp; General syntax of LCA calculations

# Let's create our first LCA object using our random activity and our IPCC method.

# In[66]:


functional_unit = {random_act:1}
method = ipcc2013


# In[67]:


myFirstLCA_quick = bw.LCA(functional_unit, ipcc2013)


# These are the steps to get to the impact scores:

# In[68]:


myFirstLCA_quick.lci()    # Builds matrices, solves the system, generates an LCI matrix.
myFirstLCA_quick.lcia()   # Characterization, i.e. the multiplication of the elements 
                          # of the LCI matrix with characterization factors from the chosen method
myFirstLCA_quick.score    # Returns the score, i.e. the sum of the characterized inventory


# Let's not take a closer look at the LCA object and its methods/attributes. We'll do this by creating a new LCA object:

# In[69]:


myFirstLCA = bw.LCA(functional_unit, ipcc2013)


# ### 1.5.1 &ensp; The `demand` attribute

# With `.demand` we see the functional unit we defined:

# In[70]:


myFirstLCA.demand


# To access the actual activity from the demand, you would do this:

# In[71]:


demanded_act = list(myFirstLCA_quick.demand.keys())[0]
demanded_act


# In[72]:


demanded_act == random_act


# There are also other attributes that have simply not been built yet, such as the `demand_array` and the `score`. To generate them, we first need to actually build the matrices. This will be done when calling the `.lci()` method.

# ### 1.5.2 &ensp; Time for some theory: Solving the LCI system

# Before actually running the `.lci()` method, here's a quick refresher of the actual calculation that Brightway will need to do to calculate the inventory:
# 
# \begin{equation}
# g = BA^{-1}f
# \end{equation}
# 
# where:
# 
# * A: Technosphere matrix.
# * B: Biosphere matrix (i.e. matrix with elementary flows).
# * f: Final demand vector.
# * g: Inventory.
# 
# **Discussion:** Knowing what you do about the structure of Brightway (notably, activities and exchanges), what needs to happen to generate these matrices?
# 
# * How should the order of the rows and columns be determined?
# * How should we keep track of what is in each row and column?
# * The parameters in the matrices are sometimes actually probability distribution functions - how should we consider this uncertainty information?
# * The matrices are sparse, i.e. they are mostly made up of zeros. Should we consider this? Why? How?
# 
# Let's get some answers!
# 

# ### 1.5.3 &ensp; Building matrices

# #### 1.5.3.1 &ensp; Structured arrays

# LCI data imported in Brightway is stored in the `databases.db` database, discussed above.
# It is also stored in [numpy structured arrays](https://numpy.org/doc/stable/user/basics.rec.html). 
# 
# Let's load the structured array of the forwast database you are working with now as a neat pandas dataframe.

# In[73]:


fw.filepath_processed()


# In[74]:


your_structured_array = np.load(fw.filepath_processed())
pd.DataFrame(your_structured_array).head()


# In this array:
# 
# * `input and output` columns are integers that map to an activity. This mapping is found in the mapping.pickle file in the project directory and it looks something like this:

# In[75]:


pd.Series(bw.mapping).head()


# * `row` and `col` store *dummy* placeholder information about the location of the parameter in the matrices.
# * The `type` indicates whether the exchange is a **reference flow** (`type=0`), **technosphere exchange** (`type=1`) or **elementary flow** (`type=2`).
# * The other columns deal with uncertainty data. We'll cover that later, but one can always read about these columns in the `stats_arrays` [documentation](https://stats-arrays.readthedocs.io/en/latest/).
# 
# You can find more information about this matrix in the [official documentation](https://2.docs.brightway.dev/lca.html#turning-processed-data-arrays-in-matrices).
# 
# When the `.lci()` method is called, the structured arrays are used to build matrices. The code responsible to do this is in the `MatrixBuilder` [class methods](https://2.docs.brightway.dev/technical/bw2calc.html?highlight=matrixbuilder#bw2calc.MatrixBuilder).
# 
# The method `MatrixBuilder.build_dictionary` is used to take input and output values, respectively, and figure out which rows and columns they correspond to. The actual code is succinct - only one line - but what it does is:
# 
# 1. Get all unique values, as each value will appear multiple times
# 2. Sort these values
# 3. Give them integer indices, starting with zero.
# 
# This information on row and column indices is sufficient to build matrices. These matrices are build in a [COOrdinate sparse matrix format](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.html), where, for each exchange, three values are required: (1) row position, (2) column position, and (3) amount (the actual value). The sparse matrices are actually stored in [CSR format](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html#scipy.sparse.csr_matrix), but this is a detail.
# 
# Some more details are are found [here](https://2.docs.brightway.dev/lca.html?highlight=building+matrices#lca-calculations).
# 
# Let's now finally unpack what the `.lci()` does:
# 

# In[76]:


myFirstLCA.lci()


# Here's what the structured arrays *now* look like:

# In[77]:


pd.DataFrame(myFirstLCA.bio_params).head(5) # Technosphere parameters are at myFirstLCA.tech_params


# We see that the `row` and `col` numbers are no longer dummy variables, but that they actually have real matrix indices.

# #### 1.5.3.2 &ensp; Dictionaries that map between indices and activities

# One of the useful things that the MatrixBuilder produces are dictionaries that map row and column numbers to the keys of activities. There are three such dictionaries, all directly accessible as attributes of the LCA object:
# 
# * `activity_dict:` Columns in the **technosphere matrix** $A$ or **biosphere matrix** $B$.
# * `product_dict`: Rows in the **technosphere matrix** $A$
# * `biosphere_dict`: Rows in the **biosphere matrix** $B$
# 
# Here what this dictionary looks like:
# 

# In[85]:


myFirstLCA.activity_dict;


# So, if I know the key to my activity (which, again, is a `tuple` consisting of the database name and the activity code), I can read the column index (from `activity_dict`) or row index (from `product_dict` or `biosphere_dict` for the $A$ or $B$ matrices, respectively).
# 
# Let's find out what column is associated with the activity that is producing our final demand as reference flow.

# In[ ]:





# In[82]:


# Getting the key from the `demand` attribute:
act_key = list(myFirstLCA.demand)[0].key
# Getting the column number from the activity_dict:
col_index = myFirstLCA.activity_dict[act_key]
print("The column index for activity {} is {}.".format(act_key, col_index))


# While this is useful, it is often more useful to determine what a row or column in the matrices actually refers to. In these cases, we need a dictionary that maps row or column indices to activity keys, and not the opposite.
# 
# We can do this by reversing our dictionaries:

# In[86]:


myFirstLCA_rev_activity_dict = {value:key for key, value in myFirstLCA.activity_dict.items()}
myFirstLCA_rev_activity_dict;


# For convenience, Brightway offers a method that will generate the three reverse dictionaries simultaneously.
# `.reverse_dict()` returns three reverse dictionaries (reverse activity dict, reverse product dict, reverse biosphere dict) *in that order*. The syntax for creating and assigning these reverse dictionaries is:
# 

# In[87]:


myFirstLCA_rev_act_dict, myFirstLCA_rev_product_dict, myFirstLCA_rev_bio_dict = myFirstLCA.reverse_dict()


# #### 1.5.3.2 &ensp; $A$ and $B$ matrices

# 
# 
# We can also access the matrices that were constructed. Let's look at the **technosphere matrix** ($A$).
# 
# The $A$ matrix, with elements $a_{ij}$ provides information on the amount of input or output of product $i$ comes from activity $j$. When $i = j$, the element  $a_{ij}$  is the **reference flow** for the activity described in the column.

# In[88]:


myFirstLCA.technosphere_matrix


# The dimensions of the matrix is $n \times n$ where $n$ is the number of activities in my product system, and that the amount of actually stored elements is much less than $n^2$ (because the matrix is *sparse* and zero values are not stored).
# 
# We can have an idea of what it stores by printing it out:
# 

# In[90]:


print(myFirstLCA.technosphere_matrix)


# It therefore stores both the coordinates and the values (as expected). We can slice this matrix using coordinates. For example, let's say we wanted a view of the exchanges associated with the unit process providing our **functional unit**.
# 
# We already know found the column number for that activity:

# In[92]:


print("As a reminder, the column index for  {} is  {}.".format(act_key, col_index))


# To return the whole column from the matrix, we therefore slice the $A$ matrix.
# Python notes:
# 
# * In Python, slicing is done using []
# * e specify rows first, then columns
# * : refers to "the whole row" or "the whole column" (depending if it is passed first or second in the [])

# In[93]:


myColumn = myFirstLCA.technosphere_matrix[:, col_index]
myColumn


# In[94]:


print(myColumn)


# Not too useful: it would be better to get the **names to these exchanges**.
# 
# We need to do two things:
# 
# * Get the indices from the CSR matrix (we can do this by converting it to a sparse matrix in `COOrdinate` format first)
# * Get the activity code for the each index (we can do this using the reverse of the activity_dict)
# * Use `get_activity` to access the actual names of the activities.

# 1) Converting the CSR matrix to a COO matrix:

# In[95]:


myColumnCOO = myColumn.tocoo()
myColumnCOO


# It is still a sparse matrix with the same number of elements, and it looks quite like the CSR version when we print it out:

# In[96]:


print(myColumnCOO)


# 2) Get the activity code for each element using the **reverse product dictionary** we produced above:

# In[98]:


# Using a list comprehension:
[myFirstLCA_rev_product_dict[i] for i in myColumnCOO.row];


# It would be even nicer to get the names for these:

# In[100]:


names_of_my_inputs = [bw.get_activity(myFirstLCA_rev_product_dict[i])['name'] for i in myColumnCOO.row]
names_of_my_inputs;


# We can put these in a neat Pandas Series, with actual names and amounts:

# In[101]:


# First create a dict with the information I want:
myColumnAsDict = dict(zip(names_of_my_inputs,myColumnCOO.data))
# Create Pandas Series from dict
pd.Series(myColumnAsDict, name="Nice series with information on exchanges in my foreground process")


# Alternative way to generate similar information without even looking at the matrices:

# In[102]:


pd.Series({bw.get_activity(exc.input)['name']:exc.amount for exc in random_act.technosphere()}, 
          name="alternative way to generate exchanges")


# Note the differences:
# 
# * The reference flow is not there (activity.technosphere() only returns technoshere exchanges where the input is not equal to the output).
# * The values are positive, not negative (because the $A$ matrix is $I - Z$ where $Z$ contains the information on these inputs.

# ##### **Exercise 1.5.1:** Create a Pandas Series with the elementary flows of the activity supplying the reference flow for myFirstLCA.
# 

# In[180]:


myBioColumn = myFirstLCA.biosphere_matrix[:, col_index]
myBioColumn


# In[123]:


myBioColumnCOO = myBioColumn.tocoo() # Add .data to get an array with the values
#myBioColumnCOO


# In[126]:


myBioNames = [bw.get_activity(myFirstLCA_rev_bio_dict[row])['name'] for row in myBioColumnCOO.row]
#myBioNames


# In[127]:


myBioDict = dict(zip(myBioNames,myBioColumnCOO.data))
pd.Series(myBioDict)


# #### 1.5.3.3 &ensp; Demand array $f$

# The demand array is the $f$ in $A s = f$ (where $s$ is the supply array. It is an attribute of the LCA object.

# In[128]:


myFirstLCA.demand_array


# Looks like it is all zeros, but not so. Can you spot the one?

# In[129]:


myFirstLCA.demand_array.sum()


# If you don't want to manually search the `1` like where is [Waldo](https://en.wikipedia.org/wiki/Where%27s_Wally%3F), we can know this by using our `activity_dict`.
# 

# In[130]:


demand_database = list(myFirstLCA.demand.keys())[0]['database']
demand_code = list(myFirstLCA.demand.keys())[0]['code']
(demand_database, demand_code)


# In[131]:


row_of_demand = myFirstLCA.activity_dict[(demand_database, demand_code)]
row_of_demand # Row number of our demand vector containing the functional unit.


# In[132]:


myFirstLCA.demand_array[row_of_demand]


# ### 1.5.4 &ensp; Solution to the inventory calculation

# Recap on the math, we want to solve the following equation:
# 
# \begin{equation}
# g = BA^{-1}f
# \end{equation}
# 
# Now we add the supply array $s$ which is the product of the inverse of the **technosphere matrix** $A$ and the demand array $f$. Therefore we have:
# 
# \begin{equation}
# g = Bs
# \end{equation}
# 
# We saw above how `.lci()` produced the $A$ and $B$ matrices.
# `.lci()` also solves the equation $As = f$ and calculates the inventory by multiplying the solution to this equation by the **biosphere matrix**.

# #### 1.5.1.1 &ensp; Supply array $s$

# Vector containing the amount each activity, it will need to provide to meet the functional demand, i.e. $s = A^{-1}f$.

# In[134]:


myFirstLCA.supply_array;


# In[135]:


myFirstLCA.supply_array.shape


# #### 1.5.1.1 &ensp; Inventory matrix $g$

# Contains the inventory by *activity* (i.e. not summed). In other words, we do not have $g = BA^{-1}f$, but rather  $G = B \cdot diag(A^{-1}f)$

# In[136]:


myFirstLCA.inventory


# We can aggregate the LCI results along the columns (i.e. calculate the **cradle-to-gate inventory**):

# In[137]:


LCI_cradle_to_gate = myFirstLCA.inventory.sum(axis=1)
LCI_cradle_to_gate.shape


# ##### **Exercise 1.5.2:** Get the total (cradle-to-gate) emissions of nitrogen oxide emitted to air in the "urban air" subcompartment.

# I had an issue replicating this exercise since the emissions were different in mine and it does not have 'urban air' subcompartment. What I did was finding the code in `myFirstLCA.biosphere_dict` that has a nitrogen oxide and directly setting it to the value. I know it is not the smartest, but I will keep practicing search queries.

# In[234]:


NOx_act = [act for act in my_bio if act['code'] == 'c1b91234-6f24-417b-8309-46111d09c457'][0]
NOx_act


# In[231]:


NOx_act.key


# In[232]:


NOx_row = myFirstLCA.biosphere_dict[NOx_act]
NOx_row


# In[236]:


print('Producing 1 kg of the random activity uses', myFirstLCA.inventory[NOx_row, :].sum(), 'kg of nitrogen oxide.')


# What is the environmental/health factor of this? This is why we need the LCIA calculation!

# ### 1.5.5 &ensp; LCIA calculation

# The LCIA calculation is done via the `.lcia()` method.

# In[237]:


myFirstLCA.lcia()


# Two additional matrices are now available:
# * Characterization matrix.
# * Characterized inventory.
# 

# In[238]:


myFirstLCA.characterization_matrix # Matrix of characterization factors
print(myFirstLCA.characterization_matrix.shape)

myFirstLCA.characterized_inventory # Matrix of characterized inventory flows
print(myFirstLCA.characterized_inventory.shape)


# **Question:** Why are there more elements in the characterized inventory than in the characterization matrix?

# The overall score is now an attribute of the `LCA` object:

# In[239]:


myFirstLCA.score


# But what does this score mean? Remember the method we used? That is where we define the impact factor we are interested in. 
# 
# `('IPCC 2013', 'climate change', 'GWP 100a')` means that we want the IPCC 2013 score of the **impact category** `climate change`, more specifically, we want the `GWP 100a` or the Global Warning Potential, with units Kg CO<sub>2</sub>-eq, (some other methods might have more considerations within the same impact category). 

# We also could have determined what this score was by summing the elements of our `characterized_inventory` matrix:

# In[240]:


myFirstLCA.characterized_inventory.sum()


# We could also have calculated it by multiplying the inventory and characterization factors ourselves:

# In[241]:


(myFirstLCA.characterization_matrix * myFirstLCA.inventory).sum()


# We could also calculate the score by elementary flow (summing columns for each rows), irrespective of the unit process that produced it:

# In[244]:


elementary_flow_contribution = myFirstLCA.characterized_inventory.sum(axis=1) #Axis is the dimension I want to sum over:
print(elementary_flow_contribution.shape)
elementary_flow_contribution


# Notice that is has **two** dimensions. The result is in fact a one-dimensional matrix:

# In[245]:


type(elementary_flow_contribution)


# To convert it to an array (probably more useful for many purposes), you can use any of the following approaches (they all have exactly the same output).

# In[248]:


elementary_flow_contribution.A1 
#np.squeeze(np.asarray(elementary_flow_contribution))
#np.asarray(elementary_flow_contribution).reshape(-1)
#np.array(elementary_flow_contribution).flatten()
#np.array(elementary_flow_contribution).ravel()


# ##### **Exercise 1.5.2:** Create a Pandas series that has the scores per unit process, sorted by value (contribution analysis).
# 
# 

# In[256]:


# Create array with the results per column (i.e. per activity)
results_by_activity = (myFirstLCA.characterized_inventory.sum(axis=0)).A1
results_by_activity;


# In[257]:


# Create a list of names in columns
list_of_names_in_columns = [bw.get_activity(myFirstLCA_rev_act_dict[col])['name'] 
                            for col in range(myFirstLCA.characterized_inventory.shape[1])]


# In[258]:


pd.Series(index=list_of_names_in_columns, data=results_by_activity).sort_values(ascending=False).head(10)


# ## 1.6 &ensp; Second LCA: Comparative LCA

# Let's choose two activities to compare, say coal production betweeen Denmark and Europe in general.
# 
# Exercise: 
# 

# ##### **Exercise 1.5.2:** Assign the two activities to variables DK and EU respectively.

# In[279]:


[act for act in fw if "Coal" in act['name']]


# In[280]:


DK = [act for act in fw if "Electricity" in act['name']][1]
EU = [act for act in fw if "Electricity" in act['name']][0]


# Let's also compare these according to their carbon footprint as measured with the IPCC method we already selected above:

# In[269]:


ipcc_2013_method


# ### 1.6.1 &ensp; One at a time approach

# In[283]:


DKCoalLCA = bw.LCA({DKCoal:1}, ipcc_2013_method.name)
DKCoalLCA.lci()
DKCoalLCA.lcia()
DKCoalLCA.score



# ##### **Exercise 1.5.3:** Do the LCA for Europe.
# 

# In[282]:


EUCoalLCA = bw.LCA({EUCoal:1}, ipcc_2013_method.name)
EUCoalLCA.lci()
EUCoalLCA.lcia()
EUCoalLCA.score


# In[317]:


#Compare results:
if DKCoalLCA.score>EUCoalLCA.score:
    print("The Danish coal GWP is above the Europe average.")
elif DKCoalLCA.score<EUCoalLCA.score:
    print("The Danish coal GWP is below the Europe average.")
else:
    print("Both options have the same climate change indicator result")


# ### 1.6.2 &ensp; "Delta" LCA approach

# In[290]:


deltaLCA = bw.LCA({DKCoal:1, EUCoal:-1}, ipcc_2013_method.name)
deltaLCA.lci()
deltaLCA.lcia()
deltaLCA.score


# In[318]:


#Compare results:
if deltaLCA.score>0:
    print("The Danish coal GWP is above the Europe average.")
elif deltaLCA.score<0:
    print("The Danish coal GWP is below the Europe average.")
else:
    print("Both options have the same climate change indicator result")


# ## 1.7 &ensp; Third LCA: Multiple impact categories

# Say we want to evaluate the indicator results for our `random_act` for all [ReCiPe](https://www.rivm.nl/en/life-cycle-assessment-lca/recipe) midpoint categories (with long-term emissions).

# In[298]:


# Make a list of all impact method names (tuples):
RCP_mid = [method for method in bw.methods if "ReCiPe" in str(method) and "Midpoint" in str(method) and "no LT" not in str(method)]
RCP_mid;


# So much to choose from!

# Simplest way: for loop, using `switch` method:

# In[300]:


myThirdLCA = bw.LCA({random_act:1}, RCP_mid[0]) # Do LCA with one impact category
myThirdLCA.lci()
myThirdLCA.lcia()
for category in RCP_mid:
    myThirdLCA.switch_method(category)
    myThirdLCA.lcia()
    print("Score is {:f} {} for category {}".format(myThirdLCA.score, 
                                                 bw.Method(category).metadata['unit'],
                                                 bw.Method(category).name)
          )


# In[301]:


myFirstLCA_unitProcessContribution = myFirstLCA.characterized_inventory.sum(axis=0).A1
myFirstLCA_unitProcessRelativeContribution = myFirstLCA_unitProcessContribution/myFirstLCA.score


# ## 1.8 &ensp; Revisiting second and third LCA with `MultiLCA`

# The `MultiLCA` method allows the calculation of LCA results for multiple functional units and impact categories.
# One simply needs to create a calculation setup, i.e. a named set of functional units and LCIA methods.
# 
# Calculation setups: dictionary with lists of functional units and methods.

# In[316]:


list_functional_units = [{DKCoal.key:1}, {EUCoal.key:1}]
list_methods = RCP_mid


# In[321]:


bw.calculation_setups['DK_vs_EU_coal'] = {'inv':list_functional_units, 'ia':list_methods}
bw.calculation_setups['DK_vs_EU_coal'];


# In[322]:


myMultiLCA = bw.MultiLCA('DK_vs_EU_coal')


# In[323]:


myMultiLCA.results.shape


# In[325]:


myMultiLCA.results;


# In[327]:


pd.DataFrame(index=RCP_mid, columns=[DKCoal['name'], EUCoal['name']], data=myMultiLCA.results.T)


# You can also create "fuller" DataFrames. Here is with code from [here](https://stackoverflow.com/questions/42984831/create-a-dataframe-from-multilca-results-in-brightway2):

# In[330]:


scores = pd.DataFrame(myMultiLCA.results, columns=myMultiLCA.methods)

as_activities = [
    (bw.get_activity(key), amount) 
    for dct in myMultiLCA.func_units 
    for key, amount in dct.items()
]
nicer_fu = pd.DataFrame(
    [
        (x['database'], x['code'], x['name'], x['location'], x['unit'], y) 
        for x, y in as_activities
    ], 
    columns=('Database', 'Code', 'Name', 'Location', 'Unit', 'Amount')
)
pd.concat([nicer_fu, scores], axis=1).T


# You can even generate beautiful heatmaps like this in a relatively easy way, see example notebook [here](./2_BW2_BasicTutorial/BW_Tutorial_5_Calculation_Setups.ipynb)

# In[ ]:




