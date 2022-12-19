from pybliometrics.scopus import ScopusSearch,AbstractRetrieval,AuthorRetrieval
# import time
import pandas as pd 
import numpy as np 

#--------------------------------------------------------------------
                    # Definition of functions # 
#--------------------------------------------------------------------

# Get_citing_papers for reference paper
def get_citing_papers(reference_paper_eid):
    """
    This function returns a list of citing papers for a given paper.
    
    INPUT:
    - reference_paper_eid: the eid of paper in Scopus e.g 2-s2.0-85101235827
    OUTPUT:
    - citing_papers: citing papers of given eid
    
    """
    # Create a query 
    query = f"REF({reference_paper_eid})" 
    
    try: # try to query through ScopusSearch from pybliometrics
        # Search in scopus using a query 
        s = ScopusSearch(query) 
        
        # Extract data  on  papers , citing the reference paper 
        citing_papers = s.results 
    
    except : # if any problem with the ScopusSearch from pybliometrics
        
        # Assume citing_papers as 0
        citing_papers=0
        
    return citing_papers 

# Get_cited_papers for given reference paper 
def get_cited_papers(reference_paper_eid):
    """
    This function returns a list of references for a given paper. 
    
    INPUT:
    - reference_paper_eid: the eid of paper in Scopus e.g 2-s2.0-85101235827
    OUTPUT:
    - cited_papers: references of given paper's eid
    
    """    
    # Extract data on Abstact of reference paper
    ss = AbstractRetrieval(reference_paper_eid, view='FULL') 
    
    # Extract the reference list of given paper (reference_paper_eid)
    cited_papers = ss.references 
    
    return cited_papers 

# Get eids for citing or cited paper 
def get_EIDS(paper_object,publications_outside_scopus):
    """
    This function returns a list of eids for a given paper according
    to Scopus database. If paper is  not in Scopus, then it is saved 
    into  publications_outside_scopus.
    
    INPUT:
    - paper_object: information extracted from query using a ScopusSearch
    - publications_outside_scopus - a list for saving the publications which are not available in Scopus 
      
    OUTPUT:
    - eids_list: list of eids in Scopus database 
    
    """
    # Create an empty list (for filling in)
    eids_list=[]
    
    # Checking some cases of paper_object
    if paper_object is None: 
        pass # do nothing 
    elif paper_object==0:
        pass # do nothing 
    elif len(paper_object)==0:
        pass # do nothing 
    else: 
        # Extract eids from paper object
        for paper in range(len(paper_object)):
            if hasattr(paper_object[paper], 'eid'): # if eid exists
                
                # Extract eids for given paper
                eids_list.append(paper_object[paper].eid)
                
            else: # if eid does not exist then extract id (same as eid but without "2-s2.0-"")
                
                if  paper_object[paper].id is not None:
                    # Append the paper's id to eids_list 
                    eids_list.append("2-s2.0-"+str(paper_object[paper].id))
                else:
                    # Append the paper name to the publications_outside_scopus 
                    publications_outside_scopus.append(str(paper_object[paper].fulltext))
    return eids_list 

def get_paper_population(eids_list,paper_population):
    """
    This function check if papers from eids_list already exist in a 
    population of papers (from Scopus). If yes, the code returns the 
    exisitng population. If not, the code adds the papers into 
    existing population and returns it.
    
    INPUT:
    - eids_list: a list of papers - candidates for adding into a population 
    - paper_population: the current population of papers on a given topic
      
    OUTPUT:
    - paper_population: updated (or current) population of papers on 
                        a given topic
    
    """
    
    if eids_list!=0: # eids_list is not a zero

        # Append eids_list to paper population
        for eid in range(len(eids_list)): # for each eid from eids_list
            
            if eids_list[eid] in paper_population: # if eid is already in population 
                pass # do nothing 
            
            else: # eids_list[eid] is not in population 
                # Add eids_list[eid] into population
                paper_population.append(eids_list[eid])

    else: # if eids_list==0
        pass # do nothing 
    
    return paper_population


