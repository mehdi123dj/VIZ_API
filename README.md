# Visualization
* Home page after loading of data without any class defined in dataset (no supervised learning button possible)
![Semantic description of image](/ScreenShot/Page_accueil_files_loaded_with_features_and_no_class.jpg )

* Home page after loading of data and activation of learn graph node classification option
![Semantic description of image](/ScreenShot/Page_accueil_files_loaded_learn_node_classification_activated.jpg )

* Visualization page after loading of data
![Semantic description of image](/ScreenShot/Visualisation.jpg )

* Visualization page after loading of data with clicked node
![Semantic description of image](/ScreenShot/Visualisation_clicked_node.jpg )

Here we can see that the CytoView is delimited by the red rectangle excepted the two buttons *Reset view* and *Reset stylesheet* 

Also the ControlPanel is delimited by the blue rectangle.

# Instalation 

## Cloning git
Download the repository and store it in a directory, you can use to clone with https
```
git clone https://gitlab.com/d7036/visualization.git 

```

to clone with ssh:
```
git clone git@gitlab.com:d7036/visualization.git 
```


## Docker
First install docker https://docs.docker.com/get-docker/ by following the step from the official site. Then launch the docker desktop app. Under linux you can also type :
```
 sudo systemctl start docker
```
Once docker daemon has been launched depending on your configuration then navigate to the corresponding directory and launch the following command :

