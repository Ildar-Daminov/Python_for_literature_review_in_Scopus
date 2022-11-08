from pybliometrics.scopus import ScopusSearch,AbstractRetrieval,AuthorRetrieval
# import time
import pandas as pd 
import numpy as np 

#--------------------------------------------------------------------
                    # Definition of functions # 
#--------------------------------------------------------------------

# Create a global variable 
global paper_population # list of paper eids related to a studied topic
global publications_outside_scopus # list of relatve publications outside of scopus  
global publications_with_errors

# Get_citing_papers for reference paper
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
    global publications_outside_scopus

    eids_list=[]
    if paper_object is None:
        pass
    elif paper_object==0:
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
                    # print('No id. Probably reference is not in Scopus')
                    # print('Title:',paper_object[paper].fulltext)
                    if "publications_outside_scopus" in globals(): # if variable is already created 
                       publications_outside_scopus.append(str(paper_object[paper].fulltext))
                    else: # if variable is not created yet
                        # create "publications_outside_scopus" and append
                        publications_outside_scopus=[] 
                        publications_outside_scopus.append(str(paper_object[paper].fulltext))
    return eids_list 

def get_paper_population(eids_list):
    global paper_population
    
    if eids_list!=0: # eids_list is not a zero
        if 'paper_population' in globals():
            
            # Append eids_list to paper population
            for eid in range(len(eids_list)):
                if eids_list[eid] in paper_population: 
                    pass # do nothing 
                
                else: # eids_list[eid] is not in population 
                    
                    # Add eids_list[eid] into population
                    paper_population.append(eids_list[eid])

        else: # there is no variable "paper_population" in globals 
                
             # Create a paper population from given eids_list
             paper_population=list(set(eids_list))
             
             # it works only once 
             
    else: # if eids_list==0
        if 'paper_population' in globals(): # if paper_population exists
            pass # do nothing 
        
        else: # if paper_population does not exist
            paper_population=[] # create an empty list
            
    return paper_population


def check_related_articles(eid_list):
    
    global publications_with_errors

     # Selected keywords
    keywords=['hosting capacity','Hosting capacity','hosting capacities', 'Hosting capacities']
    
    # Prepare a zero vector (used later as one of the function output)
    decision_vector=np.zeros(len(eid_list)) # 0 - drop the paper ; 1 - keep the paper 

    # Checking the papers eids from the given eid_list
    for idx,paper_eid in enumerate(eid_list): # for each paper eid

        # Checking the abstract by keywords 
        try:
            # Extract data on Abstact of given paper
            ss = AbstractRetrieval(paper_eid, view='FULL') 
                
            # Checking the matching of keywords 
            # in abstract
            if hasattr(ss, 'abstract'):
                paper_abstract=ss.abstract # extract a paper abstract 
                
                if any(keyword in paper_abstract for keyword in keywords):
                    decision_vector[idx]=1 # add 1 into a zero vector
            
            if decision_vector[idx]!=1:
                # in keywords
                if hasattr(ss, 'authkeywords'):
                    paper_keywords=ss.authkeywords # extract author keywords 
                    
                    if paper_keywords is not None and any(keyword in paper_keywords for keyword in keywords):
                        decision_vector[idx]=1 # add 1 into a zero vector

            if decision_vector[idx]!=1:
                # in title 
                if hasattr(ss, 'title'):
                    paper_title=ss.title # extract a paper's title 
                    if any(keyword in paper_title for keyword in keywords):
                        decision_vector[idx]=1 # add 1 into a zero vector
                        
        except Exception as exception: # if any error with AbstractRetrieval occured

            if "publications_with_errors" in globals(): # if variable is already created 
                print(type(exception).__name__,'with ',paper_eid)
                publications_with_errors.append([type(exception).__name__,'with ',paper_eid])
            else: # if variable is not created yet
                print(type(exception).__name__,'with ',paper_eid)
                # create a list "publications_with_errors" and append
                publications_with_errors=[] 
                publications_with_errors.append([type(exception).__name__,'with ',paper_eid])
            pass
        
    # -------------------------------------------------------------------------------
    # Deciding on the papers: drop or keep 
    if np.sum(decision_vector)>0: # if there is at least one '1'
        
        # Find the indexes of ones in a decision_vector
        ones_indexes = [i for i,val in enumerate(decision_vector) if val==1]
        
        # Create an empty list
        intermediate_list=[]
        
        # Extract the eids which corresponds to the status 1 (relevant publication)
        for i in range(len(ones_indexes)):
            index=ones_indexes[i]
            intermediate_list.append(eid_list[index])
            
        eid_list=intermediate_list
        
    else: # if all values are zero in ones_indexes 
        eid_list=0
        
    return eid_list       
   
   
   
# Function to retrive the metadata for each paper from scopus populations
def retrieve_paper_data():
    """
    This function retrieves the metadata for each paper from scopus populations 
    
    """
    global  paper_population
    
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