def check_related_articles(eid_list,keywords,publications_with_errors):
    """
    This function extracts only  papers corresponding to the given topic.
    The criterion for keeping or not the paper is a presence of
    predefined keywords in a paper's title, abstract or among author 
    keywords.
    
    INPUT:
    - eids_list: a list of papers for processing on keywords  
    - keywords: user defined keywords
    - publications_with_errors: list where a publication is saved if 
                                any error occurs during the processing 
      
    OUTPUT:
    - eid_list: a list of kept papers corresponding to the given topic
    """    

    # Prepare a zero vector (used later as one of the function output)
    decision_vector=np.zeros(len(eid_list)) # 0 - drop the paper ; 1 - keep the paper 

    # Checking the papers eids from the given eid_list
    for idx,paper_eid in enumerate(eid_list): # for each paper eid

        # Checking the abstract by keywords 
        try:
            # Extract data on Abstact of given paper
            ss = AbstractRetrieval(paper_eid, view='FULL') 
                
            # Checking the matching of keywords in abstract
            if hasattr(ss, 'abstract'): # if an abstract exists
                paper_abstract=ss.abstract # extract a paper abstract 
                
                # Check if any keywords exist in a paper abstract 
                if any(keyword in paper_abstract for keyword in keywords):
                    decision_vector[idx]=1 # add 1 into a zero vector
            
            if decision_vector[idx]!=1: # if still zero
                # Check keywords in author keywords
                if hasattr(ss, 'authkeywords'):# if author keywords exist
                    paper_keywords=ss.authkeywords # extract author keywords 
                    
                    # Check if any keywords exist in  paper_keywords
                    if paper_keywords is not None and any(keyword in paper_keywords for keyword in keywords):
                        decision_vector[idx]=1 # add 1 into a zero vector

            if decision_vector[idx]!=1: # if still zero
                # Check keywords in title 
                if hasattr(ss, 'title'): # if a title exists 
                    paper_title=ss.title # extract a paper's title
                    
                    # Check if any keywords exist in title
                    if any(keyword in paper_title for keyword in keywords):
                        decision_vector[idx]=1 # add 1 into a zero vector
                        
        except Exception as exception: # if any error with AbstractRetrieval occured

            # Print in command line the error name and eid of a paper
            print(type(exception).__name__,'with ',paper_eid)
            
            # Save the paper eid in a special list (for post analysis)
            publications_with_errors.append([type(exception).__name__,'with ',paper_eid])
            
            # Continue 
            pass
        
    # Deciding on the paper: drop or keep (in a population)
    if np.sum(decision_vector)>0: # if there is at least one '1'
        
        # Find the indexes of ones in a decision_vector
        ones_indexes = [i for i,val in enumerate(decision_vector) if val==1]
        
        # Create an empty list
        intermediate_list=[]
        
        # Extract the eids which corresponds to the status 1 (relevant publication)
        for i in range(len(ones_indexes)):
            index=ones_indexes[i]
            intermediate_list.append(eid_list[index])
        
        # Save  intermediate_list as output of the function  
        eid_list=intermediate_list
        
    else: # if all values are zero in ones_indexes
        
        # Assume eid_list=0
        eid_list=0
        
    return eid_list       
   
   
   
# Function to retrive the metadata for each paper from scopus populations
def retrieve_paper_data(paper_population):
    """
    This function retrieves the metadata for each paper from a given
    population of papers (in Scopus). 
    
    INPUT:
    - paper_population: a list of eids representing the population of papers 
    
    OUTPUT:
    - df: a dataframe with several columns (see below)
    """

    # Column names 
    column_names=['eid','title','publicationName','coverDate','refcount','citedby_count','doi']
    
    # Create an empty dataframe  
    df=pd.DataFrame(columns = column_names)
    
    if paper_population is None: # if paper_population does not have a data 
        
       pass # do nothing and return df without data 
   
    else: # if population is NOT None 
        
        for idx,paper_eid in enumerate(paper_population):  # for each paper eid      
           
           # Retrieve data for a given paper  
           paper_data = AbstractRetrieval(paper_eid, view='FULL') # Extract entire metadata on Abstact of reference paper
           
           # Preselect the data for df
           retrieved_data=[paper_eid, paper_data.title,paper_data.publicationName,paper_data.coverDate,paper_data.refcount,paper_data.citedby_count,paper_data.doi]
           
           # Create an intermediate dataframe with retreived data for the given paper
           df2 = pd.DataFrame([retrieved_data],columns=column_names)
           
           # Concatenate dataframes df and df2
           df=pd.concat([df,df2])
           
    return df # return dataframe with retreived data for all papers in population 

