
from torch_geometric.nn.models.basic_gnn import GCN, GraphSAGE, GAT
from torch_geometric.nn import Linear
from torch.nn import Softmax, BCEWithLogitsLoss 
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
    pred = model(data.x, data.edge_index)
    pred = one_hot(torch.max(pred,dim=1)[1],num_classes=len(pred[0]))

    accs = []
    for mask in [data.train_mask, data.val_mask, data.test_mask]:
        accs.append(accuracy_score(data.y[mask].cpu(), pred[mask].cpu()))


    return accs, pred[data.test_mask]
