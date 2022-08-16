#!/usr/bin/env python
# coding: utf-8

# # 0 &ensp; Introduction and main concepts

# ## 0.1 &ensp; Brightway2 M1 install

# Source: [Brightway](https://2.docs.brightway.dev/intro.html#intro) main documentation.
# 
# 
# 
# M1 Silicon has given me a lot of trouble. So, this is the installation version that worked for _me_. Before copy pasting like a monkey on Adderall, I would strongly recommend you to follow the steps in this marvelous [post](https://taylorreiter.github.io/2022-04-05-Managing-multiple-architecture-specific-installations-of-conda-on-apple-M1/). Since Brightway2 works with some packages that need Intel, having a terminal running on Rosetta (Intel translator) with miniconda3, and a terminal running on ARM64 with miniforge3 will save you A LOT of troibleshooting. I renamed my terminal iTerm Rosetta and use this terminal every time I use Brightway2. 
# 
# `conda create -n bw_rosetta python=3.9` 
# 
# `conda activate bw2_rosetta` (You can name your environment as you please of course!)
# 
# `conda config --append channels conda-forge`  
# 
# `conda config --append channels cmutel` 
# 
# `conda install brightway2 scikit-umfpack` 
# 
# `conda remove pypardiso --force`
# 
# 
# <div class="alert alert-block alert-info">
# <b>Tip:</b> I use Jupyterlab (or Jupyter Notebook) for a lot of stuff. What I do and work wonders is to install it in my base environment with <code>brew install jupyterlab</code> or <code>brew install jupyter</code>. Then, I go INSIDE my environment (<code>conda activate yadayada</code>) and install <code>ipykernel</code> with <code>conda install ipykernel</code> and FIIIINALLY I type <code>ipython kernel install --user --name=yadayada</code>. This way you store your environments in your notebook and can activate them inside jupyter. I know it is a lot, but I am saving you a lot of headaches. YOU ARE WELCOME.
# </div>
# 
# You can find how to install for Linux and Windows in the Brightway2 [documentation](https://2.docs.brightway.dev/installation.html).

# ## 0.2 &ensp; Glossary

# To understand some of the terminology used in Brightway (BW) it is important to grasp some general LCA terminology (from Hauschild's Glossary, p.1185—the actual reference for each word are specified in the glossary):
# 
# **Life cycle assessment (LCA):** Compilation and evaluation of the inputs, outputs and the potential environmental impacts of a product system throughout its life cycle.
# 
# **Life cycle inventory analysis (LCI):** Phase of life cycle assessment involving the compilation and quantification of inputs and outputs for a product throughout its life cycle.
# 
# **Life cycle impact assessment (LCIA):** Phase of life cycle assessment aimed at understanding and evaluating the magnitude and significance of the potential environmental impacts for a product system throughout the life cycle of the product
# 
# **Ecosphere:** Biosphere of earth, especially when the interaction between living and non-living components is emphasised.
# 
# **Technosphere:** The sphere or realm of human technological activity; the technologically modified environment
# 
# **Functional unit:** Defines the qualitative aspects and quantifies the quantitative aspects of the function, answers the questions *what?, how much?, for how long/how many times?, where? and how well?*. Quantified performance of a product system for use as a reference unit.
# 
# **Unit process or node:** Smallest element considered in the life cycle inventory analysis for which input and output data are quantified.
# 
# **Product system**: Collection of unit processes with elementary and product flows, performing one or more defined functions, and which models the life cycle of a product.
# 
# **Input**: Product, material or energy flow that enters a unit process. *Note: Products and materials include raw materials, intermediate products and co-products.*
# 
# **Output:** Product, material or energy flow that leaves a unit process. *Note: Products and materials include raw materials, intermediate products, co-products and releases.*
# 
# **Resource flow:** Input flow sourced directly from the ecosphere, this flow had no human intervention.
# 
# **Emission flow:** Output flow released into the ecosphere without subsequent human transformation.
# 
# **Energy flow:** Input or output of a unit process or product system quantified in energy units.
# 
# **Material or Product flow:** Products entering from or leaving to another product system.
# 
# **Intermediate flow:** Product, material or energy flow occurring between unit processes of the product system being studied.
# 
# **Reference flow**: Measure of the outputs from processes in a given product system required to fulfil the function expressed by the functional unit.
# 
# **Characterization factor**: Factor derived from a characterization model which is applied to convert an assigned life cycle inventory analysis result to the common unit of the category indicator. *Note*: The common unit allows calculation of the category indicator result.
# 
# **Characterization model**: Reflect the environmental mechanism by describing the relationship between the LCI results, category indicators and, in some cases, category endpoint(s). The characterization model is used to derive the characterization factors.
# 
# ![PROJECT:](images/unitprocess_flows.jpg)
# 
# 

# ## 0.3 &ensp; Project structure

# The following image represent the hierarchy in a Brightway project:
# 
# ![PROJECT:](images/project_layout.svg)
# 
# **Inventory databases:** *Object* used to organize nodes and edges (unit processes and flows, respectively)  in a life cycle inventory analysis (LCI).
# 
# **Activities and exchanges:** Nodes are called *activities*, include transforming and market activities, but also product and biosphere flows. Edges are called *exchanges*, describe the relationship betweem two nodes. E.g. input of a product to a transforming activity, or an emission of a biosphere flow by an activity, or name and amount of a product oriduced by an activity. In short: activities are unit processes and exchanges are flows.

