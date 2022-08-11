#!/usr/bin/env python
# coding: utf-8

# # 2. Projects

# A project is a separate workspace with its own data and preferences. Project management is done through the `projects` object. This tutorial is a copy of the oficial [tutorial](https://github.com/brightway-lca/brightway2/blob/master/notebooks/Projects.ipynb) with some additional information for a more comprehensive learning experience.

# Methods used throughout this tutorial:
# 
# * `list(projects)`: Returns a list. Here it is used to return the amount of projects in the brightway2 folder.
# 
# * `projects.set_current('project_name')`: Goes to the project and creates a new project if tht name does not exist.
# 
# * `list(databases`: Lists the databases in that project.
# 
# * `bw2setup()`: Creates a default biosphere.
# 
# * `projects.dir`: Shows the location of the current project.
# 
# * `projects.request_directory('sub_directory')`: Creates a sub directory inside the project folder.
# 
# * `projects.copy_project('copy_name')`: Copies the current project and automatically activates the copied project.
# 
# * `projects.current`: Shows the active project.
# 

# In[1]:


from brightway2 import *


# List existing projects:

# In[2]:


list(projects)


# Switching projects is the same as adding a project, if the project does not exist it will be created.

# In[3]:


projects.set_current('Tut_2_Projects')
list(projects)


# New projects start empty, it is possible to add a default biosphere and impact assessment methods:

# In[4]:


list(databases)


# In[5]:


bw2setup()


# In[6]:


list(databases)


# Each project is a directory:

# In[7]:


projects.dir


# We can add subdirectories to the project if needed (e.g. for custom data):

# In[8]:


projects.request_directory("Tut_2_sub_directory")


# Finally, you can copy projects. A copy is made on the current project, so make sure to switch to the project you want to copy first and it automatically switches projects to the copied one!

# In[10]:


projects.copy_project("Tut_2_the copy")


# In[ ]:


projects.current


# In[11]:


list(projects)


# In[ ]:





# In[ ]:





# In[ ]:




