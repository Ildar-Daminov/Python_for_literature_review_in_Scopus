
## Documentation
[![Publish Docs](https://github.com/Ildar-Daminov/Python_for_literature_review_in_Scopus/actions/workflows/main.yml/badge.svg)](https://github.com/Ildar-Daminov/Python_for_literature_review_in_Scopus/actions/workflows/main.yml)
[![Check Documentation](docs/docs_badge.svg)](https://ildar-daminov.github.io/Python_for_literature_review_in_Scopus/)
[![DOI](https://zenodo.org/badge/563276645.svg)](https://zenodo.org/doi/10.5281/zenodo.12509942)


![Python_for_literature_review](https://user-images.githubusercontent.com/73365375/208320965-24fe4441-5ca9-4749-bb73-f17045f511e1.jpg)

## Understanding the main goal of code:

Main goal of this Python tool is generate a list of papers on a given topic available in Scopus with minimal input data.

Input:
- a name of a topic (for saving the results)
- a reference paper via Scopus eid 
- a list of your keywords for your topic of interest

Output: 
- Excel file <topic_name>_outputs.xlsx representing the list of papers in Scopus relevant to the  given topic
- Interactive graph showing the population of papers in html format

![Main_idea](https://user-images.githubusercontent.com/73365375/210181715-3f7a659e-c6c0-4b7e-a9a7-1c714d476af2.jpg)
<p align="center">Figure 1 - Input and outputs of Python module </p>


## Zoom of a population graph: 
Interactive graph (shown above and its increased view below) representing the population of papers on a given topic consists of blue dots and lines.
Each blue dot represents an article and lines between these dots represent their "connection". Here, a connection appears if one of the paper cites another one. 
![increased_view](https://user-images.githubusercontent.com/73365375/208321127-40c12253-d77d-4fd7-af8c-2f91d962877d.jpg)
<p align="center">Figure 2 - Interactive graph as the output of Python code and its increased view. Blue dots are articles on a given topic and lines are their connections </p>

## List of papers sorted in decsending order by the number of "connections"
After processing your query, Python generates a excel file with papers corresponding to your given topic sorted in descending order by the connection number (inside of population graph above)
![list](https://user-images.githubusercontent.com/73365375/210182373-5b234e04-1020-4d17-8c8f-2c8be3f59a2c.jpg)
<p align="center">Figure 3 - The example of excel file with the papers on the topic of hosting capacity </p>

Note: In additon to this excel file, Python generates npy files with the list of publications outside Scopus and papers with the error like 404 (such situation happens if paper in Scopus is not correctly filled e.g. empty title, authors names, abstract etc). These npy files can be further processed to doublecheck of relevant papers (this doublechecking is not included in current version of module yet)

## Python workflow: how does it work
![Python_workflow](https://user-images.githubusercontent.com/73365375/212465231-c2ff4e45-8f3d-4970-9d92-caaf4c928145.png)
<p align="center">Figure 4 - Workflow of how a paper population is reconstructed inside of the python tool </p>

# Before getting started:
First of all, you need to ensure an access to Scopus API via pybliometrics:

### Install the pybliometrics package 
Refer to the site for [pybliometrics instructions](https://pybliometrics.readthedocs.io/en/stable/)

### Get API keys for accessing Scopus via Elsevier API
1. To access Scopus via its API, you need to check two things. First, your university needs to be a subscriber (not only to Scopus, but also to its API); second, you need to register API keys at https://dev.elsevier.com/apikey/manage. For each profile, you may register 10 keys.

2. Add your API keys into config.ini (see [instructions](https://pybliometrics.readthedocs.io/en/stable/configuration.html#))

3. It may be neccesary to change apikey from config.json (see main folder). Note that a key allows for 5,000 retrieval requests, or 20,000 search requests via the Scopus Search API per week. Without changing the apikey, it may be quickly depleted 


# Get Started:
Using a poetry to install all neccesary packages and run a code  
1. Copy the reposioty to your computer and open it in your code software e.g. we use Visual Studio code
2. If you do not have a poetry on your computer you can use pip to install it. Just copy ```pip install poetry``` into your Python terminal
3. Once poetry is installed, just type  ```poetry install``` in Python terminal. This will create a virtual environment (folder .venv) where all neccesary packages will be installed. Note that the installation may take few minutes but once it will be finished you can be sure that everything would work as on our computer. 
4. During the installation accept that .venv will be installed in the same folder where you copied this Python module. Just click yes. 
5. Usually this is done automatically but check that Python interpeter (.venv':poetry) is selected. If you are in Visual Studio code just see the right bottom corner 
6. Open main_test.py in your editor and change the name, reference_paper_eid and select your keywords or run the example for the topic self-consumption (for the sake of example, we intentionally used a long keyword to reduce the number of corresponding papers and therefore get the results faster) . 
7. Before running the code, make sure that you are using the university network (directly or using VPN) to access the Scopus. Otherwise you will get the 401 error Unauthorized
8. Run ```main_test.py``` 
9. After the message <<<< Analysis is finished >>>>, check the resuts in the excel file <name>_outputs.xlsx and/or interactive graph

# Quick start:
Once you installed everything, you can simply change the input data (see Figure 5) and run your case studies. You may find the eid of your reference paper on its Scopus webpage (see example on Figure 6). 
![Python code](https://user-images.githubusercontent.com/73365375/211420715-443bd84d-c3ea-468c-965f-fb653241b07f.png)
<p align="center">Figure 5 - The only input data to be changed in order to run your case in main_test.py </p>

  ![Scopus eid](https://user-images.githubusercontent.com/73365375/212465607-e63baf1f-f51c-4d15-84e7-9dbfbce24346.png)
Figure 6 - The way how you may find the Scopus eid e.g. [2-s2.0-85101235827](https://www.scopus.com/record/display.uri?eid=2-s2.0-85101235827&origin=resultslist&sort=plf-f&src=s&sid=f716326e8305eae7e14603a5323abd22&sot=b&sdt=b&s=TITLE-ABS-KEY%28assessment+AND+dynamic+AND+transformer+AND+rating%29&sl=52&sessionSearchId=f716326e8305eae7e14603a5323abd22#abstract). 