def ploting_connection_graph():
    """
    This function plots a population graph 
    """
    import networkx as nx
    import matplotlib.pyplot as plt
    from bokeh.io import output_notebook, show, save
    from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
    from bokeh.plotting import figure
    from bokeh.plotting import from_networkx
    
    global paper_population
    
    # Create column names 
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
        eid_list_citing=get_EIDS(citing_papers)
        eid_list_cited=get_EIDS(cited_papers)        
        
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

    show(plot)
    # # Set node sizes
    # node_sizes = [100 if type(entry) !=int else 1 for entry in list(G.nodes())]
    # node_colors = ['red' if type(entry) !=int else 'blue' for entry in list(G.nodes())]        

    # # Draw graph
    # plt.figure(figsize=(17,10))
    # nx.draw(G, with_labels=False,node_size=node_sizes, node_color=node_colors)
    # plt.show()

    return graph_df

def calculate_connections_number(graph_df):
    """
    This function calculates the number of connections per each paper in a population
    """

    # Calculate the count  
    df=graph_df.groupby(['primary_list','secondary_list']).size().reset_index().rename(columns={0:'count'})

    # Find a number of connections
    connections=df.groupby('primary_list').sum()

    # Extract metadata for population  
    population_data=retrieve_paper_data()

    connections = pd.merge(population_data, connections,left_on='eid', right_on='primary_list')


    return df,connections
      
#------------------------------Case study-------------------------------

#--------------First iteration: Create initial layers------------

# Start with eid of one reference paper 
reference_paper_eid="2-s2.0-85085924004"

# Get citing papers for given reference paper
citing_papers=get_citing_papers(reference_paper_eid)

# Get cited papers for given reference paper
cited_papers=get_cited_papers(reference_paper_eid)

# Get EID of these citing and cited papers 
eid_list_citing=get_EIDS(citing_papers)
eid_list_cited=get_EIDS(cited_papers)

# Investigate given papers using 2 layers-ahead  
eid_list_citing=check_related_articles(eid_list_citing)
eid_list_cited=check_related_articles(eid_list_cited)

get_paper_population(eid_list_citing)
get_paper_population(eid_list_cited)

#----------------------------Second iteration: Selecting the paths----------------------------



#----------------------------Third iteration: Growing the population----------------------------

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
        
        if len(eid_list_citing)>0:
            
            # Extract only relevant papers
            eid_list_citing=check_related_articles(eid_list_citing)
            
            # Add cited papers into population
            get_paper_population(eid_list_citing)

        if len(eid_list_cited)>0:
            
            # Extract only relevant papers
            eid_list_cited=check_related_articles(eid_list_cited)
            
            # Add cited papers into population
            get_paper_population(eid_list_cited)
           
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
                
                # Extract only relevant papers
                eid_list_citing=check_related_articles(eid_list_citing)
                
                # Add citing papers into population
                get_paper_population(eid_list_citing)    
            else:
                pass
                    
        if no_errors_with_cited_papers==1:
            
            if cited_papers!=0:
                eid_list_cited=get_EIDS(cited_papers)

                # Extract only relevant papers
                eid_list_cited=check_related_articles(eid_list_cited)
                
                # Add cited papers into population
                get_paper_population(eid_list_cited)        
            else:
                pass
        else:
            print('Error problem')


    print('Population:', len(paper_population))

    # increase the count 
    number_analysed_papers+=1
    print('Papers analised: ',number_analysed_papers,'or ',round(number_analysed_papers/len(paper_population)*100,2),' %')

    # Add to the list of analysed papers
    analysed_papers.append(reference_paper_eid)

    # Update non-analysed papers with consideration of newly populated papers
    non_analysed_papers = list(set(paper_population).difference(analysed_papers))
    print('Non_analysed:', len(non_analysed_papers))
    print(' ')
    #time.sleep(2)    # Pause 3 seconds
        
#----------------------------Fourth iteration: Processing the results----------------------------

# Retreive a metadata from a population 
df=retrieve_paper_data()

# Sort papers by number of citations 
df=df.sort_values(by='citedby_count', ascending=False)

# Save to excel file
df.to_excel('outputs.xlsx',sheet_name='Paper population',index=False)

# Ploting the graph of paper population 
graph_df=ploting_connection_graph()

# Calculate the number of connections 
df_connections,connections=calculate_connections_number(graph_df)    
connections.to_excel('connections.xlsx')
print(connections)
print('<<<<Execution is finalized>>>>')









# Function to restore the citations 

# Function to retrieve the unique keywords from a populatiion 

        

        
        
        ## Checking the path feasibility by keywords 
        # 1. Analyze a first layer in for cycle: green or red 
        # 2. Select only papers with green light 
        # 3. Analyze a second layer for papers with green light
        # 4. Select pathes green-green
        # 5. Save selected papers from both layers into population
        
        ## Take a non-analysed paper from population and repeat the procedure 
        
        
        ## Plot the graph 
