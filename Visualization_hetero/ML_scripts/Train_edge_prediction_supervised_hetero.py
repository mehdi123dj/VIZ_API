import torch 
import pickle
from torch_geometric.transforms import ToUndirected
import os 
import copy 
from ML_scripts.utils import update_negative_sample,extract_negative_pairs
from ML_scripts.model_edge_prediction_hetero import train, test , GNN 
import argparse
from torch_geometric.transforms import RandomLinkSplit
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
import warnings


model_dir = "model"
warnings.filterwarnings('always') 

class run_edge_prediction_hetero():
    def __init__(self,dataset):
        self.dataset=dataset
    def __call__(self): 

        """
        Collect arguments and run.
        """

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-lr",
            "--learning-rate",
            default=0.001,
            type=float,
        )

        parser.add_argument(
            "-wd",
            "--weight-decay",
            default=0.,
            type=float,
        )

        parser.add_argument(
            "-ns",
            "--negative-sampling-ratio",
            default=5,
            type=int,
        )


        parser.add_argument(
            "-sp",
            "--save-path",
            default=model_dir,
            type=str,
        )

        parser.add_argument(
            "-mn",
            "--model-name",
            default="full_batch_transductive_link_pred.mdl",
            type=str,
        )

        parser.add_argument(
            "-e",
            "--number-epochs",
            default=500,
            type=int,
        )

        parser.add_argument(
            "-us",
            "--update-strategy",
            default=10,
            type=int,
        )

        args = parser.parse_args()
        writer = SummaryWriter()

        ##########################################################################################################################################
        ##########################################################################################################################################

        learning_rate = args.learning_rate
        weight_decay = args.weight_decay
        SAVEPATH = os.path.join(args.save_path,args.model_name)
        Negative_Sampling_Ratio = args.negative_sampling_ratio
        nepochs = args.number_epochs
        update_every = args.update_strategy
        
        device = torch.device("cpu")

        data = self.dataset[0]
        data['Page'].x = data['Page'].x.float()

        Mts = [("Page", "ensavoirplus", "Page")]

        print('Initialization')

        transform = RandomLinkSplit(is_undirected=False,
                                    num_val = .25,
                                    num_test = .25,
                                    edge_types = ('Page', 'ensavoirplus', 'Page'),
                                    neg_sampling_ratio = Negative_Sampling_Ratio,
                                    disjoint_train_ratio = .5)
        
        Train,Val,Test=transform(data)
        NP_train = extract_negative_pairs(Train,Mts)
        NP_val = extract_negative_pairs(Val,Mts)
        NP_test = extract_negative_pairs(Test,Mts)
        train_data = update_negative_sample(Train,Negative_Sampling_Ratio,NP_train)
        val_data = update_negative_sample(Val,Negative_Sampling_Ratio,NP_val)
        test_data = update_negative_sample(Test,Negative_Sampling_Ratio,NP_test)
        train_data.to(device)
        val_data.to(device)
        test_data.to(device)
        print('Done')

        ##########################################################################################################################################
        ##########################################################################################################################################

        mts = list(train_data.edge_index_dict.keys())
        HCs = {0:64,1:64,2:64,3:64,4:64}
        model = GNN(mts,hidden_channels=HCs, out_channels=64,num_layers = len(HCs))

        optimizer = torch.optim.Adam(params=model.parameters(), lr=learning_rate, weight_decay = weight_decay)

        ##########################################################################################################################################
        ##########################################################################################################################################

        best_val_auc = 0
        UPDATE = [i for i in range(1,nepochs+1) if i%update_every == 0]
        counter = 0
        for epoch in tqdm(range(1, nepochs+1)):
            counter+=1
            if counter in UPDATE:
                train_data = update_negative_sample(Train,Negative_Sampling_Ratio,NP_train).to(device)

            loss = train(model,train_data,optimizer)
            val_auc,val_rec,val_prec = test(model,val_data)
            test_auc,test_rec,test_prec = test(model,test_data)
            if val_auc > best_val_auc:
                best_model = copy.deepcopy(model)
                best_val_auc = val_auc
                best_test_auc = test_auc
                torch.save(best_model, SAVEPATH)

        print(f'Final Test: {best_test_auc:.4f}')
        
        H = best_model.encode(data.x_dict, data.edge_index_dict)['Page']
        return best_model.decode_all(H).detach().cpu().numpy()


        ##########################################################################################################################################
        ##########################################################################################################################################


