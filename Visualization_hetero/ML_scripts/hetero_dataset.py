import torch
from typing import Callable, Optional
import pickle 
import numpy as np
import pandas as pd 
from torch_geometric.data import InMemoryDataset, download_url,HeteroData
import warnings


warnings.filterwarnings('always') 

class CreateHeteroInfopro(InMemoryDataset):
    
    def __init__(
        self,
        data_nodes,
        data_edges,
        root: str,
        transform: Optional[Callable] = None,
        pre_transform: Optional[Callable] = None,
    ):

        self.data_nodes = data_nodes
        self.data_edges = data_edges
        super().__init__(root, transform, pre_transform)
        self.data = torch.load(self.processed_paths[0])


    @property
    def processed_file_names(self):
        return ['data.pt']

    def process(self):
        
        df_nodes = pd.DataFrame(self.data_nodes)
        df_edges = pd.DataFrame(self.data_edges)

        typed_edges = [(df_edges.iloc[i]['source'],df_edges.iloc[i]['target'],df_edges.iloc[i]['class']) for i in range(len(df_edges))]
        Representations = torch.tensor([df_nodes.iloc[i]['feature'] for i in range(len(df_nodes))])


        data = HeteroData()
        edge_types = list(set([c for u,v,c in typed_edges]))
        data['Page'].x = torch.tensor(Representations)
        for et in edge_types:
            sub_edges = [(u,v) for u,v,c in typed_edges if c == et]
    
            if et in ['market_tag','web_tag']:
                from_edges = torch.tensor([u for u,v in sub_edges]+[v for u,v in sub_edges],dtype=torch.long)
                to_edges = torch.tensor([v for u,v in sub_edges]+[u for u,v in sub_edges],dtype=torch.long)
            else : 
                from_edges = torch.tensor([u for u,v in sub_edges],dtype=torch.long)
                to_edges = torch.tensor([v for u,v in sub_edges],dtype=torch.long)
              
            E = torch.zeros([2,len(to_edges)],dtype=torch.long)
            E[0]+=from_edges
            E[1]+=to_edges
            data['Page',et,'Page'].edge_index=E
        
        torch.save(data, self.processed_paths[0])

