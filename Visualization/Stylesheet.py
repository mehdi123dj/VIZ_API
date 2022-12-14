

class Stylesheet():
    
    r"""
    A class that is managing the contents in the stylesheet dictionnary that will be used in the cytosacpe component
        
    """
    
    
    def __init__(self):
        self.stylesheet = []
        self.default_stylesheet = []

    def stylesheet_default(self, exterior_stylesheet):
        r"""
            Creation of the default stylesheet when none interaction have been made with the graph, clicked on a node or an edge
            
            Args:
                exterior_stylesheet (dictionnary): Stylesheet that comes from the ColorMap class instance to well
                attributes the colors to every node and edge

            Returns:
                Does not return anything but save the default stylesheet in self.default_stylesheet

            """
        width_default_edges = 13
        stylesheet = [
            {
                "selector": 'node',
                'style': {
                    "opacity": 0.9,
                    'width': 'data(size)',
                    'height': 'data(size)',
                    'z-index': 5
                }
            },
            {
                "selector": 'edge',
                'style': {
                    "curve-style": "bezier",
                    "width": width_default_edges,
                    "opacity": 0.25,
                    'z-index': 3
                }
            },
            {
                'selector': 'edge:selected',
                "style": {
                    "curve-style": "bezier",
                    'width': width_default_edges*3,
                    "opacity": 1,
                }
            }
        ]

        self.default_stylesheet = stylesheet+exterior_stylesheet

    def stylesheet_on_click(self, node, switch):
        r"""
            Creation of the stylesheet when clicked on a node to highlight the selected node and its neighborhood
            
            Args:
                node (int): 
                    Triggered if we press on a node in the cytoscape view
            
                switch (dictionnary):
                    Switch button use to take into account or not the direction of the edges

            Returns:
                Does not return anything but save the stylesheet in self.stylesheet

            """
        follower_color = '#0074D9'
        following_color = '#FF4136'

        stylesheet = [{
            "selector": 'node',
            'style': {
                'opacity': 0.6,
                'width': 'data(size)',
                'height': 'data(size)',
            }
        }, {
            'selector': 'edge',
            'style': {
                'opacity': 0.4,
                "width": 4,
                "curve-style": "bezier",
            }
        }, {
            "selector": 'node[id = "{}"]'.format(node['data']['id']),
            "style": {
                'background-color': '#B10DC9',
                "border-color": "purple",
                "border-width": 2,
                "border-opacity": 1,
                "opacity": 1,

                # "label": "data(label)",
                'width': 'data(size)',
                'height': 'data(size)',
                "color": "#B10DC9",
                "text-opacity": 1,
                "font-size": 12,
                'z-index': 9999
            }
        }]

        if switch:
            for edge in node['edgesData']:
                if edge['source'] == node['data']['id']:
                    stylesheet.append({
                        "selector": 'node[id = "{}"]'.format(edge['target']),
                        "style": {
                            'background-color': following_color,
                            'opacity': 1,
                            'width': 'data(size)',
                            'height': 'data(size)',
                        }
                    })
                    stylesheet.append({
                        "selector": 'edge[perso= "{}"]'.format(edge['perso']),
                        "style": {
                            "mid-target-arrow-color": following_color,
                            "mid-target-arrow-shape": "vee",
                            "line-color": following_color,
                            'width': 15,
                            'opacity': 0.9,
                            'z-index': 5000
                        }
                    })

                if edge['target'] == node['data']['id']:
                    stylesheet.append({
                        "selector": 'node[id = "{}"]'.format(edge['source']),
                        "style": {
                            'background-color': follower_color,
                            'opacity': 1,
                            'z-index': 9999,
                            'width': 'data(size)',
                            'height': 'data(size)',
                        }
                    })
                    stylesheet.append({
                        "selector": 'edge[perso= "{}"]'.format(edge['perso']),
                        "style": {
                            "mid-target-arrow-color": follower_color,
                            "mid-target-arrow-shape": "vee",
                            "line-color": follower_color,
                            'width': 15,
                            'opacity': 0.9,
                            'z-index': 5000
                        }
                    })
        else:
            for edge in node['edgesData']:
                if edge['source'] == node['data']['id']:
                    stylesheet.append({
                        "selector": 'node[id = "{}"]'.format(edge['target']),
                        "style": {
                            'background-color': following_color,
                            'opacity': 1,
                            'width': 'data(size)',
                            'height': 'data(size)',
                        }
                    })
                    stylesheet.append({
                        "selector": 'edge[perso= "{}"]'.format(edge['perso']),
                        "style": {
                            "mid-target-arrow-color": following_color,
                            "mid-target-arrow-shape": "vee",
                            "line-color": following_color,
                            'width': 15,
                            'opacity': 0.9,
                            'z-index': 5000
                        }
                    })

                if edge['target'] == node['data']['id']:
                    stylesheet.append({
                        "selector": 'node[id = "{}"]'.format(edge['source']),
                        "style": {
                            'background-color': following_color,
                            'opacity': 1,
                            'z-index': 9999,
                            'width': 'data(size)',
                            'height': 'data(size)',
                        }
                    })
                    stylesheet.append({
                        "selector": 'edge[perso= "{}"]'.format(edge['perso']),
                        "style": {
                            "mid-target-arrow-color": following_color,
                            "mid-target-arrow-shape": "vee",
                            "line-color": following_color,
                            'width': 15,
                            'opacity': 0.9,
                            'z-index': 5000
                        }
                    })

        self.stylesheet = stylesheet
