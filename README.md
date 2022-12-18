![Python_for_literature_review](https://user-images.githubusercontent.com/73365375/208320965-24fe4441-5ca9-4749-bb73-f17045f511e1.jpg)


This python code reconstructs the graph of all related papers (indexed in scopus)for any given article. 

![text](figures/graph.png)
<sup>Fig. 1 The graph representing all the publications on the HC topic (the interactive version is [here](figures/)). A blue dot represents a publication and the black link is its connection with the other publication that cites it or where it is cited.</sup>



## Understanding the main logic of code: 
![Main_idea](https://user-images.githubusercontent.com/73365375/208321059-6da612a4-e411-486d-a25a-d805fa9372ae.jpg)




## Before getting started:

### Install the pybliometrics package extracting data from Scopus
Refer to the site for [pybliometrics instructions](https://pybliometrics.readthedocs.io/en/stable/)

### Get API keys for accessing Scopus via Elsevier API
1. To access Scopus via its API, you need two things. First, your institution needs to be a subscriber (not only to Scopus, but really to its API); second, you need to register API keys at https://dev.elsevier.com/apikey/manage. For each profile, you may register 10 keys.

2. Add your API keys into config.ini (see [instructions](https://pybliometrics.readthedocs.io/en/stable/configuration.html#))

3. It may be neccesary to change apikey from config.json (see main folder). Note that a key allows for 5,000 retrieval requests, or 20,000 search requests via the Scopus Search API per week. Without changing the apikey, it may be quickly depleted 

### Other python packages 
Install other python packages, needed to run a code; 
* [networkx](https://networkx.org/documentation/stable/install.html) for working with network graph
* [bokeh.io](https://docs.bokeh.org/en/latest/docs/first_steps/installation.html) for creating the interactive graphs 


## Get Started:
In alpha  version of code, run Hosting_capacity.py to get the results for the subject with predefined keywords and reference paper (doi: 10.3390/en13112758).
If you would like to use a code for other topic. Please change a reference paper eid,and keywords inside of Hosting_capacity.py.  

Later the code will be rewritten in OOP version for its more easy use 
