### Run hyperparameter search for specific network architectures.


from train import train
import torch
import numpy as np


################################################################
# Default Configs
################################################################
configs = {
    'model':                'fno',
    'experiment':           'Burgers',
    # 'num_train':            1000,
    # 'num_test':             20,
    # 'batch_size':           20, 
    # 'epochs':               10001,
    # 'test_epochs':          10,

    # Training specific parameters
    # 'learning_rate':        0.0005,
    # 'scheduler_step':       5,
    # 'scheduler_gamma':      0.99,
    # 'weight_decay':         1e-4,                    # Weight decay

    'display_predictions':  False,
    'save_model':           True,
    'load_model':           False,
    'model_path':           '_Models/model.pt',      # Path to model file if loading model
    'min_max_norm':         False,
    # 'data_small_domain':    True,              # Whether to use a small domain or not for specifically the Airfoil experiment

    'device':               torch.device('cuda'),     # Define device for training & inference - GPU/CPU
    # 'iphi_loss_reg':        0.0,                    # Regularization parameter for IPHI loss term
    # 'loss_fn':              'L1',                   # Loss function to use - L1, L2
    # 'datapath':             '_Data/Elasticity/',    # Path to data

    # Specifically for Burgers
    # 'data_dist':            'uniform',              # Data distribution to use - uniform, cubic_from_conexp, random

    # Specifically for Shear Layer
    # 'center_1':         256,                        # Center of top interface
    # 'center_2':         768,                        # Center of bottom interface
    # 'uniform':          100,                        # Number of points uniform along interface
    # 'growth':           1.0,                        # Growth factor, how quickly do points become sparse

    # Specifically for Humidity
    # 'center_lat':       180,                        # Lattitude center of the nonuniform sampling region
    # 'center_lon':       140,                        # Longitude center of the nonuniform sampling region
}



if __name__ == "__main__":
    ################################################################
    # Search Configs
    ################################################################
    learning_rates      = [5e-3, 5e-4, 1e-4]
    scheduler_steps     = [10, 100]
    scheduler_gammas    = [0.99, 0.9]


    log = open(f"_Models/grid_search_{configs['model']}_{configs['experiment']}.txt", 'w')
    log.write(f"--- Grid Search for {configs['model']} using {configs['experiment']} Data ---\n\n")

    for lr in learning_rates:
        configs['learning_rate'] = lr
        
        for step in scheduler_steps:
            configs['scheduler_step'] = step
            
            for gamma in scheduler_gammas:
                configs['scheduler_gamma'] = gamma
                
                log.write('-'*10)
                log.write(f'\nLearning Rate: {lr} \tScheduler Steps: {step} \tScheduler Gamma: {gamma}\n')
                log.flush()

                # Only drawback here is that data loaded each time. This is about 4 minutes per search. 
                metric_list = train(configs)
                
                log.write(f'Average Training Time: {np.mean(metric_list[0]):.4f}s +- {np.std(metric_list[0]):.4f}s \t\tLowest Relative Error: {100*min(metric_list[-2]):.6f}%\n')
                log.write(f'\nEpoch \tTrain Time \tTrain Loss \tTest Loss \tRelative Error \tMedian Error\n')
                for i, (train_t, train_l, test_l, rel_err, rel_med) in enumerate(zip(*metric_list)):
                    log.write(f'{i:04d} \t{train_t:.4f}s \t{train_l:.4e} \t{test_l:.4e} \t{rel_err:.4e}% \t{rel_med:.4e}%\n')
                log.flush()
                
    log.close()
                