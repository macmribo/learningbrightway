#!/usr/bin/env python
# coding: utf-8

# # 8. Importing an Excel file with an unknown format

# In this notebook, we will use the ExcelImporter to get all data from the spreadsheet, but will have to write strategies to understand the data ourselves. This notebook is based on the original notebook written by [Christopher Mutel](https://github.com/brightway-lca/brightway2/blob/master/notebooks/IO%20-%20importing%20an%20Excel%20file.ipynb).

# In[1]:


from brightway2 import *
from stats_arrays import *


# ### Project setup

# In[2]:


projects.set_current('Tut_8_Importing_Excel_File')


# In[3]:


bw2setup()


# ### Import PVPS-Task12 database

# We will be importing a different notebook than the one imported in the original notebook (i.e. Ecoinvent 3.1). Since Us LCI is not behaving nicely for now, we will be importing the super relevant database from [*Life Cycle Inventories and Life Cycle Assessments of Photovoltaic Systems*](https://treeze.ch/fileadmin/user_upload/downloads/Publications/Case_Studies/Energy/IEA-PVPS-LCI-report-2020-20201208.pdf) you can download the data [here](https://treeze.ch/fileadmin/user_upload/downloads/Publications/Case_Studies/Energy/PVPS-Task12-19_2020_EcoSpold_LCI-PV-supplyChains.xlsx). 
# 
# Let's see if this works!
# 
# 
# 

# In[5]:


pv_lci = ExcelImporter("/Users/mmendez/Documents/Postdoc/Software_dev/Brightway/BW_Tutorials/BW2_BasicTutorial/data/PVPS-Task12-Separated/PVPS-Task12-19_2020_EcoSpold_LCI-PV-supplyChains.xlsx")


# Not great, it extracted only 6 worksheets... Let's just see what it extracted and how. Let's follow what CM did on his worksheet.

# In[8]:


dir(pv_lci)


# In[19]:


df = pv_lci.database_parameters


# In[20]:


df


# In[6]:


uncertainty_mapping = {
    0: UndefinedUncertainty.id,
    1: LognormalUncertainty.id,
    2: NormalUncertainty.id,
    3: TriangularUncertainty.id,
    4: UniformUncertainty.id
}


# In[ ]:


PROCESS_INDEX_NUMBER = 3707
PROCESS_INDEX_COL = 0
PROCESS_INDEX_ROW = 1
PROCESS_NAME_ROW = 2
PROCESS_LOCATION_ROW = 3
PROCESS_UNIT_ROW = 5

INPUT_GROUP_COL = 3
OUTPUT_GROUP_COL = 4
PRODUCTION_EXC_TYPE = 0
TECHNOSPHERE_EXC_TYPE = 5
BIOSPHERE_EXC_TYPE = 4

CATEGORY_COL = 7
SUBCATEGORY_COL = 8 

EXCHANGE_PRODUCTION_NAME_COL = 5
EXCHANGE_PRODUCT_COL = 12
EXCHANGE_PROCESS_COL = 13
EXCHANGE_LOCATION_COL = 14
EXCHANGE_UNIT_COL = 10
EXCHANGE_AMOUNT_DELTA = 0
EXCHANGE_UNCERTAINTY_TYPE_DELTA = 1
EXCHANGE_SD95_DELTA = 2
EXCHANGE_COMMENT_DELTA = 3


def get_exchange_type(data, row):
    if data[row][INPUT_GROUP_COL] == TECHNOSPHERE_EXC_TYPE:
        return "technosphere"
    elif data[row][OUTPUT_GROUP_COL] == BIOSPHERE_EXC_TYPE:
        return "biosphere"
    elif data[row][INPUT_GROUP_COL] == BIOSPHERE_EXC_TYPE:
        return "biosphere"
    elif data[row][OUTPUT_GROUP_COL] == PRODUCTION_EXC_TYPE:
        return "production"
    else:
        raise ValueError
    

def get_exchange_rows(data):
    return [x for x in range(len(data)) 
            if data[x][PROCESS_INDEX_COL] 
            and data[x][PROCESS_INDEX_COL] != "Index"]
    
    
def extract_exchanges(data, col):
    return [{
        'production name': data[row][EXCHANGE_PRODUCTION_NAME_COL],
        'activity name': data[row][EXCHANGE_PROCESS_COL],
        'categories': (data[row][CATEGORY_COL], data[row][SUBCATEGORY_COL],),
        'type': get_exchange_type(data, row),
        'reference product': data[row][EXCHANGE_PRODUCT_COL],
        'unit': data[row][EXCHANGE_UNIT_COL],
        'location': data[row][EXCHANGE_LOCATION_COL],
        'amount': data[row][col + EXCHANGE_AMOUNT_DELTA] or 0,
        'uncertainty type': uncertainty_mapping[data[row][col + EXCHANGE_UNCERTAINTY_TYPE_DELTA] or 0],
        'sd95': data[row][col + EXCHANGE_SD95_DELTA],  # Will need to be transformed
        'comment': data[row][col + EXCHANGE_COMMENT_DELTA]
    } for row in get_exchange_rows(data)]
    

def extract_process(data, col, sheet):
    return {
        'name': data[PROCESS_NAME_ROW][col],
        'unit': data[PROCESS_UNIT_ROW][col],
        'location': data[PROCESS_LOCATION_ROW][col],
        'worksheet': sheet,
        'exchanges': extract_exchanges(data, col)
    }


def process_sample_worksheet(obj):
    ws_name, data = obj

    nrows, ncols = len(data), len(data[0])
    
    # Create dictionary of processes referred to by column index
    processes = [extract_process(data, col, ws_name) 
                 for col in range(ncols) 
                 if data[PROCESS_INDEX_ROW][col] == PROCESS_INDEX_NUMBER]
    
    return processes


def process_sample_excel_data(data):
    return [item for obj in data for item in process_sample_worksheet(obj)]

