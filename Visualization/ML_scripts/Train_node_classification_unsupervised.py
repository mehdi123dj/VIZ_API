# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:44:39 2022

@author: remit
"""

# from torch_geometric.loader.dataloader import DataLoader

from ML_scripts.model_node_classification_unsupervised import classifier, Encoder, corruption, train,summary
from torch_geometric.nn import DeepGraphInfomax
import torch 
import warnings
import copy 
import os 
import argparse

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
            "-hc",
            "--hidden-channels",
            default=512,
            type=int,
        )

        parser.add_argument(
            "-ne",
            "--number-epochs",
            default=100,
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
        in_channels = len(data.x[0])
        print("Number of feature: ",in_channels)
        have_class=False
        if 'y' in data:
            num_classes = max(data.y)+1
            have_class=True
            print("Number of classes: ",num_classes)
        
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = DeepGraphInfomax(
                                    hidden_channels=args.hidden_channels,
                                    encoder=Encoder(in_channels, args.hidden_channels),
                                    summary=summary, 
                                    corruption=corruption
                                    ).to(device)
        data = data.to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr = args.learning_rate)

        print('Start training model of type : ', args.type,args.learning_rate)
        for epoch in range(1, args.number_epochs+1):
            loss = train(model,data,optimizer)
            print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}')

    
        SAVEPATH = os.path.join(model_dir,args.model_name)
        print('Done training')
        torch.save(copy.deepcopy(model), SAVEPATH)
        if have_class:
            z, _, _ = model(data.x, data.edge_index)
            train_z,train_y,test_z,test_y = z[data.train_mask], data.y[data.train_mask],z[data.test_mask], data.y[data.test_mask]
            Classifier = classifier(train_z,train_y,test_z,test_y)

            test_acc,test_class = Classifier.compute_score(),Classifier.predict()
            print(f'Test accuracy: {test_acc:.4f}')
            print(' ')
            return test_class
        return
    