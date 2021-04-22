import glob
import numpy as np
import os
import json
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

if __name__=='__main__':
    
    input_files = glob.glob('{}/*.npy'.format('/opt/ml/processing/input'))
    print('\nINPUT FILE LIST: \n{}\n'.format(input_files))

    X = np.load(os.path.join('/opt/ml/processing/input', 'X.npy'))
    y = np.load(os.path.join('/opt/ml/processing/input', 'y.npy'))

    print('\nFit & transform features...')
    scaler = StandardScaler()
    X_transformed = scaler.fit_transform(X)
    print('Done!')

    # split data into train, test and validation
    X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=1)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=1)
    
    np.save('/opt/ml/processing/output/X_train.npy', X_train)
    print('Saved X_train file...\n')

    np.save('/opt/ml/processing/output/y_train.npy', y_train)
    print('Saved y_train file...\n')

    np.save('/opt/ml/processing/output/X_test.npy', X_test)
    print('Saved X_test file...\n')

    np.save('/opt/ml/processing/output/y_test.npy', y_test)
    print('Saved y_test file...\n')

    with open('/opt/ml/processing/output/X_val.json', 'w') as outfile:
        json.dump(X_val.tolist(), outfile)
        print('Saved X_val file...\n')

    with open('/opt/ml/processing/output/y_val.json', 'w') as outfile:
        json.dump(y_val.tolist(), outfile)
        print('Saved y_val file...\n')

    with open('/opt/ml/processing/output/StandardScaler.pkl', 'wb') as outfile:
        pickle.dump(scaler, outfile, protocol=pickle.HIGHEST_PROTOCOL)        
        print('Saved StandardScaler file...\n')
