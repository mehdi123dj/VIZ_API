import numpy as np
import torch 
from torch_geometric.nn import HeteroConv, GATConv,Linear,GCNConv,to_hetero,SAGEConv
from sklearn.metrics import roc_auc_score, recall_score, precision_score
import torch.nn.functional as F
from ML_scripts.utils import update_negative_sample
from torch_geometric.nn.models import JumpingKnowledge
device = torch.device("cpu")
class GNN(torch.nn.Module):
    def __init__(self,mts, hidden_channels, out_channels, num_layers):
        super().__init__()
        self.num_layers = num_layers
        self.convs = torch.nn.ModuleList()
        self.lins = torch.nn.ModuleDict()
        self.bns = torch.nn.ModuleList()
        self.JK = JumpingKnowledge(mode = 'cat')

        node_types = list(set([mt[0] for mt in mts]+[mt[2] for mt in mts]))
        
        for i in range(num_layers):
            conv = HeteroConv({mt : SAGEConv((-1,-1), hidden_channels[i]) for mt in mts}, aggr='mean')
            #conv = HeteroConv({mt : GATConv((-1,-1), hidden_channels[i]) for mt in mts}, aggr='mean')
            self.convs.append(conv)
            
        for node in node_types:
            #self.lins[node] = Linear(hidden_channels[num_layers-1], out_channels)
            self.lins[node] = Linear(sum(list(hidden_channels.values())), out_channels)
            #self.lins[node] = Linear(-1, out_channels)


    def encode(self, x_dict, edge_index_dict):
        L = []
        for i in range(self.num_layers):
            conv = self.convs[i]
            x_dict = conv(x_dict, edge_index_dict)
            L.append(x_dict)
        x_dict = {node : self.JK([L[i][node] for i in range(len(L))]) for node in x_dict.keys()}
        x_dict = {node: self.lins[node](x.float())  for node, x in x_dict.items()}
        return x_dict

    def decode(self, x_dict, edge_label_index_dict):
        pred = {}
        
        for mt in edge_label_index_dict.keys():
            nodes_first = torch.index_select(x_dict[mt[0]], 0, edge_label_index_dict[mt][0,:].long())
            nodes_second = torch.index_select(x_dict[mt[2]], 0, edge_label_index_dict[mt][1,:].long())
            pred[mt] = (nodes_first * nodes_second).sum(dim=-1)
            
        return pred

    def decode_all(self,H):
        #Specifique au cas Pages, doit etre generalise
        prob_adj = (H @ H.t()).sigmoid()
        print(((prob_adj > .95).nonzero(as_tuple=False).t()).shape)
        return (prob_adj > .95).nonzero(as_tuple=False).t()



def train(model,train_data,optimizer):
    
    edge_label_index_dict = train_data.edge_label_index_dict
    edge_label_dict = train_data.edge_label_dict

    model.train()
    optimizer.zero_grad()
    X_dict = model.encode(train_data.x_dict, train_data.edge_index_dict)
    out_dict = model.decode(X_dict, edge_label_index_dict)
        
    loss = 0
    for k in list(out_dict.keys()):
        loss += F.binary_cross_entropy_with_logits(out_dict[k],edge_label_dict[k])
    
    loss.backward()
    optimizer.step()
    return loss


def test(model,data):
    model.eval()
    X_dict = model.encode(data.x_dict, data.edge_index_dict)
    out_dict = model.decode(X_dict, data.edge_label_index_dict)
    roc_auc = recall = precision = acc = 0
    
    for key in out_dict:
        
        link_prob = out_dict[key].sigmoid()
        p = link_prob.cpu().detach().numpy()
        pred_label = np.zeros_like(p, dtype=np.int64)
        pred_label[np.where(p >= 0.5)[0]] = 1
        pred_label[np.where(p < 0.5)[0]] = 0
        
        
        label_array = data.edge_label_dict[key].cpu().numpy() 
        roc_auc+=roc_auc_score(label_array, pred_label)/len(out_dict)
        recall+=recall_score(label_array,pred_label)/len(out_dict)
        precision+=precision_score(label_array,pred_label)/len(out_dict)
        acc += np.sum(pred_label == data.edge_label_dict[key].cpu().numpy())/len(out_dict)

    ROC_AUC = roc_auc 
    REC = recall 
    PREC = precision 

    return ROC_AUC,REC,PREC
