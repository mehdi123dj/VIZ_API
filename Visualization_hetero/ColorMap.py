import pandas as pd
import matplotlib.colors as mcolors
import random as random

class ColorMap():
    r"""
    A class that is designed to attribute to every type of edge and node a color.
        self.stylesheet will be given to the cytoscape component
        self.node_legend will be given to the control panel to give the good color to the nodes buttons
        self.edge_legend will be given to the control panel to give the good color to the edges buttons
    
        
    """

    def __init__(self):
        self.edge_legend = []
        self.stylesheet = []
        self.node_legend = []

    def __call__(self, data_edges, data_nodes, classif=False):
        r"""
            Creation of the intial value for edge_mask and node_mask
            
            Args:                
                data_edges (list): A list of the following format, for each edge:
                    {'source': int, 'target': int, 'data': str, 'class': str}
                    
                    source: The id of the source node | Compulsory
                    
                    target: The id of the taget node | Compulsory
                    
                    data: String which gives some info about the edge | Optionnal, used when clicking on an edge to display info about it
                    
                    class: A string which gives the class of the given edge | Optionnal
                
                data_nodes (list): A list of the following format, for each node:
                    {'id': int, 'positionX': float, 'positionY': float, 'class': str, 'data': str, 'feature': list of float}
                
                    id: The local id of a node | Compulsory
                    
                    positionX, positionY : The position gave as input or compiled thanks to features | this is optional but nothing 
                        will appear if not provide.
                    
                    class: A string which gives the class of the given node | Optionnal
                    
                    feature: A list of float which give the embedding for a given node | Optionnal, not used for representation
                    
                    data: String which gives some info about the node | Optionnal, used when clicking on a node to display info about it
                    
                classif (bool): If a classification learning method has been used
                    
            Instance variables :
                self.node_legend (list): List of tuples [string of the hex color,string of the name of the class]
                
                self.edge_legend (list): List of tuples [string of the hex color,string of the name of the class]
                
                self.stylesheet (list): List of dictionnaries
                    {'selector': string, "style": dictionnary}
                    
                    selector: string of the selected class for the design style, for example '.family' if family is a class type
                        
                    style: Dictionnary
                        {"color": string, 'background-color': string}
                        
                        color: string of the hex color
                        
                        background-color: string of the hex color

            Returns:
                Do not have any return arguments

            """
        #color_list =  list(mcolors.CSS4_COLORS.values())
        color_list = ["navy","orange","limegreen","black","lightcoral","gold","teal","darkorchid",
                            "peru","olivedrab","dodgerlblue","pink","red","darkkhaki","turquoise","hotpink"]
        # Color Map for nodes the numbers on the left correspond to the number of class, on the right the associated colors
        #n_color = { i : list(random.sample(color_list, i)) for i in range(len(color_list))}
        n_color = { i :  color_list[:i] for i in range(len(color_list))}

        if classif == False:

            df_node = pd.DataFrame.from_dict(data_nodes)

            stylesheet = []
            legend = []
            self.edge_stylesheet_legend(data_edges)

            if 'class' in df_node:
                n_class = list(set(df_node['class']))
                n_class.sort()

                m = max(n_color)
                N = len(n_class)
                if N > m:
                    c = m
                else:
                    c = N
                for i in range(N):
                    if i < m and n_class[i] != 'nan':
                        stylesheet.append({
                            'selector': '.'+str(n_class[i]),
                            "style": {
                                "color": n_color[c][i],
                                'background-color': n_color[c][i],
                            }
                        })
                        legend.append([n_color[c][i], str(n_class[i])])
                    else:
                        legend.append(['#999999', str(n_class[i])])

            self.node_legend = legend
            self.stylesheet = self.stylesheet+stylesheet

        else:
            stylesheet = []
            legend = []
            df_node = pd.DataFrame.from_dict(data_nodes)

            self.edge_stylesheet_legend(data_edges)
            
            if 'class' in df_node:
                n_class = list(set(df_node['class']))
                n_real_class = [
                    elem for elem in n_class if "wrong" not in elem and "true" not in elem]
                n_predicted_class = [
                    elem for elem in n_class if "wrong" in elem or "true" in elem]
                n_real_class.sort()

                m = max(n_color)
                N = len(n_real_class)
                if N > m:
                    c = m
                else:
                    c = N
    
                for i in range(N):
                    if i < m and n_class[i] != 'nan':
                        stylesheet.append({
                            'selector': '.'+str(n_real_class[i]),
                            "style": {
                                "color": n_color[c][i],
                                'background-color': n_color[c][i],
                            }
                        })
                        legend.append([n_color[c][i], str(n_real_class[i])])
                    else:
                        legend.append(['#999999', str(n_real_class[i])])
    
                for j in range(len(n_predicted_class)):
                    if "wrong" in n_predicted_class[j] and n_predicted_class[j] != 'nan':
    
                        real_class, wrong_class = n_predicted_class[j].split("wrong_")[
                            1].split('_sep_')
    
                        index_real = n_real_class.index(real_class)
                        index_wrong = n_real_class.index(wrong_class)
                        stylesheet.append({
                            'selector': '.'+str(n_predicted_class[j]),
                            "style": {
                                'border-color': n_color[c][index_wrong],
                                'border-width': 'data(borderWidth)',
                                'background-color': n_color[c][index_real],
                            }
                        })
                        legend.append(
                            [n_color[c][index_real], str(n_predicted_class[j])])
                    elif "true" in n_predicted_class[j] and n_predicted_class[j] != 'nan':
                        index = n_real_class.index(
                            n_predicted_class[j].split("true_")[1])
                        stylesheet.append({
                            'selector': '.'+str(n_predicted_class[j]),
                            "style": {
                                'border-color': "#00FF00",
                                'border-width': 'data(borderWidth)',
                                'background-color': n_color[c][index],
                            }
                        })
                        legend.append(
                            [n_color[c][index], str(n_predicted_class[j])])
                    else:
                        legend.append(['#999999', str(n_predicted_class[j])])

            self.node_legend = legend
            self.stylesheet = self.stylesheet+stylesheet

    def edge_stylesheet_legend(self, data_edges):
        # Color Map for edges, the numbers on the left correspond to the number of class, on the right the associated colors
        e_color = {1: ['#000000'],
                   2: ['#9d9e6f', '#3c005d'],
                   3: ['#9d9e6f', '#b84e55', '#3c005d'],
                   4: ['#9d9e6f', '#af695e', '#8f3458', '#3c005d'],
                   5: ['#9d9e6f', '#ab7662', '#b84e55', '#7a2759', '#3c005d'],
                   6: ['#9d9e6f', '#a87e65', '#b35e5a', '#9f3e57', '#6e1f5a', '#3c005d'],
                   7: ['#9d9e6f', '#a68366', '#af695e', '#b84e55', '#8f3458', '#651a5b', '#3c005d'],
                   8: ['#9d9e6f', '#a58767', '#ac7060', '#b45959', '#a64356', '#832d59', '#5f165b', '#3c005d']
                   }

        e_class = pd.DataFrame.from_dict(data_edges)
        class_in_edge = "class" in e_class
        stylesheet = []
        legend = []
        if class_in_edge == True:
            e_class = list(set(e_class['class']))
            e_class.sort()
            m = max(e_color)
            N = len(e_class)
            if N > m:
                c = m
            else:
                c = N
            for i in range(N):
                if i < m and e_class[i] != 'nan':
                    stylesheet.append({
                        'selector': '.'+e_class[i],
                        "style": {
                            "line-color": e_color[c][i]
                        }
                    })
                    legend.append([e_color[c][i], e_class[i]])
                else:
                   legend.append(['#999999', e_class[i]])
        

        self.edge_legend = legend
        self.stylesheet = self.stylesheet+stylesheet
        
        