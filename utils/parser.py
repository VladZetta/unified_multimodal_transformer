import argparse

def createParser():
    parser = argparse.ArgumentParser(description='Input parameters to train the model.')
    
    # mode
    parser.add_argument ('-mode', '--mode', default="train", help='Mode of the script: train or test.')
    
    # device
    parser.add_argument ('-n_gpu', '--n_gpu', type=int, default=0,
                        help='Number of GPU core.')
    # seed
    parser.add_argument ('-seed', '--seed', type=int, default=42,
                        help='Random seed')
    # train dataset
    parser.add_argument ('-afile', '--annotation_file', default="annotations_file_short_SF.csv",
                        help='Path to the annotation_file.')
    parser.add_argument ('-path_to_train_dataset', '--path_to_train_dataset', default="/workdir/sf_pv/data_v2",
                        help='Path to the dataset directory.')
    parser.add_argument ('-dataset_type', '--dataset_type', default="SF", choices=("SF","VX2"),
                        help='SF - Speaking Faces, VX2 - VoxCeleb2.')

    # valid dataset - path_to_valid_dataset
    parser.add_argument ('-path_to_valid_dataset', '--path_to_valid_dataset', 
                         default='/workdir/sf_pv',
                        help='path to validation dataset: for SF - sf_pv, \
                              for VoxCeleb1 - VoxCeleb1/test.')
    parser.add_argument ('-path_to_valid_list', '--path_to_valid_list', 
                         default='/workdir/sf_pv/metadata/valid_list_v2.txt',
                        help='path to validation list: for SF - sf_pv/metadata/valid_list_v2.txt \
                              for VoxCeleb1 - VoxCeleb1/metadata/test_list_vc_v2.txt')
    

    # train_dataloader
    parser.add_argument ('-sampler', '--sampler', default="SFProtoSampler", 
                         choices="SFProtoSampler, VoxCelebProtoSampler")

    parser.add_argument ('-n_b', '--n_batch', type=int, default=100, 
                        help='Number of batches in train dataloader')
    parser.add_argument ('-n_w', '--n_ways', type=int, default=30,
                        help='Number of classes inside one batch. \
                            Maximum number of n_ways is 100, \
                            since maximum number of classes in train set is 100.')
    parser.add_argument ('-n_s', '--n_support', type=int, default=1,
                        help='Number of support vectors inside one class. \
                            The following inequality should be satisfied: \
                            n_support + n_query < 78, since minimum number of \
                            utterances per person in SpeakingFaces Dataset in train set is 78.')
    parser.add_argument ('-n_q', '--n_query', type=int, default=1,
                        help='Number of query vectors inside one class. \
                            The following inequality should be satisfied: \
                            n_support + n_query < 78, since minimum number of \
                            utterances per person in SpeakingFaces Dataset in train set is 78.')
    # valid_dataloader
    parser.add_argument ('-b_s', '--batch_size', type=int, default=64, 
                        help='Batch size in valid dataloader')

    # optimizer
    parser.add_argument ('-weight_decay', '--weight_decay', type=float, default=0, 
                        help='weight decay regularization parameter.')
    parser.add_argument ('-lr', '--lr', type=float, default=1e-3, 
                        help='learning rate parameter.')
    parser.add_argument ('-scheduler', '--scheduler', default="StepLR", 
                        choices=("StepLR","CosineAnnealingLR"),
                        help='Choose scheduler.')
                         
    parser.add_argument ('-step_size', '--step_size', type=int, default=10, 
                        help='step_size for StepLR scheduler ')
    parser.add_argument ('-gamma', '--gamma', type=float, default=0.95, 
                        help='gamma for StepLP scheduler ')
    parser.add_argument ('-t_max', '--t_max', type=int, default=10, 
                        help='t_max for CosineAnnealingLR scheduler ')
    
    # loss
    parser.add_argument ('-dist_type', '--dist_type', default='squared_euclidean',
                        help='Distance type to calculate in Prototypical Loss function \
                              (default: "squared_euclidean"). Can be either "squared_euclidean" or "cosine_similarity"')
    parser.add_argument ('-loss_type', '--loss_type', default='metric_learning',
                        choices=("classification","metric_learning"),
                        help='Loss type can be either classification loss or metric learning loss.')

    # model
    parser.add_argument ('-library', '--library', default="timm", 
                        choices=("pytorch","timm","huggingface"),
                        help='Choose library from where to load model.')
    parser.add_argument ('-model_name', '--model_name', default="vit_base_patch16_224", 
                        choices=("resnet34","vit_base_patch16_224","AST","WavLM"),
                        help='Choose model to load.')
    parser.add_argument ('-pretrain_w', '--pretrained_weights', type=int, choices=(0,1), default=1,
                        help='Ways of weights initialization. \
                            If "1" it means resnet34 pretrained weights are used, \
                            If "0", it means random initialization and no pretrained weights.')
    parser.add_argument ('-fine_tune', '--fine_tune', type=int, choices=(0,1), default=1,
                        help='Allows to choose between two types of transfer learning: fine tuning and feature extraction. \
                            If "1" it means fine tuning mode, i.e. train all weights,  \
                            If "0", it means feature extraction mode, i.e. train last classifier layer. \
                            For more details of the description of each mode, \
                            read https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html')
    
    parser.add_argument ('-transfer', '--transfer', type=int, choices=(0,1), default=0,
                        help='Allows to continue training of a pretrained model')
    
    parser.add_argument ('-transfer_exp_path', '--transfer_exp_path', default="exp1",
                        help='The path to the experiment from where to load the model and transfer knowledge.')
    
    parser.add_argument ('-emb_size', '--embedding_size', type=int, default=128,
                        help='Size of the embedding of the last layer.')
    parser.add_argument ('-pool', '--pool', default="default", 
                        choices=("default","SAP"),
                        help='Choose pooling.')
    parser.add_argument ('-exp_name', '--exp_name', default="exp1",
                        help='Experiment name.')
    
    # audio transforms
    parser.add_argument ('-sample_rate', '--sample_rate', type=int, default=16000,
                        help='Audio signal sample rate.')
    parser.add_argument ('-sample_duration', '--sample_duration', type=float, default=3,
                        help='Sample_duration in seconds.')
    parser.add_argument ('-n_fft', '--n_fft', type=int, default=512,
                        help='Size of FFT, creates n_fft // 2 + 1 bins')
    parser.add_argument ('-win_length', '--win_length', type=int, default=400,
                        help='Window size of MelSpectrogram transformation')
    parser.add_argument ('-hop_length', '--hop_length', type=int, default=128,
                        help='Length of hop between STFT windows.')
    parser.add_argument ('-n_mels', '--n_mels', type=int, default=128,
                        help='Number of mel filterbanks. ')
                    
    # image transform
    parser.add_argument ('-image_resize', '--image_resize', type=int, default=128,
                        help='Resize image to the input size.')

    # train
    parser.add_argument ('-n_epochs', '--num_epochs', type=int, default=100,
                        help='Number of epochs in training process.')
    parser.add_argument ('-save_dir', '--save_dir', default="/workdir/results",
                        help='Path to the directory where output data will be saved.')
    parser.add_argument('-data_type', '--data_type', nargs='+', default=['rgb'],
                        help='Allows to choose modality, it can be either "rgb" or "thrm". \
                            If "rgb" it means model train and evaluate on rgb images, \
                            If "thr", it means model train and evaluate on thermal images, \
                            If "wav", it means model train and evaluate on wav files.')
    parser.add_argument ('-wandb', '--wandb', type=int, choices=(0,1), default=0,
                        help='Use wandb or not. \
                            If "1" it means WanDB is used, \
                            If "0", it means no.')

    return parser