With gpu
```
  docker build -t visualization-cuda -f dockerfileCuda .
  docker run -p 8050:8050 --rm visualization-cuda
```
Without gpu
```
  docker build -t visualization-no-cuda -f dockerfileNoCuda .
  docker run -p 8050:8050 --rm visualization-no-cuda
```
Once the steps for dockers have been correctly pursued connect to http://localhost:8050/ to use the SaaS app
## Possible change
### In dockerfiles
To switch from a local use of the app using only flask and dash we could use a gunicorn server by uncommenting the last line and commenting the previous one. 
### Change in app behaviour
We could manually changed one file to be able to control wheel sensitivity the process is described there (https://github.com/plotly/dash-cytoscape/compare/wheel-sensitivity-feature)
Then in CreateElements.py file uncomment wheelSensitivity

# Used package and dependencies
To create the app I used the following packages (see evironment yml files):
* dash : To build a full-stack web app with interactive data visualization. (https://github.com/plotly/dash)
* dash-bootstrap-components : library of Bootstrap components for Plotly Dash (https://github.com/facultyai/dash-bootstrap-components)
* dash_cytoscape : graph visualization component for creating easily customizable, high-performance, interactive, and web-based networks (https://github.com/plotly/dash-cytoscape)
* dash-daq : framework that provides pure Python abstraction around HTML, CSS, and JavaScript (https://github.com/plotly/dash-daq)
* pyg : Pytorch geometric library use for machine learning tasks on graphs (https://github.com/pyg-team/pytorch_geometric). Need the torchvision and torchaudio packages.
* gunicorn : Python WSGI (Web Server Gateway Interface) HTTP Server for UNIX (https://github.com/benoitc/gunicorn). I only used it when the line is decommented in the docker file for production server purposes.

# File Tree Structure

    ????????? Visualization                    
    ???   ????????? ColorMap.py             # Part repsonsible to create adequate color mapping for nodes and edges legend
    ???   ????????? ControlPanel.py         # Part design to control the creation of the legend and export navigation bar with cytoscape layout
    ???   ????????? CreateElements.py       # Create the different pages (home and visualization) 
    ???   ????????? CytoView.py             # Create and update the graph interactive part
    ???   ????????? NodeLayout.py           # Define the position and size of nodes reagrding to their degree and initial given position
    ???   ????????? Stylesheet.py           # Register all the possible stylesheet for nodes and edges regarding their state
    ???   ????????? Visualization.py        # Define the server and theme use for all the pages
    ???   ????????? FileConvert.py          # Convert the csv/xls or gml file into dataframe and dcc.store objects
    ???   ????????? ML_scripts
    ???   ???   ????????? MachineLearning.py  # Create a class that is launching the creation of the dataset, train the model and give the results on test set for the graph to be shown properly
    ???   ???   ????????? my_dataset.py       # Creation of a pytorch geometric dataset from the data saved in dcc.Store objects
    ???   ???   ????????? Train_edge_prediction_supervised.py             
    ???   ???   ????????? model_edge_prediction_supervised.py            
    ???   ???   ????????? Train_node_classification_deep.py             
    ???   ???   ????????? model_node_classification_deep.py          
    ???   ???   ????????? Train_node_classification_unsupervised.py             
    ???   ???   ????????? model_node_classification_unsupervised.py          
    ???   ????????? Config
    ???   ???   ????????? ConfigExplicit.txt          # Config with explicit ref to weblinks
    ???   ???   ????????? Config.yml
    ???   ????????? assets
    ???   ???   ????????? favicon.ico       
    ???   ???   ????????? reset.css 
    ????????? Dockerfile                 
    ????????? Test_CSV.py                 # File able to create fake examples for testing
    ????????? README.md

## Files dependencies
```mermaid
  graph TD;
      Visualization.py---CreateElements.py;
      CreateElements.py---ControlPanel.py;
      CreateElements.py---ColorMap.py;
      CreateElements.py---CytoView.py;
      CreateElements.py---FileConvert.py;
      CreateElements.py---MachineLearning.py;
      MachineLearning.py---my_dataset.py;
      MachineLearning.py---Train_node_classification_unsupervised.py;
      MachineLearning.py---model_node_classification_unsupervised.py;
      MachineLearning.py---Train_node_classification_deep.py;
      MachineLearning.py---model_node_classification_deep.py;
      MachineLearning.py---Train_edge_prediction_supervised.py; 
      MachineLearning.py---model_edge_prediction_supervised.py;
      CytoView.py---Stylesheet.py;
      CytoView.py---NodeLayout.py;
```


# Input files format
They are as follow :

* **CSV and XLS files**, you will have to upload edges and nodes file simultaneously in the drop zone, otherwise will not work.

    * File for edges should have the same format of header as shown below (you could omit non compulsory columns) and registered as csv/xls. You are force to furnish values for the **source** and **target** you can also provide values for **class** and **data** but it is not mandatory and sparse information could be given. A solution could be to add nothing, just let it empty (as shown below).
    ```
    source,target,class,data
    34,4,professional,Knowing since : 3 years
    1,21,friend,Knowing since : 97 years
    20,12,friend,Knowing since : 9 years
    3,0,friend,Knowing since : 51 years
    6,38,family,Knowing since : 3 years
    45,4,professional,Knowing since : 7 years
    0,8,family,Knowing since : 3 years
    ```

    * File for nodes should have the same format of header as shown below (you could omit non compulsory columns) and registered as csv/xls.You are force to furnish values for the **id** you can also provide values for **positionX**,**positionY**,**feature**, **class** but you will have to furnish value for all rows!  **data** column is not mandatory and you can provide sparse information. <A solution could be to add nothing, just let it empty (as shown below).>
    ```
    id,positionX,positionY,class,data,feature
    0,59.17180618694536,22.11030522902449,teenager,"Name : ludivine, age : 65","[69.33928670214559, 75.45925097633007, 70.99528587804748]"
    1,-96.05151980887148,-70.4455325019663,teenager,"Name : fabrice, age : 78","[96.69387532958712, 69.9360406529872, 74.12491979334999]"
    2,33.53531243249327,5.4884938927682185,adult,"Name : fabrice, age : 34","[11.618561313551945, 14.80660556644035, 30.668334158786944]"
    3,-28.93342830907102,5.372990605701716,adult,"Name : matthieu, age : 34","[25.44111693575362, 2.1404425396293245, 19.5873407260785]"
    4,-14.80054648587111,-55.81053799438567,teenager,"Name : matthieu, age : 55","[82.0134713406511, 75.87393548272328, 91.15490976049222]"
    5,87.89876740468642,29.610566777499315,adult,"Name : henri, age : 65","[21.614522662913647, 15.749883206784437, 30.730064306816665]"
    6,-54.64595487735493,-17.741161229561484,child,"Name : pascale, age : 20","[46.63956809476848, 48.89752997060593, 49.8082400003897]"
    ```

* **GML Files**
  File should have the same form as shown below and registered as gml. You are force to furnish values for the **source** and **target** for the edges and **id** for the nodes. You can provide **positionX**,**positionY**,**features** but you will have to furnish for all rows! For **class** and **data** sparse information could be given, you will have to add **'NaN'** when no information is given (as shown below).
    ```
  graph [
    multigraph 1
      node [
        id 0
        label "0"
        positionX 59.17180618694536
        positionY 22.11030522902449
        class "teenager"
        data "Name : ludivine, age : 65"
        feature "[69.33928670214559, 75.45925097633007, 70.99528587804748]"
      ]
      node [
        id 1
        label "1"
        positionX -96.05151980887148
        positionY -70.4455325019663
        class "nan"
        data "Name : fabrice, age : 78"
        feature "[96.69387532958712, 69.9360406529872, 74.12491979334999]"
      ]
      node [
        id 2
        label "2"
        positionX 33.53531243249327
        positionY 5.4884938927682185
        class "adult"
        data "Name : fabrice, age : 34"
        feature "[11.618561313551945, 14.80660556644035, 30.668334158786944]"
      ]
      node [
        id 3
        label "3"
        positionX -28.93342830907102
        positionY 5.372990605701716
        class "adult"
        data "nan"
        feature "[25.44111693575362, 2.1404425396293245, 19.5873407260785]"
      ]
      ...

      edge [
        source 0
        target 2
        key 0
        class "professional"
        data "Knowing since : 23 years"
      ]
      edge [
        source 0
        target 2
        key 1
        class "professional"
        data "Knowing since : 23 years"
      ]
      edge [
        source 0
        target 11
        key 0
        class "nan"
        data "Knowing since : 9 years"
      ]
      edge [
        source 0
        target 11
        key 1
        class "friend"
        data "Knowing since : 9 years"
      ]
      ...
    ]
    ```
## Usage of each keyword
* **Data** is a string that is only used to display information about the nodes or edges when clicked on.
* **Class** is a string and correspond to the class of each node/edge

* For an edge:
  * **Key** are auto generated in gml files and not used in my program
  * **Source** the beginning node of the link (this is important if you have a directed graph and want to activate the directed graph button that will allow you to see which is incoming our outcoming when clicked on one)
  * **Target** the end node of the link (this is important if you have a directed graph and want to activate the directed graph button that will allow you to see which is incoming our outcoming when clicked on one)
  
* For a node:
  * **id** is the identifier of the node
  * **positionX** is the position of the node along x axis
  * **positionY** is the position of the node along y axis
  * **feature** is a numeric vectorized representation of the attribute of the node pre computed by the user (this will be used to train the model, if the option is choosed, and make some prediction on node classification)

# Some known issues
* Because I use the dcc.store component and because this component store in browser memory the file that are saved it is impossible to store big files (>150 MB) furthemore it is quasi impossible to use the app on a mobile
* Use of gunicorn on server side is not guaranteed as long as gunicorn is using argparse to work and that agrparse is also use in our code to create our models. We so need to change in the code all the argparse fashion description to a simpler one without the ease of modification.
