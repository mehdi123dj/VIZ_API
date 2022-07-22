
from torch_geometric.nn.models.basic_gnn import BasicGNN, GCN, GraphSAGE, GIN, GAT, PNA 
from torch_geometric.nn import Linear
from torch.nn import Softmax, BCEWithLogitsLoss 
from sklearn.metrics import roc_auc_score, recall_score, precision_score
from torch.nn.functional import one_hot
import torch 
import warnings
from sklearn.metrics import accuracy_score
warnings.filterwarnings('always') 


class AML_model(torch.nn.Module):
    def __init__(self,in_channels, hidden_channels,out_channels,num_layers, dropout,act, negative_slope, jk, heads,num_classes,_type):
        super().__init__()

        if _type == 'GAT':

            self.GNN_model = GAT(
                                in_channels = in_channels,
                                hidden_channels = hidden_channels,
                                num_layers = num_layers,
                                out_channels = out_channels,
                                dropout = dropout,
                                act = act,
                                jk = jk,
                                negative_slope = negative_slope,
                                heads = heads,
                                )
        elif _type == 'SAGE':
            self.GNN_model = GraphSAGE(
                                in_channels = in_channels,
                                hidden_channels = hidden_channels,
                                num_layers = num_layers,
                                out_channels = out_channels,
                                dropout = dropout,
                                # act = act,
                                jk = jk,
                                )
        elif _type == 'GCN':         
            self.GNN_model = GCN(
                                in_channels = in_channels,
                                hidden_channels = hidden_channels,
                                num_layers = num_layers,
                                out_channels = out_channels,
                                dropout = dropout,
                                act = act,
                                jk = jk,
                                )
        elif _type == 'GIN':         
            self.GNN_model = GCN(
                                in_channels = in_channels,
                                hidden_channels = hidden_channels,
                                num_layers = num_layers,
                                out_channels = out_channels,
                                dropout = dropout,
                                act = act,
                                jk = jk,
                                )


        self.lin = Linear(out_channels,num_classes)

    def forward(self, x, edge_index):
        X = self.GNN_model(x,edge_index)
        softmax = Softmax(dim=1)
        preds = softmax(self.lin(X))
        # preds = self.lin(X)
        return preds


def train(model,data,optimizer,device):
    loss=BCEWithLogitsLoss()
    data = data.to(device)
    model.train()
    optimizer.zero_grad()
    out  = model(data.x, data.edge_index)
    loss = loss(out[data.train_mask],data.y[data.train_mask].float())
    loss.backward()
    optimizer.step()

    return float(loss)

def test(model,data,device):
    data = data.to(device)
    model.eval()
    pred = model(data.x, data.edge_index)#.argmax(dim=-1)
    # print(torch.max(pred,dim=1)[1])
    # print(pred)
    pred = one_hot(torch.max(pred,dim=1)[1],num_classes=len(pred[0]))
    # print(pred)

    accs = []
    for mask in [data.train_mask, data.val_mask, data.test_mask]:
        # print(mask)
        # print(mask.sum())
        # print(pred[mask])
        # print(data.y[mask])
        # print([all(elem) for elem in pred[mask] == data.y[mask]])
        # accs.append(int(sum(([all(elem) for elem in pred[mask] == data.y[mask]]))) / int(mask.sum()))
        accs.append(accuracy_score(data.y[mask].cpu(), pred[mask].cpu()))
    # roc_auc = roc_auc_score(y, pred)
    # recall = recall_score(y,pred)
    # precision = precision_score(y,pred)

    return accs, pred[data.test_mask]
