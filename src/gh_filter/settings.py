DL_FRAMEWORKS_DIR = "../../../DL Frameworks/"

APP_CONFIG = {
    "distilled_dir":"../../data/distilled/",
    "raw_dir":"../../data/raw/",
}

DATA_CONFIG = {
    'frameworks': ['caffe','keras','opencv','pytorch', 'tensorflow'],
    # IMPORTANT: for each framework, the corresponding local repository must be specified as follow:
    'caffe_repo':      DL_FRAMEWORKS_DIR + 'caffe',
    'keras_repo':      DL_FRAMEWORKS_DIR + 'keras',
    'opencv_repo':     DL_FRAMEWORKS_DIR + 'opencv',
    'pytorch_repo':    DL_FRAMEWORKS_DIR + 'pytorch',
    'tensorflow_repo': DL_FRAMEWORKS_DIR + 'tensorflow',
}