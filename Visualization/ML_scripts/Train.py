# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 15:49:34 2022

@author: remit
"""


# from torch_geometric.loader.dataloader import DataLoader

from ML_scripts.model import AML_model, train, test
import torch 
import warnings
import copy 
import os 
import argparse
from torch.nn.functional import one_hot

warnings.filterwarnings('always') 



model_dir = "model"

class run():
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
            default=32,
            type=int,
        )
    
        parser.add_argument(
            "-oc",
            "--out-channels",
            default=16,
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
            default=200,
            type=int,
        )
    
    
        parser.add_argument(
            "-t",
            "--type",
            default='GAT',
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

        data.y = one_hot(data.y)
        in_channels = len(data.x[0])

        num_classes = len(data.y[0])
        print("Number of feature: ",in_channels)
        print("Number of classes: ",num_classes)
        model = AML_model(
                            in_channels = in_channels, 
                            hidden_channels = args.hidden_channels,
                            num_layers = args.number_layers, 
                            out_channels = args.out_channels,
                            dropout = args.dropout,
                            act = args.activation, 
                            negative_slope = args.negative_slope, 
                            jk = args.jumping_knowledge, 
                            heads = args.number_heads,
                            num_classes = num_classes,
                            _type = args.type
                        )
    
    
        device = torch.device('cpu')
        optimizer = torch.optim.Adam(model.parameters(), lr = args.learning_rate)
    
        best_val_acc = 0
        test_list = []
        print('Start training model of type : ', args.type)
        for epoch in range(1, args.number_epochs+1):
            loss = train(model,data,optimizer,device)
            acc,test_class = test(model,data,device)
            val_acc,test_acc = acc[1:]
             # = test(model,data,device)
            if val_acc > best_val_acc:
                best_model = copy.deepcopy(model)
                best_val_acc = val_acc
                best_test_acc = test_acc
                test_list = [list(elem).index(1) for elem in test_class]
                print("[New best Model]")
            print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}')
            print(f'Val accuracy: {val_acc:.4f}')
            print(f'Test accuracy: {test_acc:.4f}')
            print(' ')
    
        SAVEPATH = os.path.join(model_dir,args.model_name)
        print('Done training')
        torch.save(best_model, SAVEPATH)
        print(f'Final Test: {best_test_acc:.4f}')
        return test_list
    
