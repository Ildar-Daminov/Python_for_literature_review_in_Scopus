from pybliometrics.scopus import ScopusSearch,AbstractRetrieval
import time

#--------------------------------------------------------------------
                    # Definition of functions 
#--------------------------------------------------------------------

# Create a global variable 
global paper_population # list of paper eids related to a studied topic

# Get_citing_papers for cited paper
def get_citing_papers(reference_paper_eid):
    query = f"REF({reference_paper_eid})" # create a query 
    try:
        s = ScopusSearch(query) # search in scopus using a query 
        citing_papers = s.results # extract data  on  papers , citing the reference paper 
    except :
        citing_papers=0

    return citing_papers 

# Get_cited_papers for given reference paper 
def get_cited_papers(reference_paper_eid):
    ss = AbstractRetrieval(reference_paper_eid, view='FULL') # Extract data on Abstact of reference paper
    cited_papers = ss.references # extract the reference list of given paper (reference_paper_eid)
    return cited_papers 

# Get eids for citing or cited paper 
def get_EIDS(paper_object):
    
    eids_list=[]
    if paper_object is None:
        pass
    elif len(paper_object)==0:
        pass
    else: 
        # Extract eids from paper object
        for paper in range(len(paper_object)):
            if hasattr(paper_object[paper], 'eid'): # if eid exists
                # Extract eids for given paper
                eids_list.append(paper_object[paper].eid)
            else: # if eid does not exist then extract id (same as eid but without "2-s2.0-"")
                if  paper_object[paper].id is not None: 
                    eids_list.append("2-s2.0-"+str(paper_object[paper].id))
                else:
                    print('No id. Probably reference is not in Scopus')
                    print('Title:',paper_object[paper].fulltext)

            
    return eids_list 

def get_paper_population(eids_list):
    global paper_population
    if 'paper_population' in globals():
        
        # Append eids_list to paper population
        for eid in range(len(eids_list)):
            if eids_list[eid] in paper_population: 
                pass # do nothing 
            
            else: # eids_list[eid] is not in population 
                
                # Add eids_list[eid] into population
                paper_population.append(eids_list[eid])

    else: # there is no variable "paper_population" in globals 
              
        # Create a population of paper on investigated topic
        paper_population=list(set(eids_list))

    return paper_population
         
#------------------------------Case study-------------------------------

#--------------First iteration: Create an initial population------------

# Start with eid of one reference paper 
reference_paper_eid="2-s2.0-85101235827"

# Get citing papers for given reference paper
citing_papers=get_citing_papers(reference_paper_eid)

# Get cited papers for given reference paper
cited_papers=get_cited_papers(reference_paper_eid)

# Get EID of these citing and cited papers 
eid_list_citing=get_EIDS(citing_papers)
eid_list_cited=get_EIDS(cited_papers)

# Print results for citing papers
print('Number of citing paper: ',len(citing_papers))
print('List of citing paper: ',eid_list_citing)

# Print results for cited papers
print('Number of cited paper: ',len(cited_papers))
print('List of cited paper: ',eid_list_cited) 

# Add cited papers into population
get_paper_population(eid_list_cited)
print('Number of papers in population after adding cited paper: ',len(paper_population))

# Add citing papers into population
get_paper_population(eid_list_citing)   
print('Number of papers in population after adding citing paper: ',len(paper_population))

#----------------------------Second iteration: Growing the population----------------------------

# Assume that  papers were not analyzed yet 
number_analysed_papers=0

# Create a list of non-analysed and analysed papers 
non_analysed_papers=paper_population
analysed_papers=[] # empty list
errors_count=0 

while number_analysed_papers!=len(paper_population): # while we do not analyze everything 
    
    # Refresh status of errors 
    no_errors_with_citing_papers=1 # 1 means true i.e. no erros exist
    no_errors_with_cited_papers=1 # 1 means true i.e. no erros exist
    
    if number_analysed_papers==0: # first iteration
        
        # Take a first paper from population
        reference_paper_eid=paper_population[0] 
        
        # Get citing papers for given reference paper
        citing_papers=get_citing_papers(reference_paper_eid)

        # Get cited papers for given reference paper
        cited_papers=get_cited_papers(reference_paper_eid)

        # Get EID of these citing and cited papers 
        eid_list_citing=get_EIDS(citing_papers)
        eid_list_cited=get_EIDS(cited_papers)

        # Add cited papers into population
        get_paper_population(eid_list_cited)

        # Add citing papers into population
        get_paper_population(eid_list_citing)   
        print('Population:', len(paper_population))

        # increase the count of analysed papers  
        number_analysed_papers+=1
        print('Papers analised: ',number_analysed_papers)

        analysed_papers.append(reference_paper_eid)
        
        # Remove analysed paper from non_analysed_papers 
        non_analysed_papers.remove(reference_paper_eid)
        print('Non_analysed:', len(non_analysed_papers))
        print(' ')
        
    else: # number_analysed_papers!=0 i.e. >0
         
        # Take a first paper from non_analysed_papers
        reference_paper_eid=non_analysed_papers[0] 
        
        try: 
            # Get citing papers for given reference paper
            citing_papers=get_citing_papers(reference_paper_eid)
        except:
            no_errors_with_citing_papers=0
            print('Error with citing papers')
            errors_count+=1
        try: 
            # Get cited papers for given reference paper
            cited_papers=get_cited_papers(reference_paper_eid)
        except:
            no_errors_with_cited_papers=0
            print('Error with cited papers')
            errors_count+=1
        if no_errors_with_citing_papers==1:
            
            if citing_papers!=0:
                # Get EID of these citing and cited papers 
                eid_list_citing=get_EIDS(citing_papers)
                
                # Add citing papers into population
                get_paper_population(eid_list_citing)    
            else:
                pass
                    
        elif no_errors_with_cited_papers==1:
            
            if cited_papers!=0:
                eid_list_cited=get_EIDS(cited_papers)
                
                # Add cited papers into population
                get_paper_population(eid_list_cited)        
            else:
                pass
        else:
            print('Error problem')


    print('Population:', len(paper_population))

    # increase the count 
    number_analysed_papers+=1
    print('Papers analised: ',number_analysed_papers)

    # Add to the list of analysed papers
    analysed_papers.append(reference_paper_eid)

    # Update non-analysed papers with consideration of newly populated papers
    non_analysed_papers = list(set(paper_population).difference(analysed_papers))
    print('Non_analysed:', len(non_analysed_papers))
    print(' ')
    #time.sleep(2)    # Pause 3 seconds
        
        # TODO next: 
        # Handling Error if no citation exists
        # Handling Error if paper lacks the data 
        # Handling Errors in general  
        
        # Design a output as dataframe 
        
        
        ## Plot the graph 