def ploting_connection_graph(paper_population,publications_outside_scopus):
    """
    This function plots an interactive graph of paper population and saves
    it in xlsx format.  
    
    INPUT: 
    - paper_population - a population of papers (a list of eids)
    - publications_outside_scopus - list of publications outside of scopus (required for get_EIDS)
    
    OUTPUT:  
    interactive html graph: a html plot, automatically generated and opened in browser 
    - graph_df.xlsx - excel table, representing the created graph
    
    """
    
    # import neccesary packages 
    import networkx as nx
    import matplotlib.pyplot as plt
    from bokeh.io import output_notebook, show, save
    from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
    from bokeh.plotting import figure
    from bokeh.plotting import from_networkx
    
    # Create column names (for an excel table)
    columns_name=['primary_list','secondary_list','Direction']
    direction_forward=1  # 'primary_secondary' it means the paper from primary list cites the paper from secondary list
    direction_backward=2 # 'secondary_primary' it means that the paper from SECONDARY list cites the paper from primary list 
    
    # Create an empty dataframe 
    graph_df=pd.DataFrame(columns=columns_name)
    
    for idx,paper_eid in enumerate(paper_population):  # for each paper eid
        
        # Get citing and cited papers for given reference paper
        citing_papers=get_citing_papers(paper_eid)
        cited_papers=get_cited_papers(paper_eid)

        # Get EID of these citing and cited papers 
        eid_list_citing=get_EIDS(citing_papers,publications_outside_scopus)
        eid_list_cited=get_EIDS(cited_papers,publications_outside_scopus)        
        
        eid_list_citing = set(eid_list_citing) # convert to set 
        eid_list_cited=set(eid_list_cited)  # convert to set      

        # Apply intersection to sets and convert to list 
        eid_list_citing = list(eid_list_citing.intersection(paper_population)) 
        eid_list_cited = list(eid_list_cited.intersection(paper_population)) 
        
        if len(eid_list_citing)!=0: 
            # Prepare graph_df for citing articles 
            intermediate_df=pd.DataFrame(columns=columns_name)
            intermediate_df['primary_list']=[paper_eid]*len(eid_list_citing)
            intermediate_df['secondary_list']=eid_list_citing
            intermediate_df['Direction']=list(str(direction_backward))*len(eid_list_citing)
            graph_df=pd.concat([graph_df,intermediate_df])

        if len(eid_list_cited)!=0: 
            # Prepare graph_df for cited articles (references)
            intermediate_df=pd.DataFrame(columns=columns_name)
            intermediate_df['primary_list']=[paper_eid]*len(eid_list_cited)
            intermediate_df['secondary_list']=eid_list_cited
            intermediate_df['Direction']=list(str(direction_forward))*len(eid_list_cited)
            graph_df=pd.concat([graph_df,intermediate_df])
        
    # -------------- Plotting part ---------------------
    graph_df.to_excel('graph_df.xlsx',index=False)

    
    # Create a G graph between restaurants and customers
    G=nx.from_pandas_edgelist(graph_df,
                            target='primary_list',
                            source='secondary_list') # 
    
    #Choose a title!
    title = 'Interconnection of papers in their population'

    #Establish which categories will appear when hovering over each node
    HOVER_TOOLTIPS = [("Scopus eid", "@index")]

    #Create a plot — set dimensions, toolbar, and title
    plot = figure(width=1400, height=700,tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
            x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)
    network_graph = from_networkx(G, nx.spring_layout, scale=10, center=(0, 0))

    #Set node size and color
    network_graph.node_renderer.glyph = Circle(size=7, fill_color='skyblue')

    #Set edge opacity and width
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

    #Add network graph to the plot
    plot.renderers.append(network_graph)

    # Show a plot
    show(plot)

    return graph_df

def calculate_connections_number(graph_df,paper_population):
    """
    This function calculates the number of connections per each paper 
    in a population of papers. 
    
    INPUT:
    - graph_df: a dataframe generated in the function ploting_connection_graph()
    - paper_population: a population of papers (a list of eids)
    
    OUTPUT:
    - df: an intermediate column 
    connections: a dataframe (paper's metadata+ number of connections inside of population) 
    
    """

    # Calculate the count (the column for merging later)  
    df=graph_df.groupby(['primary_list','secondary_list']).size().reset_index().rename(columns={0:'count'})

    # Find a number of connections
    connections=df.groupby('primary_list').sum()

    # Extract metadata for population  
    population_data=retrieve_paper_data(paper_population)

    # Merge into a new dataframe
    connections = pd.merge(population_data, connections,left_on='eid', right_on='primary_list')

    return connections