from pybliometrics.scopus import ScopusSearch,AbstractRetrieval,AuthorRetrieval
# import time
import pandas as pd 
import numpy as np 
import Python_for_literature_review_in_Scopus
from Python_for_literature_review_in_Scopus import functions,data_classes
from Python_for_literature_review_in_Scopus.data_classes import research_topic

#--------------------------------------------------------------------------
#                                Case study
#--------------------------------------------------------------------------


#----------------------------------Input data---------------------------------
# Define th name of research topic 
name='Anthony_code'

# Define the eid of one reference paper 
reference_paper_eid="2-s2.0-85123755228"

# Define the keywords as a criterion
keywords=['collective self-consumption'
          ]


#-------------------------------Doing the analysis---------------------------------
# Create an object 
hosting_capacity=research_topic(name,reference_paper_eid,keywords)

# Analyze the object "hosting capacity"
results=hosting_capacity.analyze()


# -------------------------------- Output data---------------------------------
np.save(results.name+'_'+'publications_outside_scopus.npy',results.publications_outside_scopus)
np.save(results.name+'_'+'publications_with_errors.npy',results.publications_with_errors)
np.save(results.name+'_'+'paper_population.npy',results.paper_population)
