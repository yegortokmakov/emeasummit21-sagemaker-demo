import argparse
import numpy as np
import os
import tensorflow as tf

from model_def import get_model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def parse_args():

    parser = argparse.ArgumentParser()

    # hyperparameters sent by the client are passed as command-line arguments to the script
    parser.add_argument('--epochs', type=int, default=1)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--learning_rate', type=float, default=0.1)

    # data directories
    parser.add_argument('--input', type=str, default=os.environ.get('SM_CHANNEL_INPUT'))

    # model directory
    parser.add_argument('--sm-model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))

    return parser.parse_known_args()


def get_train_data(data_dir):

    X_train = np.load(os.path.join(data_dir, 'X_train.npy'))
    y_train = np.load(os.path.join(data_dir, 'y_train.npy'))
    print('X train', X_train.shape,'y train', y_train.shape)

    return X_train, y_train


def get_test_data(data_dir):

    X_test = np.load(os.path.join(data_dir, 'X_test.npy'))
    y_test = np.load(os.path.join(data_dir, 'y_test.npy'))
    print('X test', X_test.shape,'y test', y_test.shape)

    return X_test, y_test


if __name__ == "__main__":

    args, _ = parse_args()

    print('Data location: {}'.format(args.input))
    X_train, y_train = get_train_data(args.input)
    X_test, y_test = get_test_data(args.input)

    device = '/cpu:0'
    print(device)
    batch_size = args.batch_size
    epochs = args.epochs
    learning_rate = args.learning_rate
    print('batch_size = {}, epochs = {}, learning rate = {}'.format(batch_size, epochs, learning_rate))

    with tf.device(device):

        model = get_model()
        optimizer = tf.keras.optimizers.SGD(learning_rate)
        model.compile(optimizer=optimizer, loss='mse')
        model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs,
                  validation_data=(X_test, y_test))

        # evaluate on test set
        scores = model.evaluate(X_test, y_test, batch_size, verbose=2)
        print("\nTest MSE :", scores)

        # save model
        model.save(args.sm_model_dir + '/1')

