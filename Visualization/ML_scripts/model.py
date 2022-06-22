
from torch_geometric.nn.models.basic_gnn import BasicGNN, GCN, GraphSAGE, GIN, GAT, PNA 
from torch_geometric.nn import Linear
from torch.nn import Softmax, BCEWithLogitsLoss 
from sklearn.metrics import roc_auc_score, recall_score, precision_score
from torch.nn.functional import one_hot
import torch 
import warnings
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
        # print(x)
        X = self.GNN_model(x,edge_index)
        softmax = Softmax(dim=1)
        preds = softmax(self.lin(X))

        return preds


def train(model,train_loader,optimizer,device,):

    loss_op = BCEWithLogitsLoss()
    total_loss = 0
    for data in train_loader : 
        model.train()
        optimizer.zero_grad()
        data = data.to(device)
        labeled_idx = torch.where(data.y !=2)
        x_out  = model(data.x, data.edge_index)

        loss = loss_op(x_out[torch.where(data.y !=2)], one_hot(data.y[torch.where(data.y !=2)]).double())
        total_loss += loss.item() * data.num_graphs
        loss.backward()
        optimizer.step()

    return total_loss / len(train_loader.dataset)

def test(model,loader,device):

    ys, preds = [], []
    for data in loader:
        model.eval()
        data = data.to(device)
        labeled_idx = torch.where(data.y !=2)

        x_out = model(data.x, data.edge_index)[labeled_idx]

        preds.append(torch.tensor([x_out[i].argmax().item() for i in range(x_out.shape[0])]))
        ys.append(data.y[labeled_idx])

    y, pred = torch.cat(ys, dim=0).numpy(), torch.cat(preds, dim=0).numpy()

    roc_auc = roc_auc_score(y, pred)
    recall = recall_score(y,pred)
    precision = precision_score(y,pred)

    return roc_auc,recall,precision
