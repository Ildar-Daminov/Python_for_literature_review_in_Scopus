from pybliometrics.scopus import ScopusSearch,AbstractRetrieval,AuthorRetrieval
import pandas as pd 
import numpy as np 
import python_for_scopus_literature_review
from python_for_scopus_literature_review import functions,data_classes
from python_for_scopus_literature_review.data_classes import research_topic

#--------------------------------------------------------------------------
#                                Case study
#--------------------------------------------------------------------------


#--------------------------------- Input data --------------------------------
# Define th name of research topic 
name='self_consumption' # also used for naming the xlsx and npy files  

# Define the eid of one reference paper 
reference_paper_eid="2-s2.0-85123755228"

# Define the keywords as a criterion
keywords=['collective self-consumption'
          ]


#------------------------------ Doing the analysis --------------------------------
# Create an object of research topic 
self_consumption=research_topic(name,reference_paper_eid,keywords)

# Analyze the object "self_consumption"
results=self_consumption.analyze()


# -------------------------------- Output data ---------------------------------
# see the outputs xlsx - the main file with relevant publications 

# Additional files as publciations outside of scopus and with errors  
np.save(results.name+'_'+'publications_outside_scopus.npy',results.publications_outside_scopus)
np.save(results.name+'_'+'publications_with_errors.npy',results.publications_with_errors)
np.save(results.name+'_'+'paper_population.npy',results.paper_population)