# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 10:29:21 2022

@author: remit
"""


class Stylesheet():
    def __init__(self):
        self.stylesheet=[]
        self.default_stylesheet=[]
        
    def stylesheet_default(self,exterior_stylesheet):
        stylesheet=[
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
                        "width":8,
                        "opacity": 0.4,
                        'z-index': 3
                    }
                },
                # {
                #     'selector': 'node:selected',
                #     "style": {
                #         "border-width": 10,
                #         "border-color": "black",
                #         "border-opacity": 1,
                #         "opacity": 1,
                #         "label": "data(label)",
                #         "color": "black",
                #         "font-size": 50,
                #         'z-index': 9999
                #     }
                # },
                {
                    'selector': 'edge:selected',
                    "style": {
                        'width':15,
                        "opacity": 1,
                    }
                }
        ]
        

        self.default_stylesheet=stylesheet+exterior_stylesheet
    
    
    def stylesheet_on_click(self,node,switch):
        follower_color='#0074D9'
        following_color='#FF4136'
        
        
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
                "width":4,
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
                            'width':15,
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
                            'width':15,
                            'opacity': 0.9,
                            'z-index': 5000
                        }
                    })
        else:
            for edge in node['edgesData']:
                if edge['target'] or edge['source'] ==  node['data']['id']:
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
                            "line-color": following_color,
                            'width':15,
                            'opacity': 0.9,
                            'z-index': 5000
                        }
                    })
            
        self.stylesheet=stylesheet
    