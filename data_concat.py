def data_concat():
    import numpy as np
    from glob import glob
    import pandas as pd

    KINEMATIC_PATH = 'csv/20240403/kine/*csv'
    FORCE_PATH = 'csv/20240403/force/*csv'

    KINEMATIC_DIR = [i.replace('\\','/') for i in glob(KINEMATIC_PATH)]
    FORCE_DIR = [i.replace('\\','/') for i in glob(FORCE_PATH)]

    for kine_dir, force_dir in zip(KINEMATIC_DIR, FORCE_DIR):
        
        kine = pd.read_csv(kine_dir)
        force = pd.read_csv(force_dir)

        _, kday, _, kfname = kine_dir.split('/')
        _, fday, _, ffname = force_dir.split('/')

        kfname = kfname.replace('.csv','')
        kplayer_name, ktrial, _, weight, height, kfoot = kfname.split('_')

        ffname = ffname.replace('.csv','')
        fplayer_name, ftrial, _, weight, height, ffoot = ffname.split('_')

        kine['player'] = kplayer_name
        kine['day']    = kday
        kine['trial']  = ktrial
        kine['weight'] = weight
        kine['height'] = height
        kine['foot']   = kfoot

        force['player'] = fplayer_name
        force['day']    = fday
        force['trial']  = ftrial
        force['weight'] = weight
        force['height'] = height
        force['foot']   = ffoot
        
    return kine, force