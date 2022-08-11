#!/usr/bin/env python
# coding: utf-8

# # Introductory note
# <a id='section0'></a>
# This is a [Jupyter Notebook](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html) with the purpose of making you familiar with the basic Python-based [Brightway2 LCA framework](https://brightwaylca.org/) and its various functionalities, all developed by [Chris Mutel and colleagues](https://2.docs.brightwaylca.org/credits.html#authors).
# 
# This notebook is designed to get you started with creating your own project, setting up your database(s) (used as background systems) and simple foreground systems, performing your first impact assessments, analysing your results, and running Monte Carlo simulations in calculation setups.
# 
# Since Brightway2 builds on Python, a widely used programming language for scientific analysis, and can be installed easiest through the package and environment mangement system [*conda*](https://docs.conda.io/projects/conda/en/latest/), we need to get either [Anaconda](https://www.anaconda.com/), an open source distribution for multiple languages including Python and R, or at least [Miniconda](https://docs.conda.io/en/latest/miniconda.html), the bootstrap version of Anaconda. The full Anaconda installation contains, among others, a terminal and an IDE (integrated development environment). And, good for us, it natively installs the setup for Jupyter Notebooks, through which we can work most effectively with Brightway2. Both Jupyter and Brightway can also be installed through [*pip*](https://jupyter.readthedocs.io/en/latest/install.html#new-to-python-and-jupyter), but it may be a tad trickier.
# 
# For clarification: *conda* is, just like *pip*, a package and environment management system; the difference, however, is that "*pip* installs python packages within any environment; *conda* installs any package within conda environments." (quote from [here](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/))
# 
# <br>
# 
# ---
# 
# **Recommended prerequisites are:**
# * having installed [Brightway2](https://2.docs.brightwaylca.org/installation.html) + all relevant packages (make sure to do so in the correct virtual environment) and possibly even having had a first quick look at its [documentation](https://docs.brightwaylca.org/index.html). <ins>*Credits where credits are due:*</ins> much of the present notebook is based both directly and indirectly on this documentation (and the [example notebooks](https://docs.brightwaylca.org/notebooks.html#example-notebooks))
# * knowledge of the foundations of life cycle assessment. If you don't have this knowledge (or simply need a refresher), have a look at the [online teaching resources](http://www.teaching.industrialecology.uni-freiburg.de/) provided by the Industrial Ecology Freiburg Group, led by Stefan Pauliuk
# * familiarity with any programming language - no Python-specific requirements, as most methods are quite intuitive and will be explained anyway. In case you are a bloody beginner, check [this](https://github.com/PoutineAndRosti/Brightway-Seminar-2017/blob/master/Day%201%20AM/1%20-%20Python%20and%20notebook%20basics.ipynb) out :)
# 
# <br>
# 
# ---
# 
# **For Jupyter newbies**
# 
# In a [Jupyter notebook](https://jupyter-notebook.readthedocs.io/en/stable/index.html) everything is live and interactive. And, perhaps more interesting, markdown elements and actual code are mixed - and you can even include images, videos, and other formats. There are [many](https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks), [many](https://rise.readthedocs.io/en/maint-5.5/index.html) things that you can do with such notebooks, and there are also many [cool](https://blog.dominodatalab.com/lesser-known-ways-of-using-notebooks/) [tricks](https://www.dataquest.io/blog/jupyter-notebook-tips-tricks-shortcuts/) as well as some [extensions](https://github.com/ipython-contrib/jupyter_contrib_nbextensions).
# 
# To get you started, you might want to press the `h`-key, which gives you an overview of keyboard shortcuts. Then, you have markdown (richt text containing) cells and code cells: if you hover over and select any cell by clicking on it (notice the blue bar on the left of the cell; turns green when you are in edit mode, i.e. having clicked into the cell box) you can turn it into either a markdown one by pressing `m` or into a code cell by pressing `y`; there are other types, too, but they are not relevant for what we want to do. Click on a cell to select it or simply use the arrow keys to navigate. If you want to run a cell, simply press `shift+enter`. And if you want to insert an empty cell above or below the current one, simply press `a` or `b`. For changing the contents of a cell, either doubleclick a markdown cell or click a code cell; pressing `enter` works, too. You can exit a cell using `Esc` and can copy, cut, and paste cells when pressing the keys `c`, `x`, and `v` when having selected a cell. As for the output of a command, note that clicking on it once makes it scroll-able, clicking on it twice results in hiding it.
# 
# You will notice further below that there are sometimes commands starting with `import`. These ones are needed to "import" the code of the respective package into the present code. For instance, by importing the Brightway2 package you enable the present notebook to use the Brightway2 functionalities. To have access to these packages, you need to download them first; otherwise you will receive an error message. You can download such packages in two ways: either in the notebook or in the terminal (make sure to be in the right virtual environment). To find out more about that I would advise you to use the search engine of your choice ;)
# 
# These are the absolute basics, but they are already more than what you need here. Because you basically just need to run the presented cells.
# 
# <br>
# 
# ---
# 
# **Recap on LCA**
# 
# To make sure we are on the same page, let's recapitulate the basics of LCA, expressed in a single formula (the notation may differ to the one that you are familiar with):
# 
# $$h = CBA^{-1}f$$
# 
# where:
# - $A$... transaction matrix (dimensions *p x q*)
# - $B$... environmental interventions matrix (dimensions *r x q*)
# - $C$... characterisation matrix (dimensions *p x q*)
# - $f$... final demand vector (dimensions *p x 1*)
# - $h$... characterised inventory matrix (dimensions *1 x 1*)
# 
# with the dimensions being:
# - *p*... number of products
# - *q*... number of activities/processes
# - *r*... number of elementary flows
# 
# Specific parts of the above formula have distinct names. Since these names are also used in the Brightway2-framework, we will note them down here:
# - $f$... demand array
# - $A{^-1}f$... supply array
# - $BA{^-1}f$... inventory
# - $CBA{^-1}f$... characterised inventory
# 
# To not only get a single score per impact category, we can diagonalise the supply array (how this can be realised in the Brightway2-framework is not shown in this notebook) so that we can see the environmental impacts per process:
# 
# $$h_{process} = CB~diag(A^{-1}f)$$
# 
# You can do the same for breaking down the total environmental impact to the stressors:
# 
# $$h_{stressor} = C~diag(BA^{-1}f)$$
# 
# Another way of representing your results is to show the environmental stressors per activity for a specific impact category:
# 
# $$h_{category} = diag(C)~B~diag(A^{-1}f)$$
# 
# <br>
# 
# ---
# 
# **The notebook is structured as follows:**
# 1. [Setup of a project](#section1): *How to set up a project to work in*
# 2. [Database import/setup](#section2): *How to import a database and get it ready for use*<br><br>
#     2.1 [Importing ecoinvent and Forwast](#section21)<br>
#     2.2 [Database selection and a first look at activities](#section22)<br>
#     2.3 [Importing a dataset from Excel](#section23)<br><br>
# 3. [Manual database creation](#section3): *How to manually create a database*
# 4. [LCIA](#section4): *Basics of the LCIA calculations*
# 5. [Foreground system](#section5): *How to set up a very simple product system and ways to explore BW2's functionalities*<br><br>
#     5.1 [Simple product system](#section51)<br>
#     5.2 [Bottle production](#section52)<br><br>
# 6. [Manipulating an exchange](#section6): *How to manipulate an activity in multiple ways*<br><br>
#     6.1 [Copying and deleting an activity](#section61)<br>
#     6.2 [First attempts at manipulating an exchange's keys/values](#section62)<br>
#     6.3 [Substituting an exchange](#section63)<br>
#     6.4 [Successfully manipulating an exchange](#section64)<br><br>
# 7. [Basic contribution analysis](#section7): *How to examine the LCA results*<br><br>
#     7.1 [Recalculation of the inventory](#section71)<br>
#     7.2 [Basic contribution analysis](#section72)<br>
#     7.3 [Top emissions and processes by name](#section73)<br><br>
# 8. [Multi-LCA](#section8): *How to compare multiple alternatives across multiple impact categories simultaneously*<br><br>
#     8.1 [Manually comparing products](#section81)<br>
#     8.2 [Calculation setups](#section82)<br>
#     8.3 [MLCA](#section83)<br><br>
# 9. [Monte Carlo simulation](#section9): *How to quantify uncertainties of the LCA result*<br><br>
# 
# <br>
# 
# ---
# 
# **Outcomes - what are we going to learn?**
# 
# By completing this notebook (run it locally on your machine and don't just read the code), we will:
# - have understood the basics of the Brightway2 LCA framework
# - know how to import/generate/handle datasets in Brightway2
# - be able to run simple LCAs (both linearly and in parallel)
# - be able to analyse a product system and the results of an LCA
# - be able to visualise data in form of tables and figures
# - be rewarded with a dabbing 🦄
# 
# <br>
# 
# ---
# Just for clarification, abbreviations used in the markdown cells of this notebook are:
# 
# | Abbreviation(s) | Written out |
# | --- | --- |
# | bw, BW2 | Brightway2 |
# | FU | Functional unit |
# | LCA | Life cycle assessment |
# | LCI | Life cycle inventory |
# | LCIA | Life cycle impact assessment |
# 
# ---
# 
# So, that would be it what we're up to do. But if you're super keen then you might also be interested in checking out the **[Activity browser](https://github.com/LCA-ActivityBrowser/activity-browser)** and **[LCOPT](https://lcopt.readthedocs.io/en/latest/)**, both of which are essentially graphical user interfaces for BW2. The latter one can be used particularly for parametrised inventories (you'll learn more about the basics of this later).
# 
# <br>
# 
# ---

# <a id='section1'></a>
# # 1. Setup of a project
# 
# A project gets instantiated and relevant libraries/modules imported.

# In[1]:


import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import brightway2 as bw
from brightway2 import *
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter, Group


# Let's list the available projects. There are two ways for doing so:

# In[2]:


list(bw.projects)


# In[3]:


#same as above
bw.projects


# We can get more information (installed databases and file sizes) on the individual projects with the following command:

# In[4]:


bw.projects.report()


# ... and also see where they are stored:

# In[5]:


bw.projects.dir


# We can also create sub-directories for e.g. to-be-generated data:

# In[6]:


projects.request_directory("my-new-directory")


# But we won't need this here, so let's delete it again:

# In[7]:


import shutil
os.rmdir(os.path.join(bw.projects.dir, 'my-new-directory'))


# To create a new project or to access an existing one, we type in:

# In[8]:


bw.projects.set_current("maximikos_StepByStep") #Creating/accessing the project
bw.bw2setup() #Importing elementary flows, LCIA methods and some other data


# In[9]:


#now we see that we have created our first project
bw.projects


# To see where your current project is stored, type:

# In[10]:


bw.projects.dir


# **Troubleshooting**
# 
# Sometimes not everything goes as intended (depending on many different factors) and there may be some problems occurring when executing Brightway specific commands. Then it helps to examine the system paths for all respective modules, see where the binary Python interpreter is located, and list which kernels are available and where they are located.

# In[11]:


import sys


# In[12]:


sys.executable


# In[13]:


sys.path


# In[14]:


get_ipython().system('jupyter kernelspec list')


# **Magic commands**

# For unexperienced python users it may be interesting to check out some *magic commands* that can be quite helpful, for example when timing the execution of a command. A list of available *magic commands* can be found below.

# In[15]:


lsmagic


# Just two examples:

# In[16]:


get_ipython().run_line_magic('pwd', '')
#returns the path to the current folder
#same output as:
#os.getcwd()


# In[17]:


import math
get_ipython().run_line_magic('timeit', 'math.sqrt(42)')

#compare this with the time needed for the simple command:
#%time math.sqrt(42)


# Btw, if you don't know how a method works, just add a "?" behind, e.g. for this magic command:

# In[18]:


get_ipython().run_line_magic('pinfo', 'alias')


# ... or "??" to see the actual code of this method.

# In[19]:


get_ipython().run_line_magic('pinfo2', 'alias')


# **Continue, or back to [table of contents](#section0)?**
# ***

# <a id='section2'></a>
# # 2. Database import/setup

# <a id='section21'></a>
# ## 2.1 Importing ecoinvent and Forwast
# 
# LCA draws on a lot of background data. Those can be found in numerous databases, for instance ecoinvent. We can check which databases are available in the current project with the following command:

# In[20]:


#list the available databases
bw.databases


# If the list does not yet include the database we want, we can import it. As an example, we first import FORWAST and then the 3.5 ecoinvent cut-off database and check on some of the import's statistics:

# In[ ]:


#FORWAST
import zipfile
from bw2data.utils import download_file

if 'forwast' in bw.databases:
    print("Database has already been imported.")
else:
    filepath = download_file("forwast.bw2package.zip", url="http://lca-net.com/wp-content/uploads/")
    dirpath = os.path.dirname(filepath)
    zipfile.ZipFile(filepath).extractall(dirpath)
    BW2Package.import_file(os.path.join(dirpath, "forwast.bw2package"))


# In[ ]:


#ecoinvent
if 'ecoinvent 3.5_cutoff_ecoSpold02' in bw.databases:
    print("Database has already been imported.")
else:
    # mind that the ecoinvent file must be unzipped; then: path to the datasets subfolder
    fpei35cut = r"C:\Users\Maximilian Koslowski\Forschung\Ecoinvent\3.5\ecoinvent 3.5_cutoff_ecoSpold02\datasets"
    # the "r" makes sure that the path is read as a string - especially useful when you have spaces in your string
    ei35cut = bw.SingleOutputEcospold2Importer(fpei35cut, 'ecoinvent 3.5_cutoff_ecoSpold02')
    ei35cut
    ei35cut.apply_strategies()
    ei35cut.statistics()


# If unlinked exchanges are present: If that happens (it might for other versions of ecoinvent!) and we want to understand the details of it, we first check the proper exchange linkages in the logfile of the import:

# In[ ]:


#open the logfile and check the deleted exchanges
fp = r"C:\Users\Maximilian Koslowski\AppData\Local\pylca\Brightway3\Logs\3Dprinting-LCA.674d125927554cffbf495553d43372bd\Ecospold2-import-error.FyZMwV.log"

with open(fp) as f:
    lines = [x.strip() for x in f]

for line in lines[:26]:
    print(line)


# And then we check what the actual flows of the respective activities are:

# In[ ]:


#mind that the identifiers looked for below were used when linking the consequential ecoinvent 3.5 database, hence "fpei35con"
for filename in os.listdir(fpei35con):
    if "874057b2-e4e0-446c-be44-ff2881801e9f" in filename:
        print(filename)
    if "7757e24e-897e-4b07-8ca9-87bb8dbe3016" in filename:
        print(filename)


# As of now, no better way of handling this issue exists than simply deleting such exchanges (as was done automatically). The import of other databases works a bit smoother. How that is done can be found in some example notebooks [here](https://docs.brightwaylca.org/notebooks.html#example-notebooks).

# Before we can actually make use of the newly imported database, we need to save it!

# In[ ]:


#write database to disk --> actually saves it
ei35cut.write_database()


# In[ ]:


#list the available databases - again
bw.databases


# <span style="color:red"><ins>**IMPORTANT NOTE**</ins></span>
# 
# >In the following, we will mainly use data from ecoinvent. In case you do not have access to it, do not worry - you can complete almost the whole notebook with the free FORWAST database, too. You would only have to change the database selection in each respective cell from `eidb.<something>` to `fw.<something>` (abbreviations taken from below). Mind that you would also have to undertake manual changes in the Excel spreadsheet for making the respective import work (chapter 2.3). Also, mind that the FORWAST data differs to the one of ecoinvent; this, however, affects only few of your commands further below (e.g. finding activities by name etc.). If you want to work with data from other sources, e.g. Agribalyse, please see the respective [strategies](https://2.docs.brightwaylca.org/notebooks.html#example-notebooks) for their data import.

# <a id='section22'></a>
# ## 2.2 Database selection and a first look at activities
# 
# If our database of choice is already included, then we just make use of it directly. For convenience, we need to assign a variable to it so that the database can be worked with more easily.

# In[ ]:


eidb = bw.Database('ecoinvent 3.5_cutoff_ecoSpold02')
fw = bw.Database('forwast')


# We can also check up on the type and length of our imported database.

# In[ ]:


print("The imported ecoinvent database is of type {} and has a length of {}.".format(type(eidb), len(eidb)))


# And we can even visualise our technospheres:

# In[ ]:


fw.graph_technosphere()


# In[ ]:


eidb.graph_technosphere()


# Nice graphic! But it doesn't really tell us much... Let's have a bit of a closer look at what our database contains. We can, for instance, examine a random process of the imported ecoinvent database by doing the following:

# In[ ]:


random_act = eidb.random()
random_act.as_dict()


# To get an overview of all exchanges of the selected process, type:

# In[ ]:


for exc in random_act.exchanges():
    print(exc)


# And if you want to get more information on one specific exchange of the chosen process, do:

# In[ ]:


#change the numeral to check out the other exchanges (as from the list above)
[exc for exc in random_act.exchanges()][0].as_dict()


# Sometimes it can also be helpful to have some activity characteristics at hand, for instance if you want to search a database using an activity's code or want to get an activity's name when only having its key...

# In[ ]:


#getting an activity's code
random_act['code']


# In[ ]:


#getting an activity's name through its code
eidb.get(random_act['code'])


# In[ ]:


#getting an activity's key
random_act.key


# In[ ]:


#getting an activity's name using its key
bw.get_activity(random_act.key)


# <a id='section23'></a>
# ## 2.3 Importing a dataset from Excel
# 
# In addition to the import of a standard background database and the manual database creation (see below), we can also import data from various file types, one of them being Excel. This works relatively smoothly, provided the Excel workbook is created correctly. In the following, we import a flawless dataset. However, if you are interested in tiny, tricky challenges regarding the Excel import, have a look [here](https://github.com/PoutineAndRosti/Brightway-Seminar-2017/blob/master/Day%201%20PM/Data%20IO.ipynb). The here used Excel file was adapted from this source, so that it works with our imported ecoinvent 3.5  database. Another way for importing an, now unknown, Excel file can be found [here](https://nbviewer.jupyter.org/urls/bitbucket.org/cmutel/brightway2/raw/default/notebooks/IO%20-%20importing%20an%20Excel%20file.ipynb). But here we'll stick to the first approach:

# In[ ]:


imp = bw.ExcelImporter(os.path.join("excel_importer_example.xlsx"))
imp.apply_strategies()
imp.match_database(fields=('name', 'unit', 'location'))
imp.match_database("ecoinvent 3.5_cutoff_ecoSpold02", fields=('name', 'unit', 'location'))
imp.statistics()


# You can check whether the import went as expected by having a look at an Excel sheet, that includes our process data. The location of this file is given as output of the following command:

# In[ ]:


imp.write_excel()


# Seems like everything went fine :)
# 
# If an exchange cannot be linked using the above applied strategies, because the respective input is listed multiple times in the database, you would have to link it manually. An example for such a case is `treatment of aluminium scrap, post-consumer, prepared for recycling, at refiner`, for which two ecoinvent (3.5 cutoff) entries exist.

# Having imported the data, we also need to write it to a database to save it:

# In[ ]:


imp.write_database()


# In[ ]:


bw.databases


# In[ ]:


wbi = bw.Database("BW2 Excel water bottle import")
for act in wbi:
    print(act)


# In[ ]:


wbp = [act for act in wbi][0]
for exc in wbp.exchanges():
    print(exc)


# See whether the details of our biosphere exchange are correct:

# In[ ]:


ex = [act for act in wbi if 'water bottle production' in act['name']][0]
[exc for exc in ex.exchanges() if 'Carbon dioxide' in str(exc)][0].as_dict()


# Final check whether really everything worked - these commands will be explained later in detail:

# In[ ]:


lca = bw.LCA(
    {("BW2 Excel water bottle import", "WriteSomeCode_UUID_isFineButNotNecessary"): 1}, 
    ('IPCC 2013', 'climate change', 'GWP 100a')
)
lca.lci()
lca.lcia()
lca.score


# Ok, enough with that. Let's delete this database (not the Excel file!) and the associated variables now:

# In[ ]:


del databases[wbi.name]
#or:
#wbi.delete()
del wbi, wbp


# Alternatively, we can also deregister the database, which removes all metadata:

# In[ ]:


bw.Database('BW2 Excel water bottle import').deregister()


# In[ ]:


bw.databases


# **Continue, or back to [table of contents](#section0)?**
# ***

# <a id='section3'></a>
# # 3. Manual database creation
# In addition, let's add a new database manually. There are two very similar ways of doing so, shown below. Mind that this database needs to be saved as well so that we can work with it.

# In[ ]:


#One way of manually creating a database:
db1 = bw.Database('3D')
db1.register()
db1.write({('3D', 'Printer'):{
    'name': 'Printer',
    'exchanges': [],
    'unit': 'unit',
    'location': 'somewhere',
    'categories': ('in the', 'universe')
}})



#Another way of manually creating a database is to have the data in a separate dictionary and then write it into an instantiated database:
db2 = Database("example")
example_data = {
    ("example", "A"): {
        "name": "A",
        "exchanges": [{
            "amount": 1.0,
            "input": ("example", "B"),
            "type": "technosphere"
            }],
        'unit': 'kilogram',
        'location': 'here',
        'categories': ("very", "interesting")
        },
    ("example", "B"): {
        "name": "B",
        "exchanges": [],
        'unit': 'microgram',
        'location': 'there',
        'categories': ('quite', 'boring')
        }
    }

db2.write(example_data)


# Let's see if our databases actually exist:

# In[ ]:


bw.databases


# Well, seems like it. Now, let's have a look at a random activity in our second database:

# In[ ]:


db2.random()


# If we want to get some information on the number of exchanges in each activity contained in the database, we type in:

# In[ ]:


num_exchanges = [(activity, len(activity.exchanges())) for activity in db2]
num_exchanges


# We can also look for our activities, in this case all of them, by typing:

# In[ ]:


db1.search("*")


# However, we don't want to use these databases in the following. Therefore, we simply delete them, just like we deleted the dataset imported from an Excel file above:

# In[ ]:


del databases[db1.name]
del databases[db2.name]


# In[ ]:


#make sure that the databases got deleted
bw.databases


# Okay, now that we have our background data (be it manually created or imported from an existing database), it's time to model our foreground system!

# **Continue, or back to [table of contents](#section0)?**
# ***

# <a id='section4'></a>
# # 4. LCIA
# 
# Before continuing with a simple product system example, the basics of the inventory caluclation shall be introduced. First, let's have a look at which LCIA methods we can access:

# In[ ]:


list(bw.methods)

#or use the built-in method
#bw.methods.list

#or the following
#bw.methods.items()


# Ok, we see that there are quite a few methods that we could use for our LCA. Can we get more details on them? Sure we can! Those details are stored as values (`bw.methods.values()`), with the method names being the keys (`bw.methods.keys()`):

# In[ ]:


for key in bw.methods:
    print(key, ':', bw.methods[key])


# To access the description of only one method, type:

# In[ ]:


bw.methods.get(('CML 2001', 'acidification potential', 'average European'))


# As you can see, this is a nested dictionary. You can also access values within the nested one, for example:

# In[ ]:


bw.methods.get(('ILCD 1.0.8 2016 midpoint', 'ecosystem quality', 'marine eutrophication')).get('unit')


# Now, let's select a set of LCIA methods to be applied in an inventory calculation, in this case the IPCC 2013 GWP100a (no LT).

# In[ ]:


CC_method = [m for m in bw.methods if 'IPCC 2013' in str(m) and  'climate change' in str(m) and 'GWP 100a' in str(m) and not 'no LT' in str(m)][0]
CC_method


# Let's define the functional unit/ reference flow; for now, this is only a random one, picked from our ecoinvent database:

# In[ ]:


# select a process to be defined as functional unit
process = eidb.random()
process


# In[ ]:


functional_unit = {process:1}


# Now we can calculate the inventory!

# In[ ]:


lca = LCA(functional_unit,CC_method)

# alternatively, you can enter both functional unit and LCIA method directly into the LCA-command:
# myFirstLCA_quick = bw.LCA({process:1}, ('IPCC 2013', 'climate change', 'GWP 100a'))


# And here we perform the actual impact calculation! Mind that this does not yield an output.

# In[ ]:


lca.lci()
lca.lcia()


# To see the actual impact as mid- or endpoint indicator (according to the impact assessment method used), we type in:

# In[ ]:


lca.score


# This result is given in the unit specified by the impact assessment method.

# You can also check which LCIA method was applied for a given result:

# In[ ]:


lca.method


# To see what else you can do with the lca-object, press tab in the next cell:

# In[ ]:


lca.


# **Change the method**

# Now let's change the impact assessment method and experiment with two other methods, `redo_lci` and `redo_lcia`:

# In[ ]:


agri_land_occ = [m for m in bw.methods if 'ReCiPe Midpoint (H)' in str(m) and  'agricultural land occupation' in str(m) and not 'w/o LT' in str(m) ][0]
lca.switch_method(agri_land_occ)


# We can recalculate our LCI, including a changed demand, i.e. a new functional unit:

# In[ ]:


demand = {process:2}
lca.redo_lci(demand)
lca.score


# The above command, however, has neither adopted the changed impact assessment method, nor has it recalculated the impacts. What's more, we don't see the change of the inventory reflected in our score - simply because it wasn't recalculated. Only the inventory as well as the demand and supply arrays got changed. To recalculate our inventory with our newly chosen impact assessment method (and, if you like, an adjusted demand), we need to type the following:

# In[ ]:


demand2 = {process:3}
lca.redo_lcia(demand2)
lca.score


# **Additional stuff**

# Ok, enough with adjustments and recalculations. Let's check out some matrices now:
# 
# - the technosphere matrix:

# In[ ]:


lca.technosphere_matrix


# In[ ]:


print(lca.technosphere_matrix)


# - the biosphere matrix:

# In[ ]:


lca.biosphere_matrix


# In[ ]:


print(lca.biosphere_matrix)


# - the characterisation matrix:

# In[ ]:


lca.characterization_matrix


# In[ ]:


print(lca.characterization_matrix)


# - the inventory:

# In[ ]:


lca.inventory


# In[ ]:


print(lca.inventory)


# - the characterised inventory:

# In[ ]:


lca.characterized_inventory


# In[ ]:


print(lca.characterized_inventory)


# + and the demand as well as supply arrays:

# In[ ]:


lca.demand_array #contains what we entered as final demand. Check that it only contains this demand by summing up the whole array


# In[ ]:


lca.demand_array.sum()


# In[ ]:


lca.supply_array #equals the multiplication of our inverted transaction matrix by the final demand, i.e. (Ae-1)*y


# **Continue, or back to [table of contents](#section0)?**
# ***

# <a id='section5'></a>
# # 5. Foreground system
# 
# For modeling a foreground system, a new database is created that is linked to ecoinvent via exchanges. Some steps need to be considered, exemplified below for two simple product systems.

# <a id='section51'></a>
# ## 5.1 How to create a simple product system?

# Now we want to create the product system for a fictitious aluminium waste handling process, consisting of inputs from the treatment of aluminium scrap as well as markets for transports and compressed air. For creating a product system, we need to create foreground processes that we link to background processes. For the latter, we can search in the background database. When we don't know the exact name of an activity, we can first search for the parts of the name that we are sure about, e.g. low-voltage electricity:

# **Setup of technosphere**

# In[ ]:


#this search does not yield the complete list as we will see later
eidb.search('electricity, low voltage')


# In[ ]:


#this search, however, does yield the complete list
for act in [act for act in eidb if 'electricity, low voltage' in act['name']]:
    print(act)


# From this list, we can select the target activity through a more narrow description including indexing.

# In[ ]:


process = [act for act in eidb if 'electricity, low voltage' in act['name'] and 'CA-ON' in act['location']][0]
process


# Have a closer look at the description of the target activity.

# In[ ]:


process.as_dict()


# Side note: You can also find the name of an activity by its code:

# In[ ]:


eidb.get('cfd25c57d2a355b94813229866ae9f5d')


# Now, let's create and save a new activity for which we design the product system.

# In[ ]:


waste_handling = eidb.new_activity(code = 'test1', name = "Waste handling", unit = "unit")
waste_handling.save()


# **Include parameters**

# Adding some parameters on the project level works like the following. Mind that there are also parameters on the activity and database level. The commands for handling and saving those are quite similar; for more details, look [here](https://docs.brightwaylca.org/technical/bw2data.html#parameters)

# In[ ]:


project_data = [{
    'name': 'M',
    'amount': 0.06,
}, {
    'name': 'D',
    'amount': 200
}]

parameters.new_project_parameters(project_data)


# In[ ]:


# have a look at existing project parameters
for param in ProjectParameter.select():
    print(param, param.amount)


# Let's make use of the entered parameters by parametrising the input amounts!

# In[ ]:


aluminium = [act for act in eidb if act['name']=='treatment of aluminium scrap, post-consumer, prepared for recycling, at refiner' and 'RER' in act['location']][0]
waste_handling.new_exchange(input=aluminium.key,amount=0,unit="kilogram",type='technosphere', formula='M').save()
waste_handling.save()

transport = [act for act in eidb if act['name']=='market for transport, freight, lorry 3.5-7.5 metric ton, EURO5' and 'RoW' in act['location']][0]
waste_handling.new_exchange(input=transport.key,amount=0,unit="ton kilometer",type='technosphere', formula='D*M/1000').save()
waste_handling.save()

air = [act for act in eidb if act['name']=='market for compressed air, 600 kPa gauge' and 'GLO' in act['location']][0]
waste_handling.new_exchange(input=air.key,amount=0,unit="cubic meter",type='technosphere', formula='D*M/1000').save()
waste_handling.save()


# Before the parameters become valid, we also need to save them by adding them to a group. Then we need to recalculate the exchanges based on the parameters.

# In[ ]:


parameters.add_exchanges_to_group("again another group", waste_handling)
ActivityParameter.recalculate_exchanges("again another group")


# Now we can have a look at the inputs to our waste handling activity. There are two ways:
# 
# - one that quantifies the input:

# In[ ]:


#Have a look at all exchanges of the selected activity
for exc in waste_handling.exchanges():
    print(exc)


# - and one that does not:

# In[ ]:


for act in waste_handling.technosphere():
    print(act.input)


# Moreover, we can check on some details of our new activity:

# In[ ]:


#get general information on the new activity
act = eidb.get('test1')
act


# In[ ]:


#or like that
eidb.search('waste handling')


# **Delete parameters and activities**

# In[ ]:


#delete a set of parameters; does not delete the parameter from the project parameters list?!?
name = ['M']
for name in ProjectParameter.select():
    name.delete()


# In[ ]:


#should delete the parameters but doesn't?!?
ProjectParameter.delete()


# In[ ]:


#remove the respective exchanges from the group; does not yet change anything about the exchanges?!?
parameters.remove_exchanges_from_group("again another group", waste_handling)


# In[ ]:


#should remove parameters, but does not really work
parameters.remove_from_group("again another group", waste_handling)


# In[ ]:


#Delete the list of project data (or any other dictionary); does not affect the parametrised exchanges until they get recalculated
project_data.clear() #.remove would only clear the content but leave empty instances
#quick check to see that it got deleted
for data in project_data:
    print(data)


# In[ ]:


#delete the table of existing project parameters, i.e. actually deletes the project parameters
ProjectParameter.drop_table(safe=True, drop_sequences=True)
#create a new empty table of project parameters
ProjectParameter.create_table()

for name in ProjectParameter.select():
    name.print()


# In[ ]:


#delete all waste handling activities that were accidentally created
for activity in [act for act in eidb if act['name']=='Waste handling' and 'GLO' in act['location']]:
    activity.delete()
#delete individual bottle production activity
#waste_handling.delete


# In[ ]:


#check that the activity actually got deleted
eidb.search('waste handling')


# Seems like it...

# <a id='section52'></a>
# ## 5.2 Bottle production
# Okay, now that we know the basics for creating (and deleting) a simple product system, we will create another one, explore it, and perform an LCA on it. So, here's a first short example on a simplified plastic bottle production. This process only has three inputs: electricity, transport, and polyethylene.

# **Setup of the product system**

# As mentioned earlier, the 'eidb.search' function does not give all the items that actually match the search criteria. We see this by comparing the following command with the one thereafter:

# In[ ]:


#incomplete search results
eidb.search('electricity production, photovoltaic, 3kWp slanted-roof installation,')#, filter={'location': 'CA-ON'})


# In[ ]:


#complete search results
for act in [act for act in eidb if 'electricity production, photovoltaic, 3kWp slanted-roof installation,' in act['name']]:# and 'CA-ON' in act['location']]:
    print(act)


# In[ ]:


#we can also sort our search results
list_to_be_sorted = [act for act in eidb if 'electricity production, photovoltaic, 3kWp slanted-roof installation,' in act['name']] # and 'CA-ON' in act['location']]:
newlist = sorted(list_to_be_sorted, key=lambda k: k['name'])

#for multiple keys, its works like this:
#newlist = sorted(list_to_be_sorted, key = itemgetter('name','categories'))
#or
#newlist = sorted(list_to_be_sorted, key=lambda k: (k['name'],k['categories']))

newlist


# In[ ]:


#now let's refine the search and pick one activity
[act for act in eidb if 'electricity production, photovoltaic, 3kWp slanted-roof installation,' in act['name'] and 'CA-ON' in act['location']][0]


# mind:
#     Activities do not have very many required fields; aside from database and code, the only other required field is name, but most activities will have a location and unit as well. If no type is specified for an activity, then the activity is assumed to be a process. Other types include product and biosphere for biosphere flows. Activity type is used to determine whether an activity should be placed in the biosphere or technosphere matrices during LCA calculations.
# 
# 
# Let's now create our [parameterised product system](https://docs.brightwaylca.org/intro.html#parameterized-datasets):

# In[ ]:


#The following for-loop is only to guarantee that we can create a new bottle production process
for activity in [act for act in eidb if 'Bottle production' in act['name'] and 'GLO' in act['location']]:
    activity.delete()

# activities and exchanges for simple bottle production model
bottle_production = eidb.new_activity(code = 'test1', name = "Bottle production", unit = "unit")
#bottle_production.save()

project_data = [{
    'name': 'M',
    'amount': 0.06,
}, {
    'name': 'D',
    'amount': 200
}]

parameters.new_project_parameters(project_data)

for param in ProjectParameter.select():
    print(param, param.amount)

electricity = [act for act in eidb if act['name']=='electricity production, photovoltaic, 3kWp slanted-roof installation, multi-Si, panel, mounted, label-certified' and 'CH' in act['location']][0]
bottle_production.new_exchange(input=electricity.key,amount=0,unit="kilowatt hour",type='technosphere', formula='20*M/3.6').save()
bottle_production.save()

#mind how the following activity is treated differently! The reason for this will be shown later
polyethylene = [act for act in eidb if act['name']=='market for polyethylene, high density, granulate' and 'GLO' in act['location']][0]
pe = bottle_production.new_exchange(input=polyethylene.key,amount=0,unit="kilogram",type='technosphere', formula='M')
pe.save()
bottle_production.save()

