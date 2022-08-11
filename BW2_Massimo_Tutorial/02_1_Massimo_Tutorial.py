#!/usr/bin/env python
# coding: utf-8

# # 1.4 &emsp; Simple LCA - Navigating through activities and exchanges

# This tutorial, based on [Massimo's](https://github.com/massimopizzol/B4B/blob/main/02.1_Simple_LCA_selecting_activities_exchanges_revised.py) of course! will show you how to explore your database and swing through the activities and exchanges!

# In[86]:


from brightway2 import *
projects.report()


# We will be using the database created in [01_2_Massimo_Tutorial](01_2_Massimo_Tutorial.ipynb), so we are going to copy into a new project. Remember how to do it? Uncomment the following lines to copy if this is the first time you run this code. Otherwise, jump and run to `projects.set_current('1_4_Massimo')`.

# In[87]:


# projects.set_current('1_2_Massimo')


# In[88]:


# projects.copy_project('2_1_Massimo') # If you run this more than once, it will throw an error saying that 1_4_Massimo already exists!!


# Even though after you copy a project, it sets you in such project, this is a sanity check, because if you run this code more thant once `copy_project` will not work!

# In[89]:


projects.set_current('2_1_Massimo')


# Now let's run the LCA basic analysis:

# In[90]:


t_db = Database('testdb')  
functional_unit = {t_db.get('Electricity production'): 1000}
lca = LCA(functional_unit)
lca.lci()

myLCIAdata = [[('testdb', 'Carbon dioxide'), 2.0],
              [('testdb', 'Sulphur dioxide'), 2.0],
              [('testdb', 'Crude oil'), 2.0]]

method_key = ('simplemethod', 'imaginaryendpoint', 'imaginarymidpoint') 
my_method = Method(method_key)
my_method.validate(myLCIAdata) # Need to figure out what these do
my_method.register()           # Need to figure out what these do
my_method.write(myLCIAdata)    # Need to figure out what these do
my_method.load()               # Need to figure out what these do

lca = LCA(functional_unit, method_key)  # LCA calculations with method
lca.lci()
lca.lcia()
print("This is the LCA inventory")
print(lca.inventory)
print("This is the LCA characterizedinventory")
print(lca.characterized_inventory)
print('This is the environmental score:')
print(lca.score)


# But we already knew these things, didn't we! Let's fish some activities and exchanges:

# First let's get `Electricity production`

# In[29]:


el = t_db.get('Electricity production') 
print(el)


# We can check the keys of that activity dictionary:

# In[30]:


for i in el:  # these the possible keys of an activity dictionary
    print(i)


# This is another way that also gives you the values:

# In[37]:


el.as_dict() 


# This option just gives you the values:

# In[45]:


print(el['name'],'\n', el['code'],'\n', el['unit'],'\n', el['database'])


# The following shows how to extract the exchanges of the activity object. Massimo here is trying to check what works and what doesn't and I find it hilarious.

# In[44]:


#el['exchanges']  # this does not work.
#el.exchanges()  # neither this
list(el.exchanges())  # yeps, this one


# Or we can loop through them to visualize all exchanges:

# In[70]:


for exc in el.exchanges():  # or this, visualize all exchanges of an activity
    print(exc,'\n', exc['type'], '\n', exc['input'][1], '\n', exc.input, '\n')


# To get the first exchange:

# In[72]:


el_exc = list(el.exchanges())[0]


# Let's compare getting three extracting method objects by looking at their `type()`:

# In[74]:


print(type(el))  # compare the three
print(type(el.exchanges()))
print(type(el_exc))


# Aha! Our objects go from `Activity` to `Exchanges` (all of them) to `Exchange` (just one!)

# Let's look at the things inside our exchange object:

# In[75]:


for i in el_exc:  # the possible keys of an exchange (DICT iteration)
    print(i, ':', el_exc[i])


# Interesting! This one has the `output` key, but we never defined an `output` in the original database dicitonary, if something... we called it `input`, how can this be??!! This is because when an exchange is identified as `'type': 'production'`, brightway2 then knows it is an `output`!

# Here are some other ways of pulling out exchanges:

# In[76]:


el_exc.as_dict()


# In[77]:


el_exc.items()


# In[78]:


el_exc.unit == el_exc['unit']  # equivalent ways, different from activities
print(el_exc['amount'], el_exc['unit'], el_exc['input'], 'to',
      el_exc['output'], 'within', el_exc['type'])


# In[81]:


el_exc.input  # I guess the intended meaning of 'input' is "from'


# In[82]:


el_exc.output  # I guess the indended meaning of 'output' is 'to'


# What if I want to get a specific exchange of a specific activity. Without using numeric indexing, but by using its name! Let's see if we can find the value of the CO2 emissions from el.

# In[83]:


for exc in list(el.exchanges()):
    if exc['input'] == ('testdb', 'Carbon dioxide'):
        print(exc)
    else:
        print('Not this one')


# Good! Now we store the value in a variable

# In[84]:


for exc in list(el.exchanges()):
    if exc['input'] == ('testdb', 'Carbon dioxide'):
        elCO2_amount = exc['amount']
        
print(elCO2_amount)


# Ta dá!

# In[ ]:




