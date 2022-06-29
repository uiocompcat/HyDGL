import numpy as np
import torch
import torch.nn.functional as F
import wandb

from torch_geometric.data.batch import Batch


class Trainer():

    def __init__(self, model, optimizer, scheduler=None, gradient_accumulation_splits=1):

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self._model = model.to(self.device)
        self._optimizer = optimizer
        self._scheduler = scheduler

        self._gradient_accumulation_splits = gradient_accumulation_splits

    @property
    def model(self):
        """Getter for model."""
        return self._model

    def _train(self, train_loader):
        self._model.train()
        loss_all = 0

        for batch in train_loader:

            self._optimizer.zero_grad()
            # gradient accumulation
            for batch_split in self._split_batch(batch, self._gradient_accumulation_splits):
                batch_split = batch_split.to(self.device)
                loss = F.mse_loss(self._model(batch_split), batch_split.y)
                loss.backward()
                loss_all += loss.item() * batch_split.num_graphs

            self._optimizer.step()

        return loss_all / len(train_loader.dataset)

    def _split_batch(self, batch, n_splits):

        # immediately return original batch if n_batches is one
        if n_splits == 1:
            return [batch]

        split_size = int(np.ceil(len(batch[:]) / n_splits))

        split_batches = []
        for i in range(n_splits):
            split_batches.append(Batch.from_data_list(batch[i * split_size:(i + 1) * split_size]))

        return split_batches

    def _mae(self, loader, target_means=0, target_stds=1):

        self._model.eval()
        errors = []

        for batch in loader:
            for batch_split in self._split_batch(batch, self._gradient_accumulation_splits):
                batch_split = batch_split.to(self.device)

                # calculate MAE
                # recover real physical values if target means and standard deviations are given
                errors.extend((np.abs((self._model(batch_split).cpu().detach().numpy() * target_stds + target_means) - (batch_split.y.cpu().detach().numpy() * target_stds + target_means))).tolist())

        return np.mean(errors)

    def _median(self, loader, target_means=0, target_stds=1):

        self._model.eval()
        errors = []

        for batch in loader:
            for batch_split in self._split_batch(batch, self._gradient_accumulation_splits):
                batch_split = batch_split.to(self.device)

                # calculate median
                # recover real physical values if target means and standard deviations are given
                errors.extend((np.abs((self._model(batch_split).cpu().detach().numpy() * target_stds + target_means) - (batch_split.y.cpu().detach().numpy() * target_stds + target_means))).tolist())

        return np.median(errors)

    def _rmse(self, loader, target_means=0, target_stds=1):

        self._model.eval()
        errors = []

        for batch in loader:
            for batch_split in self._split_batch(batch, self._gradient_accumulation_splits):
                batch_split = batch_split.to(self.device)

                # calculate RMSE
                # recover real physical values if target means and standard deviations are given
                errors.extend((np.abs((self._model(batch_split).cpu().detach().numpy() * target_stds + target_means) - (batch_split.y.cpu().detach().numpy() * target_stds + target_means))).tolist())

        return np.sqrt(np.mean(np.power(errors, 2)))

    def _r_squared(self, loader, target_means=0, target_stds=1):

        self._model.eval()
        targets = []
        predictions = []

        for batch in loader:
            for batch_split in self._split_batch(batch, self._gradient_accumulation_splits):
                batch_split = batch_split.to(self.device)

                # calculate R^2
                # recover real physical values if target means and standard deviations are given
                predictions.extend((self._model(batch_split).cpu().detach().numpy() * target_stds + target_means).tolist())
                targets.extend((batch_split.y.cpu().detach().numpy() * target_stds + target_means).tolist())

        # cast to np arrays
        predictions = np.array(predictions)
        targets = np.array(targets)

        target_mean = np.mean(targets)
        return 1 - (np.sum(np.power(targets - predictions, 2)) / np.sum(np.power(targets - target_mean, 2)))

    def predict_batch(self, batch, target_means=0, target_stds=1):

        predictions = []

        self._model.eval()
        for batch_split in self._split_batch(batch, self._gradient_accumulation_splits):
            batch_split = batch_split.to(self.device)

            # get predictions for batch
            predictions.extend((self.model(batch_split).cpu().detach().numpy() * target_stds + target_means).tolist())

        return predictions

    def run(self, train_loader, val_loader, test_loader, n_epochs=300, target_means=None, target_stds=None):

        best_val_error = None
        for epoch in range(1, n_epochs + 1):

            # get learning rate from scheduler
            if self._scheduler is not None:
                lr = self._scheduler.optimizer.param_groups[0]['lr']

            loss = self._train(train_loader)

            train_error = self._mae(train_loader, target_means=target_means, target_stds=target_stds)
            val_error = self._mae(val_loader, target_means=target_means, target_stds=target_stds)

            # learning rate scheduler step
            if self._scheduler is not None:
                self._scheduler.step(val_error)

            # retain early stop test error
            if best_val_error is None or val_error <= best_val_error:
                test_error = self._mae(test_loader, target_means=target_means, target_stds=target_stds)
                best_val_error = val_error

            output_line = f'Epoch: {epoch:03d}, LR: {lr:7f}, Loss: {loss:.7f}, 'f'Train MAE: {train_error:.7f}, 'f'Val MAE: {val_error:.7f}, Test MAE: {test_error:.7f}'
            print(output_line)

            # wandb logging
            wandb.log({'loss': loss}, step=epoch)
            wandb.log({'train_error': train_error}, step=epoch)
            wandb.log({'val_error': val_error}, step=epoch)
            wandb.log({'test_error': test_error}, step=epoch)

            wandb.log({'train_mae': self._mae(train_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)
            wandb.log({'val_mae': self._mae(val_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)
            wandb.log({'test_mae': self._mae(test_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)

            wandb.log({'train_median': self._median(train_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)
            wandb.log({'val_median': self._median(val_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)
            wandb.log({'test_median': self._median(test_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)

            wandb.log({'train_rmse': self._rmse(train_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)
            wandb.log({'val_rmse': self._rmse(val_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)
            wandb.log({'test_rmse': self._rmse(test_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)

            wandb.log({'train_r_squared': self._r_squared(train_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)
            wandb.log({'val_r_squared': self._r_squared(val_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)
            wandb.log({'test_r_squared': self._r_squared(test_loader, target_means=target_means, target_stds=target_stds)}, step=epoch)

        return self.model
