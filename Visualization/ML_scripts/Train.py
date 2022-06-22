# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 15:49:34 2022

@author: remit
"""

from my_data_set import MyEllipticBitcoinDataset 
from torch_geometric.loader.dataloader import DataLoader
from model import AML_model, train, test
import torch 
import warnings
import copy 
import os 
import argparse

warnings.filterwarnings('always') 



data_dir = "../data"
models_dir = "../models"


def main(): 

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
        default=64,
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
        "--jumping-knoweledge",
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
        default=100,
        type=int,
    )

    parser.add_argument(
        "-bs",
        "--batch-size",
        default=4,
        type=int,
    )

    parser.add_argument(
        "-t",
        "--type",
        default='SAGE',
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
        default = 'model_AML_'+args.type+'.pt',
        type=str,
    )

    args = parser.parse_args()


    data_train = MyEllipticBitcoinDataset(data_dir,split = 'train')
    data_val = MyEllipticBitcoinDataset(data_dir,split = 'val')
    data_test = MyEllipticBitcoinDataset(data_dir,split = 'test')
    
    in_channels = data_train.num_features
    num_classes = data_train.num_classes

    model = AML_model(
                        in_channels = in_channels, 
                        hidden_channels = args.hidden_channels,
                        num_layers = args.number_layers, 
                        out_channels = args.out_channels,
                        dropout = args.dropout,
                        act = args.activation, 
                        negative_slope = args.negative_slope, 
                        jk = args.jumping_knoweledge, 
                        heads = args.number_heads,
                        num_classes = num_classes,
                        _type = args.type
                    )

    train_loader = DataLoader(data_train, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(data_val, batch_size=args.batch_size, shuffle=False)
    test_loader = DataLoader(data_test, batch_size=args.batch_size, shuffle=False)

    device = torch.device('cpu')#'cuda' if torch.cuda.is_available() else 'cpu')
    optimizer = torch.optim.Adam(model.parameters(), lr = args.learning_rate)

    best_val_auc = 0
    print('Start training model of type : ', args.type)
    for epoch in range(1, args.number_epochs+1):
        loss = train(model,train_loader,optimizer,device)
        val_roc_auc, val_recall, val_precision = test(model,val_loader,device)
        test_roc_auc, test_recall, test_precision = test(model,test_loader,device)
        if val_roc_auc > best_val_auc:
            best_model = copy.deepcopy(model)
            best_val_auc = val_roc_auc
            best_test_auc = test_roc_auc
            print("[New best Model]")
        print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}')
        print(f'Val recall: {val_recall:.4f}, 'f'Val precision: {val_precision:.4f}')
        print(f'Test recall: {test_recall:.4f}, 'f'Test precision: {test_precision:.4f}')
        print(' ')

    SAVEPATH = os.path.join(models_dir,args.model_name)
    print('Done training')
    torch.save(best_model, SAVEPATH)
    print(f'Final Test: {best_test_auc:.4f}')


if __name__ == "__main__":
    main()