# ### &ensp; 0.3.1 Activities

# A database consists of a series of inventory datasets, datasets are human-readable, editable text documents. Usually they com in .json format. But BW is flexible with all sorts of formats. BW has a flexible free text form (even an empty dictionary is accepted). However, there are fields suggested:
# 
# 
# The activity data structure is:
# 
# * `'name'` (string): Name of this activity.
# 
# * `'type'` (string): If this is `'process'`, or omitted completely, Brightway2 will treat this as a inventory process with inputs and output(s). If you want to store additional information in a Database outside of the list of processes, specify a custom type here. For example, the list of biosphere flows is also an inventory database, but as these are flows, not processes, they have the type `'emission'`. Similarly, if you wanted to separate processes and products, you could create database entries for the products, with the type `'product'`. Other `'type'` includes `'biosphere'`.
#     
# * `'categories'` (list of strings, optional): A list of categories and subcategories. No length limits.
#     
# * `'location'` (string, optional): A location identifier. Default is GLO, but this can be changed in the User preferences.
#     
# * `'unit'` (string): Unit of this activity. Units are normalized when written to disk.
#    
# * `'exchanges'` (list): A list of activity inputs and outputs (it can have many!), minitum items are `'inout'`, `'type'`, and `'amount'`:
# 
#     *`'input'` (database name, database code): The technological activity that is linked to, e.g. ("my new database", "production of ice cream") or ('biosphere', '51447e58e03a40a2bbd9abf45214b7d3'). See also Uniquely identifying activities.
# 
#     *`'type'` (string):It can be production, technosphere, or biosphere. See Exchange data format.
# 
#     *`'amount'` (float): Amount of this exchange.
#        
#     *`'uncertainty type'` (integer): Integer code for uncertainty distribution of this exchange, see Storing uncertain values for more information. There can be other uncertainty fields as well.
# 
#     *`'comment'` (string, optional): A comment on this exchange. Used to store pedigree matrix data in ecoinvent v2.
# 
# Example:
# ```python
# {
#  'categories': ['Wood Product Manufacturing', 'Softwood Veneer and Plywood Mnf.'],
#  'location': 'RNA',
#  'name': 'Green veneer, at plywood plant, US PNW',
#  'type': 'process',
#  'unit': 'kilogram',
#  'exchanges': [{
#    'amount': 1.0,
#    'code': 6,
#    'group': 2,
#    'input': ('US LCI', '6ddb4cc00f9e42aa48515248256c31dc'),
#    'type': 'production',
#    'uncertainty type': 0},
#   {'amount': 7.349999999999999e-06,
#    'code': 5,
#    'group': 4,
#    'input': ('biosphere', '51447e58e03a40a2bbd9abf45214b7d3'),
#    'type': 'biosphere',
#    'uncertainty type': 0}],
# }
# ```

# ### &ensp; 0.3.2  Exchanges

# Exchanges are lists of inputs and outputs of an activity. Exchanges have a `'type'`, there are four standard exchange `'type': `'production'`, `'substitution'`, `'technosphere'`, and `'biosphere'`.
# 
# * `'production'`: How much of the output is produces by an activity.
# 
# * `'substitution'`: used in multi-output processess to indicate the avoided production of a product by another activity, always positive value.
# 
# * `'technosphere'`: input from the technosphere, i.e. industrial economy: the process “make a fizzbang” could have an input of seven kilograms of lollies.
# 
# * `'biosphere'`: consumtion of a resource or emission to the environment, the value is placed in the biosphere matrix.
# 
# **Sign convention**
# 
# * `'biosphere'`: Values are not modified.
# * `'production'`: and `'substitution'`: Values are not modified.
# * `'technosphere'`: Multiplied by -1 and inserted into the technosphere matrix, -1 means consumption of products, +1 means production or substitution (forces the substituted activity to have a negative production amount, representing the avoided production pathwayforces the substituted activity to have a negative production amount, representing the avoided production pathway). 
# 
# These rules are consistent with the traditional Leontief inverse of IO tables:
# 
# /begin{equation}
# x = (I-A)^{-1}d
# /end{equation}
# 
# Default metadata in Brightway follows ecoinvent system assumptions about biosphere flow categories:
# 
# * _Air_, _soil_, and _water_ are emissions into the natural environment.
# * _Natural resource_ flows are consumtion of natural resources from the natural environment.
# 
# **Note**: Negative biosphere values reverse these assumptions, e.g.: -2 kg of $CO_2$  with category *air* would be <ins>removal</ins> of $CO_2$ from the natural environment. Signs do not really matter as long as there is consistency with the signs of the impact assessment characterization factors.

# ## 0.4 &ensp; Database

# Brightway2 stores each database in a separate file within the Project folder. It also support pluggable database backends, which can change how databases are stores and queried.
# 
# BW2 also provides `bw2data.backends.JSONDatabase`, which stores each dataset as a se[arate file serialized to `JSON`. This approach works well with version control  systems, as each database can be saved individually, see the [documentation](https://2.docs.brightway.dev/technical/bw2data.html#json-database).

# In[ ]:




