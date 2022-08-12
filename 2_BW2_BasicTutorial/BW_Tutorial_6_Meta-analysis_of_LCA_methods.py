#!/usr/bin/env python
# coding: utf-8

# # 6.  Meta-analysis of LCA methods

# This notebook assumes you have completed the [Tutorial 4 - LCA with real data](BW_Tutorial_4_LCA_Real_Data.ipynb) notebook, or its original version by Chris Mutel [Getting Started with Brightway2](https://github.com/brightway-lca/brightway2/blob/master/notebooks/Getting%20Started%20with%20Brightway2.ipynb).
# 
# This notebook shows the real power of Brightway2, and in particular the ability to script and analyze many LCA calculations.
# 
# At the end of this notebook, you should:
# 
# * Be able to make many LCA calculations.
# * Use `multiprocessing` to utilize the full power of your computer.
# * Store calculations results in `numpy` arrays, for analysis and interpretation.
# * Use matplotlib to display results graphically.
# 
# If you finish the notebook, you get another kitten!
# 
# You should `download this notebook` and run it cell by cell - don't just read it on the web!

# ### You know the drill.

# In[2]:


from brightway2 import *


# ### Project setup

# Let's copy the *LCA with real data* project to use the same database, and change the name to our new project. Keep in mind I will be copying the project based on _my_ notebooks. 

# In[3]:


if "Tut_4_RealLCA" not in projects:
        raise ValueError("Must have run introductory notebook already!")
        
if "Tut_6_Meta-analysis" not in projects:
    projects.set_current("Tut_4_RealLCA")
    projects.copy_project("Tut_6_Meta-analysis")
else:
    projects.set_current("Tut_6_Meta-analysis")

assert 'forwast' in databases, "Something went wrong - please run the introductory notebook again"


# In[4]:


print("There are {} activities in our database".format(len(Database('forwast'))))


# Let's start by picking some LCIA methods to analyze - we don't want to use all the available ones, as many are specific to just a few biosphere flows, and it wouldn't make sense to compare these methods to other methods.

# In[5]:


CANDIDATES = sorted([
    ('CML 2001 (superseded)', 'acidification potential', 'average European'),
    ('CML 2001 (superseded)', 'climate change', 'GWP 100a'),
    ('CML 2001 (superseded)', 'eutrophication potential', 'average European'),
    ('CML 2001 (superseded)', 'freshwater aquatic ecotoxicity', 'FAETP 100a'),
    ('CML 2001 (superseded)', 'human toxicity', 'HTP 100a'),
    ('CML 2001 (superseded)', 'land use', 'competition'),
    ('CML 2001 (superseded)', 'marine aquatic ecotoxicity', 'MAETP infinite'),
    ('CML 2001 (superseded)', 'resources', 'depletion of abiotic resources'),
    ('CML 2001 (superseded)', 'stratospheric ozone depletion', 'ODP 25a'),
    ('EDIP2003', 'ecotoxicity', 'in sewage treatment plants'),
    ('EDIP2003', 'eutrophication', 'terrestrial eutrophication'),
    ('EDIP2003', 'renewable resources', 'wood'),
    ('EDIP2003', 'stratospheric ozone depletion', 'ODP total'),
    ('EPS 2000', 'total', 'abiotic stock resources'),
    ('EPS 2000', 'total', 'emissions into soil'),
    ('EPS 2000', 'total', 'emissions into water'),
    ('EPS 2000', 'total', 'land occupation'),
    ('IMPACT 2002+ (Endpoint)', 'ecosystem quality', 'land occupation'),
    ('IMPACT 2002+ (Endpoint)', 'human health', 'ozone layer depletion'),
    ('IMPACT 2002+ (Endpoint)', 'resources', 'mineral extraction'),
    ('IMPACT 2002+ (Endpoint)', 'resources', 'non-renewable energy'),
    ('IMPACT 2002+ (Midpoint)', 'ecosystem quality', 'aquatic acidification'),
    ('IPCC 2013', 'climate change', 'GWP 100a'),
    ('ReCiPe Endpoint (H,A)',
    'ecosystem quality',
    'agricultural land occupation'),
    ('ReCiPe Endpoint (H,A)',
    'ecosystem quality',
    'freshwater eutrophication'),
    ('ReCiPe Endpoint (H,A)',
    'ecosystem quality',
    'natural land transformation'),
    ('ReCiPe Endpoint (H,A)',
    'ecosystem quality',
    'terrestrial acidification'),
    ('ReCiPe Endpoint (H,A)', 'ecosystem quality', 'urban land occupation'),
    ('ReCiPe Endpoint (H,A)', 'human health', 'particulate matter formation'),
    ('ReCiPe Endpoint (H,A)', 'resources', 'fossil depletion'),
    ('TRACI', 'environmental impact', 'acidification'),
    ('TRACI', 'environmental impact', 'eutrophication'),
    ('TRACI', 'environmental impact', 'global warming'),
    ('TRACI', 'environmental impact', 'ozone depletion'),
    ('TRACI', 'human health', 'respiratory effects, average'),
    ('ecological footprint', 'total', 'CO2'),
    ('ecological footprint', 'total', 'land occupation'),
    ('ecological footprint', 'total', 'nuclear'),
    ('ecological scarcity 2013', 'POP into water', 'total'),
    ('ecological scarcity 2013', 'energy resources', 'total'),
    ('ecological scarcity 2013', 'heavy metals into soil', 'total'),
    ('ecological scarcity 2013', 'heavy metals into water', 'total'),
    ('ecological scarcity 2013', 'land use', 'total'),
    ('ecological scarcity 2013', 'mineral resources', 'total'),
    ('ecological scarcity 2013', 'non radioactive waste to deposit', 'total'),
    ('ecological scarcity 2013', 'water resources', 'total'),
    ('ecosystem damage potential', 'total', 'linear, land occupation'),
    ('ecosystem damage potential', 'total', 'linear, land transformation'),
])

print("There are {} methods to test".format(len(CANDIDATES)))


# We will now compute an LCA score for each process in the `FORWAST` database, for each of these 52 methods. To do this, we use the [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) library to dispatch jobs to each available CPU core on our machine. We will store our results in an [numpy](https://numpy.org/) array.

# In[6]:


import numpy as np


# First, we create a function that will calculate the LCA score for one method and a list of activities. To do this, we use the ability of the `LCA` class to factorize the technosphere matrix into two triangular matrices (this is what `lca.decompose_technosphere()` does), which will make the actual LCI calculations very fast, on the order of 100 per second.
# 
# There are one potentially tricky thing we need to be aware of. We use the convenience method `redo_lcia`. This will change the LCA demand vector, but will cause an error if the new demanded activity is not in the foreground and background databases that form the technosphere matrix. This is the whole point of `redo_lci` and `redo_lcia` - if the technosphere doesn't change, then we can make calculations faster. If it does change, then we might as well create a whole new LCA object. Because we are drawing our list of activities from the same database, this is no problem, but it could be if we were to sample from different databases.
# 

# In[7]:


def calculate_everything(activities, method_list):
    results = np.zeros((len(activities), len(method_list)))
    
    lca = LCA({activities[0]: 1}, method=method_list[0]) # LCA object which will do all calculating
    lca.lci()                                    # Calculate inventory once to load all database data
    lca.decompose_technosphere()                 # Keep the LU factorized matrices for faster calculations
    lca.lcia()                                   # Load method data

    characterization_matrices = []
    for method in method_list:
        lca.switch_method(method)
        characterization_matrices.append(lca.characterization_matrix.copy())
        
    for first, activity in enumerate(activities):
        lca.redo_lci({activity: 1})
        
        for second, matrix in enumerate(characterization_matrices):
            results[first, second] = (matrix * lca.inventory).sum()
            
    return results


# Now we define the function that will dispatch the activities and methods using a `multiprocessing` pool. This isn't particularly difficult - just get sorted lists of the inputs, and use `apply_async` (there are also other possibilities, see the [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) documentation, or search for tutorials on the web.

# In[8]:


activities = sorted([dataset.key for dataset in Database("forwast")])


# Now, we are ready to do the actual calculation. Let's time it to see how long it takes us to make more than 50.000 LCA calculations...

# In[9]:


from time import time

start = time()
lca_scores = calculate_everything(activities, CANDIDATES)
elapsed = time() - start


# In[10]:


print("Done in {:.2f} seconds, at {:.1f} calculations per second".format(elapsed, lca_scores.shape[0] * lca_scores.shape[1] / elapsed))


# Well that was fast! Now we interpret these scores. Because they can be so different from method to method, if would be nice to normalize them. But first, let's do some basic sanity checks on the results:

# In[ ]:


print("Array shape:", lca_scores.shape)
print("Number of activities:", len(activities))
print("Average:", np.average(lca_scores))
print("Median (of absolute value):", np.median(np.abs(lca_scores)))
print("Min, Max:", np.min(lca_scores), np.max(lca_scores))
print("Fraction of all scores with score of zero:", (lca_scores == 0).sum() / float(lca_scores.shape[0] * lca_scores.shape[1]))
print("Methods where all scores are zero:", (lca_scores.sum(axis=0) == 0).sum())
print("Activities where all scores are zero:", (lca_scores.sum(axis=1) == 0).sum())
np.histogram(lca_scores)

