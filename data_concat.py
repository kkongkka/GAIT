def data_concat():
    import numpy as np
    from glob import glob
    import pandas as pd

    FP1_PATH = 'csv/2/FP1/*csv'
    FP2_PATH = 'csv/2/FP2/*csv'

    FP1_DIR = [i.replace('\\','/') for i in glob(FP1_PATH)]
    FP2_DIR = [i.replace('\\','/') for i in glob(FP2_PATH)]

    for FP1_dir, FP2_dir in zip(FP1_DIR, FP2_DIR):
        
        FP1 = pd.read_csv(FP1_dir)
        FP2 = pd.read_csv(FP2_dir)

        _, kday, _, kfname = FP1_dir.split('/')
        _, fday, _, ffname = FP2_dir.split('/')

        kfname = kfname.replace('.csv','')
        kplayer_name, ktrial, _, weight, height, kfoot = kfname.split('_')

        ffname = ffname.replace('.csv','')
        fplayer_name, ftrial, _, weight, height, ffoot = ffname.split('_')

        FP1['player'] = kplayer_name
        FP1['day']    = kday
        FP1['trial']  = ktrial
        FP1['weight'] = weight
        FP1['height'] = height
        FP1['foot']   = kfoot

        FP2['player'] = fplayer_name
        FP2['day']    = fday
        FP2['trial']  = ftrial
        FP2['weight'] = weight
        FP2['height'] = height
        FP2['foot']   = ffoot
        
    return FP1, FP2