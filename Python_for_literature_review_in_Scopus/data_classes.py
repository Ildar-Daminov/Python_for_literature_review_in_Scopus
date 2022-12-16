import numpy as np
import pandas as pd
from Python_for_literature_review_in_Scopus import functions

class research_topic():
    
    def __init__(self,name,reference_paper_eid,keywords):
        ""
        
        ""
        self.name=name # name of the topic
        self.reference_paper_eid=reference_paper_eid # e.g. 2-s2.0-85085924004
        self.keywords=keywords              # lsit of keywords 
        self.paper_population=[]            # empty list
        self.publications_outside_scopus=[] # empty list
        self.publications_with_errors=[]    # empty list
        self.number_analysed_papers=0    # empty list
   

        return self
    
    def analyse(self):
        
        # ---------------------First iteration------------------------

        # Get citing papers for given reference paper
        citing_papers=functions.get_citing_papers(self.reference_paper_eid)

        # Get cited papers for given reference paper
        cited_papers=functions.get_cited_papers(self.reference_paper_eid)

        # Get EID of these citing and cited papers 
        eid_list_citing=functions.get_EIDS(citing_papers)
        eid_list_cited=functions.get_EIDS(cited_papers)

        # Investigate given papers using 2 layers-ahead  
        eid_list_citing=functions.check_related_articles(eid_list_citing,self.keywords)
        eid_list_cited=functions.check_related_articles(eid_list_cited,self.keywords)

        # Get the paper population
        functions.get_paper_population(eid_list_citing)
        functions.get_paper_population(eid_list_cited)
        
        self.number_analysed_papers=0
        
        
         # ---------------------Second iteration------------------------

        # Assume that  papers were not analyzed yet 
        number_analysed_papers=0

        # Create a list of non-analysed and analysed papers 
        non_analysed_papers=self.paper_population
        analysed_papers=[] # empty list
        errors_count=0 

        while number_analysed_papers!=len(self.paper_population): # while we do not analyze everything 
            
            # Refresh status of errors 
            no_errors_with_citing_papers=1 # 1 means true i.e. no erros exist
            no_errors_with_cited_papers=1 # 1 means true i.e. no erros exist
            
            if number_analysed_papers==0: # first iteration
                
                # Take a first paper from population
                reference_paper_eid=self.paper_population[0] 
                
                # Get citing papers for given reference paper
                citing_papers=functions.get_citing_papers(reference_paper_eid)

                # Get cited papers for given reference paper
                cited_papers=functions.get_cited_papers(reference_paper_eid)

                # Get EID of these citing and cited papers 
                eid_list_citing=functions.get_EIDS(citing_papers)
                eid_list_cited=functions.get_EIDS(cited_papers)
                
                if len(eid_list_citing)>0:
                    
                    # Extract only relevant papers
                    eid_list_citing=functions.check_related_articles(eid_list_citing,keywords)
                    
                    # Add cited papers into population
                    functions.get_paper_population(eid_list_citing)

                if len(eid_list_cited)>0:
                    
                    # Extract only relevant papers
                    eid_list_cited=functions.check_related_articles(eid_list_cited,keywords)
                    
                    # Add cited papers into population
                    functions.get_paper_population(eid_list_cited)
                
                print('Population:', len(self.paper_population))

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
                        eid_list_citing=functions.get_EIDS(citing_papers)
                        
                        # Extract only relevant papers
                        eid_list_citing=functions.check_related_articles(eid_list_citing,keywords)
                        
                        # Add citing papers into population
                        functions.get_paper_population(eid_list_citing)    
                    else:
                        pass
                            
                if no_errors_with_cited_papers==1:
                    
                    if cited_papers!=0:
                        eid_list_cited=functions.get_EIDS(cited_papers)

                        # Extract only relevant papers
                        eid_list_cited=functions.check_related_articles(eid_list_cited,keywords)
                        
                        # Add cited papers into population
                        functions.get_paper_population(eid_list_cited)        
                    else:
                        pass
                else:
                    print('Error problem')


            print('Population:', len(self.paper_population))

            # increase the count 
            number_analysed_papers+=1
            print('Papers analised: ',number_analysed_papers,'or ',round(number_analysed_papers/len(self.paper_population)*100,2),' %')

            # Add to the list of analysed papers
            analysed_papers.append(reference_paper_eid)

            # Update non-analysed papers with consideration of newly populated papers
            non_analysed_papers = list(set(self.paper_population).difference(analysed_papers))
            print('Non_analysed:', len(non_analysed_papers))
            print(' ')
            
            # ---------------------Third iteration------------------------
            # Retreive a metadata from a population 
            df=functions.retrieve_paper_data()

            # Sort papers by number of citations 
            df=df.sort_values(by='citedby_count', ascending=False)

            # Save to excel file
            df.to_excel('outputs.xlsx',sheet_name='Paper population',index=False)

            # Ploting the graph of paper population 
            graph_df=functions.ploting_connection_graph()

            # Calculate the number of connections 
            df_connections,connections=functions.calculate_connections_number(graph_df)    
            connections.to_excel('connections.xlsx')
            print(connections)
            print('<<<<Execution is finalized>>>>')
            
            return self