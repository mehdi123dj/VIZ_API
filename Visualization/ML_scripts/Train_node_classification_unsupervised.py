# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:44:39 2022

@author: remit
"""

# from torch_geometric.loader.dataloader import DataLoader

from ML_scripts.model_node_classification_unsupervised import Encoder, corruption, test, train, DeepGraphInfomax,summary
import torch 
import warnings
import copy 
import os 
import argparse
from torch.nn.functional import one_hot

warnings.filterwarnings('always') 



model_dir = "model"

class run_node_classif_unsupervised():
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
            default=512,
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
            default='DeepInfoMax',
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
        # print(data.y)
        # data.y = one_hot(data.y)
        in_channels = len(data.x[0])

        num_classes = max(data.y)+1
        print("Number of feature: ",in_channels)
        print("Number of classes: ",num_classes)
        
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = DeepGraphInfomax(
                                    hidden_channels=args.hidden_channels,
                                    encoder=Encoder(in_channels, args.hidden_channels),
                                    summary=summary, 
                                    corruption=corruption
                                    ).to(device)
        
        optimizer = torch.optim.Adam(model.parameters(), lr = args.learning_rate)
    
    
        best_test_acc=0
        # test_list = []
        print('Start training model of type : ', args.type)
        for epoch in range(1, args.number_epochs+1):
            
            loss = train(model,data,optimizer,device)

            test_acc,test_class = test(model,data,device)
            
             # = test(model,data,device)
            # if test_acc > best_test_acc:
            #     best_model = copy.deepcopy(model)
            #     best_val_acc = val_acc
                # best_test_acc = test_acc
                # test_list = [list(elem).index(1) for elem in test_class]
            #     print("[New best Model]")
            print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}')
            # print(f'Val accuracy: {val_acc:.4f}')
            print(f'Test accuracy: {test_acc:.4f}')
            print(' ')
    
        SAVEPATH = os.path.join(model_dir,args.model_name)
        print('Done training')
        torch.save(copy.deepcopy(model), SAVEPATH)
        print(f'Final Test: {best_test_acc:.4f}')
        return test_class.detach().cpu()
    