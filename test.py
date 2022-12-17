from pybliometrics.scopus import ScopusSearch,AbstractRetrieval,AuthorRetrieval
# import time
import pandas as pd 
import numpy as np 
import Python_for_literature_review_in_Scopus
from Python_for_literature_review_in_Scopus import functions,data_classes,research_topic
#--------------------------------------------------------------------------
#                                Case study
#--------------------------------------------------------------------------

#-------------------------------Input data---------------------------------
# Define the eid of one reference paper 
reference_paper_eid="2-s2.0-85085924004"

# Define the keywords as a criterion
keywords=['hosting capacity',
          'Hosting capacity',
          'hosting capacities', 
          'Hosting capacities'
          ]

hosting_capacity=research_topic(reference_paper_eid,keywords)

# ---------------------------- Output data---------------------------------