transport = [act for act in eidb if act['name']=='market for transport, freight, lorry 3.5-7.5 metric ton, EURO5' and 'RER' in act['location']][0]
bottle_production.new_exchange(input=transport.key,amount=0,unit="ton kilometer",type='technosphere', formula='D*M/1000').save()
bottle_production.save()

parameters.add_exchanges_to_group("again another group", bottle_production)
ActivityParameter.recalculate_exchanges("again another group")


# **Cross-check the exchanges**

# Let's check whether everything went ok when creating our exchanges:

# In[ ]:


for exc in bottle_production.exchanges():
    print(exc)


# In[ ]:


bottle_production.as_dict()


# In[ ]:


#also this works:
for key in bottle_production:
    print(key, ':', bottle_production[key])


# Ok, seems like everything is fine with the bottle production activity. But what about the inputs - can we check how they are actually linked? Sure! To see the **inputs** of, for instance, our polyethylene input, we type:

# In[ ]:


for exc in polyethylene.exchanges():
    print(exc)


# And to see the **outputs** of this activity, i.e. the upstream exchanges across the whole database, we type:

# In[ ]:


for exc in polyethylene.upstream():
    print(exc)


# ... and yes, here it is. We can find our newly created exchange at the very bottom of the window!

# Alternatively, we can also look straight for the **output of a new exchange** (and some other methods of the exchange). For doing so, it is important to have given a name to the exchange that you now want to examine further (as done when creating the product system).

# In[ ]:


pe.input, pe.output, pe.amount, pe.unit, pe.uncertainty_type


# Mind that the **amount equals to zero** here. This might possibly be due to the fact that this amount is parametrised but was set to zero initially (or because of the parameter level, i.e. project in this case).

# **Troubleshooting**
# 
# In case something went wrong during the setup of the product system, make sure to remove all parameters and the saved activities (as shown below) and rerun the window for creating the product system.

# In[ ]:


#Delete the list of project data (or any other dictionary); does not affect the parametrised exchanges until they get recalculated
project_data.clear() #.remove would only clear the content but leave empty instances
#quick check to see that it got deleted
for data in project_data:
    print(data)


# In[ ]:


#delete the table of existing project parameters, i.e. actually deletes the project parameters
ProjectParameter.drop_table(safe=True, drop_sequences=True)
#create a new empty table of project parameters
ProjectParameter.create_table()

for name in ProjectParameter.select():
    name.print()


# In[ ]:


#delete all bottle production activities that were accidentally created
for activity in [act for act in eidb if act['name']=='Bottle production' and 'GLO' in act['location']]:
    activity.delete()
#delete individual bottle production activity
#waste_handling.delete


# Now let's see whether really everthing got deleted:

# In[ ]:


for exc in bottle_production.exchanges():
    print(exc)


# **Definition of LCIA methods and functional unit**

# In[ ]:


method_key = [m for m in bw.methods if 'ReCiPe' in str(m) and  'Midpoint (H)' in str(m) and 'climate change' in str(m)][0]

functional_unit = {bottle_production:1}


# **LCA calculation**

# In[ ]:


lca = bw.LCA(functional_unit,method_key)


# In[ ]:


lca.lci()
lca.lcia()


# In[ ]:


lca.demand


# In[ ]:


lca.method


# In[ ]:


lca.score


# **Elementary and product flows**
# 
# There are a few ways to examine the elementary flows of our product system which are explained below. The same goes for product flows.

# In[ ]:


eidb.filepath_processed()


# In[ ]:


your_structured_array = np.load(eidb.filepath_processed())
pd.DataFrame(your_structured_array).head()


# In[ ]:


pd.Series(bw.mapping).head()


# In[ ]:


pd.DataFrame(lca.bio_params).head(6) 


# In[ ]:


lca.activity_dict


# In[ ]:


# Getting the key from the "demand" attribute:
act_key = list(lca.demand)[0].key
# Getting the column number from the activity_dict:
col_index = lca.activity_dict[act_key]
print("The column index for activity {} is {}".format(act_key, col_index))


# In[ ]:


#have the numbering, i.e. the value, in the beginning
myFirstLCA_rev_activity_dict = {value:key for key, value in lca.activity_dict.items()}
myFirstLCA_rev_activity_dict


# In[ ]:


lca_rev_act_dict, lca_rev_product_dict, lca_rev_bio_dict = lca.reverse_dict()


# As done earlier for another product system, let's check out the technosphere:

# In[ ]:


lca.technosphere_matrix


# In[ ]:


print(lca.technosphere_matrix)


# In[ ]:


from bw2analyzer.matrix_grapher import SparseMatrixGrapher


# In[ ]:


SparseMatrixGrapher(lca.biosphere_matrix).graph()


# In[ ]:


lca.technosphere_matrix


# In[ ]:


SparseMatrixGrapher(lca.technosphere_matrix).ordered_graph()


# If you're now wondering that this looks very similar to the result of the command `eidb.graph_technosphere()`, then you're right. The only difference is that our foreground system is now included.

# Before being able to get deeper insights, we need to prepare a few variables, all based on the column index, which we get like that:

# In[ ]:


print("As a reminder, the column index for  {} is  {}".format(act_key, col_index))


# The column is given in *compressed sparse row* format. We can see that by doing as follows:

# In[ ]:


myColumn = lca.technosphere_matrix[:, col_index]
myColumn


# In[ ]:


print(myColumn)


# Now let's switch from the *compressed sparse row* format to the *coordinate* format. With that we can examine our columns a bit further :) And, interestingly, the print-outs of our columns look exactly the same.

# In[ ]:


myColumnCOO = myColumn.tocoo()
myColumnCOO


# The output is unchanged for that:

# In[ ]:


print(myColumnCOO)


# In[ ]:


myColumnCOO.row


# Let's have a look again at the identifiers of our foreground activities:

# In[ ]:


[lca_rev_product_dict[i] for i in myColumnCOO.row]


# Through these identifiers we can also get the names of our activities:

# In[ ]:


names_of_my_inputs = [bw.get_activity(lca_rev_product_dict[i])['name'] for i in myColumnCOO.row]
names_of_my_inputs


# And those names can of course be linked to the actual amounts (which then looks much nicer in a table than above, only with the keys).

# In[ ]:


# First create a dict with the information I want:
myColumnAsDict = dict(zip(names_of_my_inputs,myColumnCOO.data))
# Create Pandas Series from dict
pd.Series(myColumnAsDict, name="A series with information on exchanges in my foreground process")


# An alternative way to generate such a table is as follows, not depending on all the column-preparation...

# In[ ]:


pd.Series({bw.get_activity(exc.input)['name']:exc.amount for exc in bottle_production.technosphere()}, 
          name="alternative way to generate exchanges")


# Which, to be honest, does not give more information than the command we already used a couple of times (the data is simply presented in a different way):

# In[ ]:


for exc in bottle_production.exchanges():
    print(exc)


# **Continue, or back to [table of contents](#section0)?**
# ***

# <a id='section6'></a>
# # 6. Manipulating an exchange

# In the following, we want to manipulate the electricity exchange. This we want to do by not only changing the amount, but by manipulating the underlying formula.

# <a id='section61'></a>
# ## 6.1 Copying and deleting activities
# 
# First, let's copy our bottle production product system!

# In[ ]:


bottle_production_copy = bottle_production.copy()


# To see whether it really got copied, let's have a look at the exchanges:

# In[ ]:


for exc in bottle_production_copy.exchanges():
    print(exc)


# In[ ]:


bottle_production_copy.save()


# Ok, seems like it worked.

# You can delete the entire technosphere of an activity like this:

# In[ ]:


bottle_production_copy.technosphere().delete()


# If you even want to delete the activity itself, you can do it this way:

# In[ ]:


bottle_production_copy.delete()


# Check whether the activity is still in the database:

# In[ ]:


bottle_production_copy in eidb


# But now let's get our copy back and start working with it:

# In[ ]:


bottle_production_copy = bottle_production.copy()
bottle_production_copy.save()


# In[ ]:


bottle_production_copy.as_dict()


# <a id='section62'></a>
# ## 6.2 First attempts at manipulating an exchange's keys/values
# 
# First a short reminder what an exchange of our activity looks like. Let's for example take the first exchange, which is electricity. There are different ways of getting (almost) the same information:

# In[ ]:


[exc for exc in bottle_production_copy.exchanges()][0]


# In[ ]:


print([exc for exc in bottle_production_copy.exchanges()][0].items)


# In[ ]:


[exc for exc in bottle_production_copy.exchanges()][0].as_dict()


# And quite obviously the output of this exchange is our bottle production...

# In[ ]:


[exc for exc in bottle_production_copy.exchanges()][0].output


# Let's have a look at the formula of our exchange of interest - there's again two ways of doing so:

# In[ ]:


[exc for exc in bottle_production_copy.exchanges()][0]['formula']


# In[ ]:


print([exc for exc in bottle_production_copy.exchanges()][0].get('formula'))


# Let's see if we can manipulate this formula or the exchange in general:

# In[ ]:


#add another key with value
[exc for exc in bottle_production_copy.exchanges()][0]['key']='value'


# In[ ]:


del [exc for exc in bottle_production_copy.exchanges()][0]['key']


# In[ ]:


#change the formula and by that the amount of our exchange
#[exc for exc in bottle_production_copy.exchanges()][0].update({'formula': '40*M/3.6'})
list(exc for exc in bottle_production_copy.exchanges())[0].update({'formula': '40*M/3.6'})
[exc for exc in bottle_production_copy.exchanges()][0].save()
bottle_production_copy.save()


# In[ ]:


[exc for exc in bottle_production_copy.exchanges()][0]


# In[ ]:


list(exc for exc in bottle_production_copy.exchanges())[0]


# In[ ]:


example = [exc for exc in bottle_production_copy.exchanges()][0]
print(example.update({'formula': '40*M/3.6'}))
example


# In[ ]:


example.update? #no the update command is used differently.


# In[ ]:


bottle_production_copy.substitution? #no, the substitution command is used for something else.


# In[ ]:


[exc for exc in bottle_production_copy.exchanges()][0].update


# In[ ]:


#change the formula and by that the amount of our exchange
[exc for exc in bottle_production_copy.exchanges()][0]['formula']='40*M/3.6'


# In[ ]:


#see if the formula in the respective exchange changed
[exc for exc in bottle_production_copy.exchanges()][0].as_dict()


# Ok, so we see that nothing of this really works. Maybe we'll still find a solution for doing so. Actually we are super close, jsut a tiny part needs to be changed. But for now, let's try to substitute an exchange first.

# <a id='section63'></a>
# ## 6.3 Substituting an exchange
# 
# So, let's first delete our activity and then recreate it:

# In[ ]:


#delete individual bottle production activity
bottle_production_copy.delete()


# In[ ]:


#delete all bottle production activities that were accidentally created
for activity in [act for act in eidb if act['name']=='Bottle production copy' and 'GLO' in act['location']]:
    activity.delete()


# In[ ]:


bottle_production_copy = bottle_production.copy(code='test2', name="Bottle production copy")
bottle_production_copy.save()


# Check whether the copy was actually created and saved:

# In[ ]:


eidb.search('Bottle production')#, filter={'code': 'test2'})


# Let's have a look at the exchanges of our production system:

# In[ ]:


[exc for exc in bottle_production_copy.exchanges()]


# Once again, let's see the details of our exchange of interest, i.e. electricity:

# In[ ]:


[exc for exc in bottle_production_copy.exchanges()][0].as_dict()


# Reminder: We can also see all upstream exchanges of our activity of interest, i.e. electricity production:

# In[ ]:


[exc for exc in electricity.upstream()]

#same as:
#for exc in electricity.upstream():
#    print(exc)


# Now let's delete an exchange either from the upstream or the downstream perspective:

# In[ ]:


#downstream
[exc for exc in bottle_production_copy.exchanges()][0].delete()


# In[ ]:


#upstream
[exc for exc in electricity.upstream()][2].delete()


# Now we add a new exchange as replacement for our deleted one. This action has to be validated by adding the exchange to the group so that the amount (calculated through a formula) is correct.

# In[ ]:


#this is our replacement for the original electricity input
el_subst = [act for act in eidb if act['name']=='electricity production, photovoltaic, 3kWp slanted-roof installation, multi-Si, panel, mounted, label-certified' and 'CH' in act['location']][0]


# In[ ]:


bottle_production_copy.new_exchange(input=el_subst.key,amount=0,unit="kilowatt hour",type='technosphere', formula='40*M/3.6').save()
bottle_production_copy.save()

parameters.add_exchanges_to_group("again another group", bottle_production_copy)
ActivityParameter.recalculate_exchanges("again another group")


# Let's check our exchanges and whether we got what we wanted!

# In[ ]:


[exc for exc in bottle_production_copy.exchanges()]


# Yesss!!! Now, a more in-detail look at our exchange of interest (especially regarding the formula and the amount):

# In[ ]:


[exc for exc in bottle_production_copy.exchanges()][2].as_dict()


# <a id='section64'></a>
# ## 6.4 Successfully manipulating an exchange

# Now let's finally manipulate a key,value pair of an exchange. There are two ways for doing so, depending on whether you want to assign a name to your exchange. **Alternative A** is the long version, **alternative B** the short one.

# + **Alternative A**
# 
# Here, we want to first add another exchange to our production system, assign a variable to it, and then change its amount through an adjustment of its formula.

# In[ ]:


#add another electricity source to our bottle production system
el_extra = [act for act in eidb if act['name']=='electricity production, photovoltaic, 3kWp slanted-roof installation, single-Si, panel, mounted, label-certified' and 'CH' in act['location']][0]

el_ext = bottle_production_copy.new_exchange(input=el_extra.key,amount=0,unit="kilowatt hour",type='technosphere', formula='10*M/3.6')
el_ext.save()
bottle_production.save()

parameters.add_exchanges_to_group("again another group", bottle_production_copy)
ActivityParameter.recalculate_exchanges("again another group")


# In[ ]:


#check our exchanges
[exc for exc in bottle_production_copy.exchanges()]


# In[ ]:


#have a look at the created exchange
el_ext.as_dict()


# In[ ]:


#let's change the amount of this exchange through an adjustment of the formula

#btw: for getting a subset of the exchange-dictionary, you can type (to get the formula):
#wanted_key = ['formula']
#formula = dict((k, el_ext[k]) for k in wanted_key if k in el_ext)

el_ext['formula']='20*M/3.6'

el_ext.save()
bottle_production.save()

parameters.add_exchanges_to_group("again another group", bottle_production_copy)
ActivityParameter.recalculate_exchanges("again another group")


# In[ ]:


#check whether it worked and got adopted in the product system
[exc for exc in bottle_production_copy.exchanges()]


# Great! It worked.

# + **Alternative B**
# 
# A quicker way for changing the formula of an exchange is to do the following. This also allows to manipulate exchanges that have no name (as compared to `el_ext` in the above example); you just need to give an intermediate name to the respective exchange.

# In[ ]:


el_exc=[exc for exc in bottle_production_copy.exchanges()][3]
el_exc['formula']='30*M/3.6'
el_exc

el_exc.save()
bottle_production.save()

parameters.add_exchanges_to_group("again another group", bottle_production_copy)
ActivityParameter.recalculate_exchanges("again another group")


# In[ ]:


#let's see whether our change got adopted in the exchange-dictionary
[exc for exc in bottle_production_copy.exchanges()][3].as_dict()


# In[ ]:


#check whether it is also included in the product system
[exc for exc in bottle_production_copy.exchanges()]


# Yeah, awesome! Now we know how to do that.

# **Troubleshooting**
# 
# If anything went wrong when copying or manipulating an activity, you can do the following things and restart - but if there's no error message anywhere, don't execute these following commands, because we will use our bottle production systems later again:

# * Only delete a selected exchange (via two ways) - be sure to index correctly, otherwise you may have to reinstantiate your database:

# In[ ]:


[exc for exc in bottle_production_copy.exchanges()][0].delete()


# In[ ]:


[exc for exc in electricity.upstream()][2].delete()


# - Delete all exchanges that you copied accidentally:

# In[ ]:


for act in [act for act in eidb if 'Bottle production copy' in act['name'] and 'GLO' in act['location']]:
    act.delete()


# **Continue, or back to [table of contents](#section0)?**
# ***

# <a id='section7'></a>
# # 7. Basic contribution analysis
# 
# Based on the bottle production product system: Let's have a bit of a closer look at the inventory and the contributions of individual exchanges/activities!

# But before that, we recalculate our inventory:

# <a id='section71'></a>
# ## 7.1 Recalculation of the inventory

# In[ ]:


#these are our method and functional unit, same as above in section 5.
method_key = [m for m in bw.methods if 'ReCiPe' in str(m) and  'Midpoint (H)' in str(m) and 'climate change' in str(m)][0]

functional_unit = {bottle_production:1}


# In[ ]:


lca = bw.LCA(functional_unit, method_key)


# In[ ]:


lca.lci()
lca.lcia()


# In[ ]:


lca.demand


# In[ ]:


lca.method


# In[ ]:


print("The {} process accounts for {:f} {}.".format(
    list(functional_unit.keys())[0]['name'],
    lca.score,
    bw.methods.get(method_key).get('unit')
    ))


# And now over to the contribution analysis. Let's find the most damaging activities and biosphere flows.

# <a id='section72'></a>
# ## 7.2 Basic contribution analysis

# In[ ]:


import bw2analyzer as bwa


# In[ ]:


ca = bwa.ContributionAnalysis()
ca.annotated_top_processes(lca, limit=5) #returns a list of tuples: (lca score, supply amount, activity name)


# We can also set a limit below one, which will filter by fraction of impact instead of number of activities; we can also return activity keys instead of names.

# In[ ]:


#change "False" to "True" and this command will give a similar result as the following one, only that we set a limit here
ca.annotated_top_processes(lca, names=False, limit=0.001, limit_type='percent')


# Another way of listing the most contributing activities is this:

# In[ ]:


lca.top_activities() #this command essentially relies on the annotated_top_process command from above. Hence, the output is given as (lca score, supply amount, activity name)


# And of course we can do the same for elementary flows:

# In[ ]:


ca.annotated_top_emissions(lca, limit=0.02, limit_type='percent')


# In[ ]:


#or like that
lca.top_emissions()


# Notice that you can use the bw2analyzer.ContributionAnalysis method for analysing your results further, for instance through a Hinton matrix - see for yourself:

# In[ ]:


ca.hinton_matrix(lca, rows=10, cols=10)


# <a id='section73'></a>
# ## 7.3 Top emissions and processes by name

# In addition to the basic contribution analysis, we can also look at individual activities (columns) or flows (rows).
# 
# What if we want to group names together, i.e. to get the total impact for all "phosphates"? There isn't a built-in function for this, but it is relatively easy to do. Let's start with creating different lists:

# In[ ]:


from collections import defaultdict

#get the keys for each biosphere flow of the same name
all_unique_names_and_their_keys = defaultdict(list)

for flow in bw.Database("biosphere3"):
    if flow.key in lca.biosphere_dict:
        all_unique_names_and_their_keys[flow['name']].append(flow.key)
    
all_unique_names_and_their_keys


# In[ ]:


#get the rows for all biosphere flows of the same name
all_unique_names_and_their_rows = {
    name: [lca.biosphere_dict[key] for key in keys] 
    for name, keys in all_unique_names_and_their_keys.items()
}

all_unique_names_and_their_rows


# In[ ]:


#get the scores for all biosphere flows of the same name
all_unique_names_and_their_scores = {
    name: [lca.characterized_inventory[row, :].sum() for row in rows]
    for name, rows in all_unique_names_and_their_rows.items()
}

all_unique_names_and_their_scores


# Now, let's sort this list by the score and only display the first 10 results.

# In[ ]:


#get the first 10 scores of the most contributing biosphere flows
sorted_scores = sorted(
    [(sum(scores), name) for name, scores in all_unique_names_and_their_scores.items()], 
    reverse=True
)

sorted_scores[:10]


# We can also encapsulate all this functionality in a single function.

# In[ ]:


from collections import defaultdict

def top_emissions_by_name(lca, biosphere_database='biosphere3'):
    names = defaultdict(list)

    for flow in bw.Database("biosphere3"):
        if flow.key in lca.biosphere_dict:
            names[flow['name']].append(
                lca.characterized_inventory[lca.biosphere_dict[flow.key], :].sum()
            )
    
    return sorted(
        [(sum(scores), name) for name, scores in names.items()], 
        reverse=True
    )


# In[ ]:


top_emissions_by_name(lca)[:5]


# We can see that this function also groups emissions according to their type, e.g. all fossil carbon dioxide emissions are summed to "Carbon dioxide, fossil", as compared to the command in the top `ca.annotated_top_emissions`.

# Possibly we can do the same for the technosphere flows with only slight adaptations to the above function:

# In[ ]:


from collections import defaultdict

def top_processes_by_name(lca, technosphere_database='ecoinvent 3.5_cutoff_ecoSpold02'):
    names = defaultdict(list)

    for flow in eidb:
        if flow.key in lca.activity_dict:
            names[flow['name']].append(
                lca.characterized_inventory[:, lca.activity_dict[flow.key]].sum()
            )
    
    return sorted(
        [(sum(scores), name) for name, scores in names.items()], 
        reverse=True
    )


# In[ ]:


top_processes_by_name(lca)[:5]


# Let's check whether both the top_processes_by_name and the top_emissions_by_name equal our lca.score:

# In[ ]:


l = [t[0] for t in top_processes_by_name(lca)]
sum(l)


# In[ ]:


l = [t[0] for t in top_emissions_by_name(lca)]
sum(l)


# In[ ]:


lca.score


# Well, I guess we can say that is close enough, as these tiny deviations may be due to some rounding errors.

# **Continue, or back to [table of contents](#section0)?**
# ***

# <a id='section8'></a>
# # 8. Multi-LCA
# 
# To speed up comparative LCA, i.e. to compare multiple product alternatives (possibly across multiple impact categories), we can use the M-LCA functionality.

# <a id='section81'></a>
# ## 8.1 Manually comparing products

# The original code for such a comparative static LCA can be found [here](https://nbviewer.jupyter.org/github/PascalLesage/Shared-BW2-notebooks/blob/master/Comparative%20static%20LCA%20in%20Brightway2.ipynb). Here, we want to look at **bananas instead of dairy**. So let's see which activities we have in ecoinvent:

# In[ ]:


bananas_unsorted = [act for act in eidb if 'banana' in act['name']]
bananas = sorted(bananas_unsorted, key=lambda k: k['name'])
bananas


# Of these activities, we now select the banana production processes for Colombia, Costa Rica, and India, and we select three impact methods on climate change, land use, and water stress.

# In[ ]:


banana_CO = [act for act in eidb if 'banana' in act['name'] and 'CO' in act['location']][0]
banana_CR = [act for act in eidb if 'banana' in act['name'] and 'CR' in act['location']][0]
banana_IN = [act for act in eidb if 'banana' in act['name'] and 'IN' in act['location']][0]

inventory = [banana_CO, banana_CR, banana_IN]

methods = [[m for m in bw.methods if 'ReCiPe Midpoint (H)' in str(m) and 'climate change' in str(m)][0],
           [m for m in bw.methods if 'ReCiPe Midpoint (H)' in str(m) and  'agricultural land occupation' in str(m) and not 'w/o LT' in str(m) ][0],
           [m for m in bw.methods if 'ReCiPe Midpoint (H)' in str(m) and  'water depletion' in str(m) and not 'w/o LT' in str(m) and not 'V1.13' in str(m)][0]]

print("Let's compare\n{},\n{}, and\n{}".format(banana_CO, banana_CR, banana_IN))


# In[ ]:


results = []

for banana in inventory:
    lca = bw.LCA({banana:1})
    lca.lci()
    for method in methods:
        lca.switch_method(method)
        lca.lcia()
        results.append((banana["name"], banana["location"], method[1].title(), lca.score, bw.methods.get(method).get('unit')))
results


# We should probably present these results in a nicer form. Let's use `pandas` for that:

# In[ ]:


results_df = pd.DataFrame(results, columns=["Name", "Location", "Method", "Score", "Unit"])
results_df = pd.pivot_table(results_df, index = ["Name", "Location"], columns = ["Method", "Unit"], values = "Score")
results_df


# In[ ]:


df = pd.DataFrame.from_dict(results).T
df


# We can also normalise these results, which may help to get a better overview:

# In[ ]:


NormResults_df = results_df / results_df.max()
NormResults_df


# Sidenote: We can certainly run this kind of comparative LCA with our own product systems, e.g. the bottle production from above. We would just have to select the respective reference flow...

# <a id='section82'></a>
# ## 8.2 Calculation setups

# A faster way of running comparative LCAs is through calculation setups. So, let's get familiar with them! This can be done best by just employing random activities as funcitonal units and selecting the LCIA methods which can be applied to the present biosphere flows (only a subset of these ones). Due to computation time, we decide to use the FORWAST database instead of ecoinvent - although this certainly works, too.

# In[ ]:


# define the functional units and LCIA methods; taken from example notebook
functional_units = [{fw.random(): 1} for _ in range(20)]

import random

all_forwast_flows = {exc.input for ds in fw for exc in ds.biosphere()}
suitable_methods = [method 
                    for method in bw.methods 
                    if {cf[0] for cf in Method(method).load()}.intersection(all_forwast_flows)]

print("Can use {} of {} LCIA methods".format(len(suitable_methods), len(bw.methods)))
chosen_methods = random.sample(suitable_methods, 8)


# In[ ]:


functional_units


# In[ ]:


chosen_methods


# Now we come to the actual calculation setup which gets defined through our functional units and the chosen LCIA methods:

# In[ ]:


my_calculation_setup = {'inv': functional_units, 'ia': chosen_methods}


# In[ ]:


calculation_setups['set of calculation setups'] = my_calculation_setup


# In[ ]:


mlca = MultiLCA('set of calculation setups')
mlca.results


# Hm, does not seem to be so difficult. Therefore, let's try it on a better chosen example.

# <a id='section83'></a>
# ## 8.3 MLCA

# Let's decide on our LCIA method selection:

# In[ ]:


[m for m in bw.methods if 'ReCiPe' in str(m) and  'Midpoint (H)' in str(m) and 'land' in str(m)][:3]


# Now a different way fo setting up our list of selected LCIA methods:

# In[ ]:


land_methods = [m for m in bw.methods if 'ReCiPe' in str(m) and  'Midpoint (H)' in str(m) and 'land' in str(m)][:3]
methods = land_methods + [[m for m in bw.methods if 'ReCiPe' in str(m) and  'Midpoint (H)' in str(m) and 'climate change' in str(m)][0],
          [m for m in bw.methods if 'ReCiPe' in str(m) and  'Midpoint (H)' in str(m) and 'water depletion' in str(m)][0]]
print(methods)


# And now we calculate the results for one functional unit (our banana production from above) and multiple LCIA methods:

# **One functional unit, multiple impact categories**

# In[ ]:


all_scores = {}
banana_lca = bw.LCA({banana_CO:1}, methods[0])
banana_lca.lci()
banana_lca.lcia()
for category in methods:
    banana_lca.switch_method(category)
    banana_lca.lcia()
    all_scores[category] = {}
    all_scores[category]['score'] = banana_lca.score
    all_scores[category]['unit'] = bw.Method(category).metadata['unit']
    print("The score is {:f} {} for impact category {}".format(banana_lca.score, 
                                                 bw.Method(category).metadata['unit'],
                                                 bw.Method(category).name)
    )


# We can certainly present these results also in a nice table:

# In[ ]:


df = pd.DataFrame.from_dict(all_scores).T
df


# And now let's visualise the results only for the scores that have the same unit, i.e. in this example agricultural and urban land occupation.

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# In[ ]:


df_m2 = df[df['unit']=='square meter-year']
df_m2


# In[ ]:


df_m2.plot(kind='barh')


# And of course we can find the relative contributions for our selected functional unit, too:

# In[ ]:


banana_lca_unitProcessContribution = banana_lca.characterized_inventory.sum(axis=0).A1
banana_lca_unitProcessRelativeContribution = banana_lca_unitProcessContribution/banana_lca.score
banana_lca_unitProcessRelativeContribution


# And now we calculate the results for multiple functional units and multiple LCIA methods:

# **Multiple functional units, multiple impact categories**

# In[ ]:


#Set up the production system
prod_sys = [{banana_CO.key:1}, {banana_CR.key:1}, {banana_IN.key:1}]
prod_sys


# In[ ]:


bw.calculation_setups['multiLCA'] = {'inv': prod_sys, 'ia': methods}
bw.calculation_setups['multiLCA']
myMultiLCA = bw.MultiLCA('multiLCA')
myMultiLCA.results

df_impact = pd.DataFrame(data = myMultiLCA.results, columns = methods)
df_impact


# Just in case we cannot remember for some reason our functional units, we can easily find their definition again:

# In[ ]:


myMultiLCA.func_units


# The same certainly goes for our chosen LCIA methods:

# In[ ]:


myMultiLCA.methods


# **Continue, or back to [table of contents](#section0)?**
# ***

# <a id='section9'></a>
# # 9. Monte Carlo simulation
# 
# According to British statistician George Cox "all models are wrong but some are useful" - in that light, quantifying uncertainty makes LCA results more reliable/robust. One of the easiest/ most common ways to do so is to perform a [Monte Carlo simulation](https://en.wikipedia.org/wiki/Monte_Carlo_method), a random sampling technique. Before elaborating on that, we need to understand how uncertainty information is stored in Brightway:

# ### Uncertainty information in Brightway

# Uncertainty is stored at the level of the exchanges - remember this! So, let's have a look at a random ecoinvent exchange:

# In[ ]:


[exc for exc in eidb.random().exchanges()][0].as_dict()


# The *necessary* uncertainty information of an exchange is described in the following fields:  
#   - **'uncertainty type'** : type of probability distribution function that the exchange follows. For example, the uncertainty type = 2 indicates a `lognormal`  distribution.  
#   - **'loc', 'scale', 'shape', 'minimum', 'maximum'**: parameters of the distribution function, which are respectively the location (mean $\mu$, mode, offset, or median), scale (e.g. standard deviation $\sigma$), and shape as well as minimum and maximum of the underlying distribution. Mind that different distribution functions require different parameters - not all parameters have to be defined for each distribution.
# 
# Some *additional* uncertainty related information ('scale without pedigree', 'pedigree') are also there, but are not directly used in the calculation of the uncertainty. They are also specific to ecoinvent.
# 
# Uncertainty in Brightway is dealt with using a Python package called `stats_arrays` (see [here](http://stats-arrays.readthedocs.io/en/latest/)), developed by Chris Mutel in the context of the development of Brightway but applicable to any stochastic model in Python. Have a look at it to see which probability distribution functions are available. And then, let's import this package!

# In[ ]:


import stats_arrays


# Just to give a brief example of how the uncertainty information "works", let's have a look at the lognormal distribution. As a reminder:   
#   - a random variable $X$ is a lognormal if its natural logarithm $ln(X)$ is normally distributed  
#   - the natural logarithm of the *median* of the lognormal distribution is equal to the median (=mean) of the underlying distribution  
# 
# Taking the deterministic amount `amount` to be the median, we should have `loc` = `ln('amount')`. Let's do this for the first exchange of a random ecoinvent activity that has a lognormal distribution:

# In[ ]:


#run this cell again if the output is empty
e = [exc for exc in eidb.random().exchanges() if exc['uncertainty type'] == 2][0]
e.as_dict()


# In[ ]:


e['loc'] == np.log(e['amount'])


# ### Basic Monte Carlo simulation

# **One functional unit, one impact category**

# In[ ]:


#MC simulation with 10 iterations for our banana production and the IPCC GWP100a method
mc = bw.MonteCarloLCA({banana_CO:1},  ('IPCC 2013', 'climate change', 'GWP 100a'))
scores = [next(mc) for _ in range(10)]
scores

#or this way:
#for _ in range(10):
#    print(next(mc))


# Let's print the results of our MC:

# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


plt.hist(scores,bins=40)


# Well, this doesn't really look like anything yet. We should increase the number of iterations - which yields more robust results. Around 10,000 iterations is a good starting point. However, this takes a while, so we will just give it a try with 1000 now. See for yourself how long it would take for a higher number of iterations.

# In[ ]:


#define the number of iterations
n_runs = 1000


# In[ ]:


get_ipython().run_cell_magic('time', '', 'values = [next(mc) for _ in range(n_runs)]')


# In[ ]:


plt.hist(values, bins=40)


# We can also **run the MCs in parallel** which speeds up the computation time - see the following and compare the calculation times!

# In[ ]:


# We can also create parallel Monte Carlo that will run simultations on multiple workers simultaneoulsy
get_ipython().run_line_magic('pinfo', 'bw.ParallelMonteCarlo')


# In[ ]:


pmc = bw.ParallelMonteCarlo(mc.demand, mc.method, iterations=n_runs)


# In[ ]:


get_ipython().run_cell_magic('time', '', 'values = pmc.calculate()')


# In[ ]:


plt.hist(values, bins=40)


# **One functional unit, multiple impact categories**

# In[ ]:


# define the function for MC simulation
def multiImpactMonteCarloLCA(functional_unit, list_methods, iterations):
    # Step 1
    MC_lca = bw.MonteCarloLCA(functional_unit)
    MC_lca.lci()
    # Step 2
    C_matrices = {}
    # Step 3
    for method in list_methods:
        MC_lca.switch_method(method)
        C_matrices[method] = MC_lca.characterization_matrix
    # Step 4
    results = np.empty((len(list_methods), iterations))
    # Step 5
    for iteration in range(iterations):
        next(MC_lca)
        for method_index, method in enumerate(list_methods):
            results[method_index, iteration] = (C_matrices[method]*MC_lca.inventory).sum()
    return results

# define the LCIA methods, functional unit, and the number of iterations
ILCD = [method for method in bw.methods if "ILCD" in str(method) and "no LT" not in str(method)]
fu = {banana_CO:1}
iterations = 100

# let it run!
test_results = multiImpactMonteCarloLCA(fu, ILCD, iterations)
test_results


# In[ ]:


ILCD


# In[ ]:


#we can get the plots for all 34 ILCD methods (--> type: len(ILCD)) by changing the index in the brackets
plt.hist(test_results[33], bins=40)


# If you are interested in applying a **sensitivity analysis**, check out this [notebook](https://github.com/PoutineAndRosti/Brightway-Seminar-2017/blob/master/Day%202%20PM/Sensitivity%20analysis%20-%20example%20with%20PAWN%20indices.ipynb).

# ---
# 
# At this point, it's worth pointing again at the **[Activity browser](https://github.com/LCA-ActivityBrowser/activity-browser)** and **[LCOPT](https://lcopt.readthedocs.io/en/latest/)**. These two Brightway2-extensions serve different purposes and require different settings, so check them out if you're curious.
# 
# ---

# And now, last but not least, here's our reward for finishing this notebook :)

# In[ ]:


from IPython.display import Image
Image(url="https://cdn.shopify.com/s/files/1/1869/0319/products/ART-dabbing-unicorn_color-powder-blue_1024x1024.jpg?v=1523903512")


# **Back to [table of contents](#section0)?**
# ***
