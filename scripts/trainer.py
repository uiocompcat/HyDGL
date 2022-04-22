import numpy as np
import torch
import torch.nn.functional as F
import wandb


class Trainer():

    def __init__(self, model, optimizer, scheduler=None):

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self._model = model.to(self.device)
        self._optimizer = optimizer
        self._scheduler = scheduler

    @property
    def model(self):
        """Getter for model."""
        return self._model

    def _train(self, train_loader):
        self._model.train()
        loss_all = 0

        for data in train_loader:
            data = data.to(self.device)
            self._optimizer.zero_grad()
            loss = F.mse_loss(self._model(data), data.y)
            loss.backward()
            loss_all += loss.item() * data.num_graphs
            self._optimizer.step()

        return loss_all / len(train_loader.dataset)

    def _test(self, loader, target_means=None, target_stds=None):

        self._model.eval()
        error = 0

        for data in loader:
            data = data.to(self.device)

            # calculate MAE
            # recover real physical values if target means and standard deviations are given
            if target_means is not None and target_stds is not None:
                error += (np.abs((self._model(data).cpu().detach().numpy() * target_stds + target_means) - (data.y.cpu().detach().numpy() * target_stds + target_means))).sum().item()
            else:
                error += (self._model(data) - data.y).abs().sum().item()

        return error / len(loader.dataset)

    def predict_batch(self, data, target_means=None, target_stds=None):

        self._model.eval()

        data = data.to(self.device)

        if target_means is not None and target_stds is not None:
            predictions = (self.model(data).cpu().detach().numpy() * target_stds + target_means).tolist()
        else:
            predictions = self.model(data).cpu().detach().numpy().tolist()

        return predictions

    def run(self, train_loader, val_loader, test_loader, n_epochs=300, target_means=None, target_stds=None):

        best_val_error = None
        for epoch in range(1, n_epochs + 1):

            # get learning rate from scheduler
            if self._scheduler is not None:
                lr = self._scheduler.optimizer.param_groups[0]['lr']

            loss = self._train(train_loader)

            train_error = self._test(train_loader, target_means=target_means, target_stds=target_stds)
            val_error = self._test(val_loader, target_means=target_means, target_stds=target_stds)

            # learning rate scheduler step
            if self._scheduler is not None:
                self._scheduler.step(val_error)

            if best_val_error is None or val_error <= best_val_error:
                test_error = self._test(test_loader, target_means=target_means, target_stds=target_stds)
                best_val_error = val_error

            output_line = f'Epoch: {epoch:03d}, LR: {lr:7f}, Loss: {loss:.7f}, 'f'Train MAE: {train_error:.7f}, 'f'Val MAE: {val_error:.7f}, Test MAE: {test_error:.7f}'
            print(output_line)

            # wandb logging
            wandb.log({'loss': loss}, step=epoch)
            wandb.log({'train_error': train_error}, step=epoch)
            wandb.log({'val_error': val_error}, step=epoch)
            wandb.log({'test_error': test_error}, step=epoch)

        return self.model
