# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 12:04:28 2022

@author: remit
"""


from ML_scripts.model_edge_prediction_supervised import test, train, Net


import torch
import warnings
import copy 
import os 
import argparse
import torch_geometric.transforms as T



warnings.filterwarnings('always') 
model_dir = "model"

class run_edge_prediction_supervised():
    def __init__(self,dataset):
        self.dataset=dataset
        
    def __call__(self): 
    
        """
        Collect arguments and run.
        """
    
        parser = argparse.ArgumentParser()
    
        parser.add_argument(
            "-nl",
            "--number-layers",
            default=3,
            type=int,
        )
    
        parser.add_argument(
            "-hc",
            "--hidden-channels",
            default=128,
            type=int,
        )
    
        parser.add_argument(
            "-oc",
            "--out-channels",
            default=64,
            type=int,
        )
    
        parser.add_argument(
            "-drop",
            "--dropout",
            default=0.0,
            type=float,
        )
    
        parser.add_argument(
            "-jk",
            "--jumping-knowledge",
            default='cat',
            type=str,
        )
    
        parser.add_argument(
            "-act",
            "--activation",
            default='leaky_relu',
            type=str,
        )
    
        parser.add_argument(
            "-ns",
            "--negative-slope",
            default=0.0,
            type=float,
        )
    
        parser.add_argument(
            "-nh",
            "--number-heads",
            default=4,
            type=int,
        )
    
        parser.add_argument(
            "-ne",
            "--number-epochs",
            default=300,
            type=int,
        )
    
    
        parser.add_argument(
            "-t",
            "--type",
            default='edge_pred',
            type=str,
        )
    
        parser.add_argument(
            "-lr",
            "--learning-rate",
            default=0.001,
            type=float,
        )
    
        args = parser.parse_known_args()[0]
    
        parser.add_argument(
            "-mn",
            "--model-name",
            default = 'model_'+args.type+'.pt',
            type=str,
        )
    

    
        args = parser.parse_args()
        
        data = self.dataset[0]
        in_channels = len(data.x[0])

        print("Number of feature: ",in_channels)

        neg_sampling_ratio=5
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
        transform = T.Compose([
            T.NormalizeFeatures(),
            T.ToDevice(device),
            T.RandomLinkSplit(num_val=0.05, num_test=0.1, is_undirected=True,
                              add_negative_train_samples=True,
                              neg_sampling_ratio=neg_sampling_ratio),
        ])
        
        D = transform(data) # RandomLinkSplit return train,val,test for edges in three separate datasets
        model = Net(in_channels, args.hidden_channels, args.out_channels).to(device)
        optimizer = torch.optim.Adam(params=model.parameters(), lr = args.learning_rate)

    
    
        best_val_auc = final_test_auc = 0
        print('Start training model of type : ', args.type)
        for epoch in range(1, args.number_epochs+1):
            loss = train(model,D[0],optimizer,neg_sampling_ratio)
            val_auc = test(D[1],model)
            test_auc = test(D[2],model)
            if val_auc > best_val_auc:
                best_model = copy.deepcopy(model)
                # best_val = val_auc
                final_test_auc = test_auc
            print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}, Val: {val_auc:.4f}, '
                  f'Test: {test_auc:.4f}')
        
        print(f'Final Test: {final_test_auc:.4f}')
        SAVEPATH = os.path.join(model_dir,args.model_name)
        print('Done training')
        torch.save(best_model, SAVEPATH)
        
        # Inference on test set
        z = model.encode(D[2].x, D[2].edge_index)
        return model.decode_all(z).detach().cpu().numpy()
