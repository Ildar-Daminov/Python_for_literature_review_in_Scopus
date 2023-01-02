import numpy as np
import pandas as pd
from source_code import functions

class research_topic():
    """
    This class allows creating the object of user-defined topic and
    extract the relevant papers (thanks to its functions) from Scopus  
    
    """
    # Function for creating the object of research topic 
    def __init__(self,name,reference_paper_eid,keywords):
        """
        This function is run automatically when a new instance of 
        research topic is created. This allows us to create an object
        
        INPUTS:
        - self: convention needed to create a function for the class
        - name: a nae of research topic (any name defined by user)
        - reference_paper_eid: a paper's eid (index) in Scopus e.g. '2-s2.0-85085924004'
                               a reference_paper_eid is defined in the main.py
        - keywords: list of keywords defined by user in the main.py
        
        OUTPUTS:
        - None: __init__ has a None output. But note that the object 
                is created as an output with following data (see below) 
        
        """
        # A research topic is created for following data
        self.name=name # name of the research topic (any  user-defined string)
        self.reference_paper_eid=reference_paper_eid # e.g. 2-s2.0-85085924004
        self.keywords=keywords              # list of keywords 
        self.paper_population=[]            # empty list (to be filled later)
        self.publications_outside_scopus=[] # empty list (to be filled later)
        self.publications_with_errors=[]    # empty list (to be filled later)
        self.number_analyzed_papers=0    # empty list (to be filled later)

    # Function for conducting the anlysis
    def analyze(self):
        """
        This function does the principal analysis decsribed in the
        documentation.

        
        INPUT:
        self: an empty object of research topic, created earlier in in the __init__  
        
        OUTPUT:
        self: a filled object of research topic
                                    + 
        Some excel files:
        - Figure.html : an interactive netwrok graph repersenting the paper population
        - Topic_name_outputs.xlsx: a lsit of papers corresponding to a research topic                               
        - graph_df.xlsx : a network graph in excel format.
        
        Note that one of columns in graph_df is named as 'Direction' having 1 or 2 values
        1 means the paper from primary list cites the paper from secondary list
        2 means that the paper from SECONDARY list cites the paper from primary list 
        
        """
        
        # ----------------------- First stage ------------------------
        # ----------------Creating the first population---------------

        print('<<< First stage: processing the reference eid >>>')

        # Get citing papers for given reference paper
        citing_papers=functions.get_citing_papers(self.reference_paper_eid)

        # Get cited papers for given reference paper
        cited_papers=functions.get_cited_papers(self.reference_paper_eid)
        
        # Get EID of these citing and cited papers 
        eid_list_citing=functions.get_EIDS(citing_papers,self.publications_outside_scopus)
        eid_list_cited=functions.get_EIDS(cited_papers,self.publications_outside_scopus)

        # Keep papers corresponding to our research topic
        eid_list_citing=functions.check_related_articles(eid_list_citing,self.keywords,self.publications_with_errors)
        eid_list_cited=functions.check_related_articles(eid_list_cited,self.keywords,self.publications_with_errors)

        # Add these papers into the paper population. For the first time population is created 
        functions.get_paper_population(eid_list_citing,self.paper_population)
        functions.get_paper_population(eid_list_cited,self.paper_population)
        
        
        # --------------------- Second stage ------------------------
        # --------------Processing each paper in population-----------

        # Assume that  papers were not analyzed yet 
        number_analyzed_papers=0

        # Create a list of non-analyzed and analyzed papers 
        non_analyzed_papers=self.paper_population
        analyzed_papers=[] # empty list
        errors_count=0 
        
        print('<<< Second stage: processing  each paper in population >>>')
        while number_analyzed_papers!=len(self.paper_population): # while we do not analyze every paper in population
            
            # Refresh status of errors 
            no_errors_with_citing_papers=1 # 1 means true i.e. no erros exist
            no_errors_with_cited_papers=1 # 1 means true i.e. no erros exist
            
            if number_analyzed_papers==0: # first iteration
                
                # Take a first paper from population
                reference_paper_eid=self.paper_population[0] 
                
                # Get citing papers for given reference paper
                citing_papers=functions.get_citing_papers(reference_paper_eid)

                # Get cited papers for given reference paper
                cited_papers=functions.get_cited_papers(reference_paper_eid)

                # Get EID of these citing and cited papers 
                eid_list_citing=functions.get_EIDS(citing_papers,self.publications_outside_scopus)
                eid_list_cited=functions.get_EIDS(cited_papers,self.publications_outside_scopus)
                
                if len(eid_list_citing)>0:
                    
                    # Extract only relevant papers
                    eid_list_citing=functions.check_related_articles(eid_list_citing,self.keywords,self.publications_with_errors)
                    
                    # Add cited papers into population
                    functions.get_paper_population(eid_list_citing,self.paper_population)

                if len(eid_list_cited)>0:
                    
                    # Extract only relevant papers
                    eid_list_cited=functions.check_related_articles(eid_list_cited,self.keywords,self.publications_with_errors)
                    
                    # Add cited papers into population
                    functions.get_paper_population(eid_list_cited,self.paper_population)
                
                print('Population:', len(self.paper_population))

                # increase the count of analyzed papers  
                number_analyzed_papers+=1
                print('Papers analyzed: ',number_analyzed_papers)

                analyzed_papers.append(reference_paper_eid)
                
                # Remove analyzed paper from non_analyzed_papers 
                non_analyzed_papers.remove(reference_paper_eid)
                print('Non_analyzed:', len(non_analyzed_papers))
                print(' ') # empty line in a command window
                
            else: # number_analyzed_papers!=0 i.e. >0
                
                # Take a first paper from non_analyzed_papers
                reference_paper_eid=non_analyzed_papers[0] 
                
                try: 
                    # Get citing papers for given reference paper
                    citing_papers=functions.get_citing_papers(reference_paper_eid)
                except:
                    no_errors_with_citing_papers=0
                    print('Error with citing papers')
                    errors_count+=1
                try: 
                    # Get cited papers for given reference paper
                    cited_papers=functions.get_cited_papers(reference_paper_eid)
                except:
                    no_errors_with_cited_papers=0
                    print('Error with cited papers')
                    errors_count+=1
                    
                if no_errors_with_citing_papers==1:
                    
                    if citing_papers!=0:
                        # Get EID of these citing and cited papers 
                        eid_list_citing=functions.get_EIDS(citing_papers,self.publications_outside_scopus)
                        
                        # Extract only relevant papers
                        eid_list_citing=functions.check_related_articles(eid_list_citing,self.keywords,self.publications_with_errors)
                        
                        # Add citing papers into population
                        functions.get_paper_population(eid_list_citing,self.paper_population)    
                    else:
                        pass
                            
                if no_errors_with_cited_papers==1:
                    
                    if cited_papers!=0:
                        eid_list_cited=functions.get_EIDS(cited_papers,self.publications_outside_scopus)

                        # Extract only relevant papers
                        eid_list_cited=functions.check_related_articles(eid_list_cited,self.keywords,self.publications_with_errors)
                        
                        # Add cited papers into population
                        functions.get_paper_population(eid_list_cited,self.paper_population)        
                    else:
                        pass
                else:
                    print('Error problem')


            print('Population:', len(self.paper_population))

            # increase the count 
            number_analyzed_papers+=1
            print('Papers analyzed: ',number_analyzed_papers,'or ',round(number_analyzed_papers/len(self.paper_population)*100,2),' %')

            # Add to the list of analyzed papers
            analyzed_papers.append(reference_paper_eid)

            # Update non-analyzed papers with consideration of newly populated papers
            non_analyzed_papers = list(set(self.paper_population).difference(analyzed_papers))
            print('Non_analyzed:', len(non_analyzed_papers))
            print(' ')
            
        # --------------------------  Third stage ----------------------------
        # --------------------- Postprocessing of results --------------------
        
        print('<<< Third stage: postprocessing of results >>>')
        
        # Ploting the graph of paper population (with saving as excel)
        graph_df=functions.creating_connection_graph(self.name,self.paper_population,self.publications_outside_scopus)

        # Calculate the number of connections 
        connections=functions.calculate_connections_number(graph_df,self.paper_population)    
        
        # Save an output
        connections.to_excel(self.name+'_'+'outputs.xlsx')
        
        # Print that the analysis is finsihed
        print('<<<< Analysis is finished >>>>')

        return self
    
    def plot_network_graph(self):
        """
        This function plots the interactive graph showing how publication are interrelated

        INPUT:
        self: an filled object of research topic after the function analyze() was used
        
        OUTPUT:
        - Figure.html : an interactive netwrok graph repersenting the paper population

        """        
        
        # import neccesary packages 
        from pathlib import Path
        import networkx as nx
        from bokeh.io import show
        from bokeh.models import Range1d, Circle, MultiLine
        from bokeh.plotting import figure
        from bokeh.plotting import from_networkx
        
        if self.paper_population: # if this list is NOT empty then plot the figure 
            
            # Find the filename graph_df.xlsx
            filename=self.name+'_'+'graph_df.xlsx'
            
            # Check the path of file in current directory
            path=Path(filename)
            
            if path.is_file(): # if file exists
                
                # Read the graph_df.xlsx
                graph_df=pd.read_excel(filename)
                
                # Create a G graph between restaurants and customers
                G=nx.from_pandas_edgelist(graph_df,
                                        target='primary_list',
                                        source='secondary_list') # 
                
                #Choose a title
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
                
            else: # if file "graph_df" does not exist
                print(f'The file {filename} does not exist')  

        else: # if the list is empty
            print('The paper population is empty. Use analyze() first to get a paper population')
            pass # do nothing
            
