# [Imports]========================================================================================================================================[Imports]
import numpy as np
import scipy.sparse
import tensorflow as tf
import argparse
from NQTM import NQTM

import other_module as otherModule # Other needed functions


# [Declarations & Initializations]==========================================================================================[Declarations & Initializations]
args = None
input_dir = "d_input"
output_dir = "d_output"

# [Functions]====================================================================================================
def init_parser():
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument('--layer1', type=int, default=100)
    parser.add_argument('--layer2', type=int, default=100)
    parser.add_argument('--batch_size', type=int, default=40)
    parser.add_argument('--topic_num', type=int, default=10)
    parser.add_argument('--learning_rate', type=float, default=0.00005)
    parser.add_argument('--keep_prob', type=float, default=1.0)
    parser.add_argument('--epoch', type=int, default=16)
    parser.add_argument('--word_sample_size', type=int, default=10)
    parser.add_argument('--word_sample_epoch', type=int, default=40)
    parser.add_argument('--omega', type=float, default=1.0)
    parser.add_argument('--commitment_cost', type=float, default=0.1)
    parser.add_argument('--test_index', type=int, default=1)
    
    args = parser.parse_args()

def load_data():
    train_data = scipy.sparse.load_npz(otherModule.define_relativepath(False,"\\{}\\bow_matrix.npz".format(input_dir))).toarray()
    vocab = list()
    with open(otherModule.define_relativepath(False,"\\{}\\vocab.txt".format(input_dir))) as file:
        for line in file:
            vocab.append(line.strip())
    return train_data, vocab

def create_minibatch(data):
    rng = np.random.RandomState(10)
    while True:
        ixs = rng.randint(data.shape[0], size=args.batch_size)
        yield data[ixs]

def print_top_words(beta, feature_names, n_top_words=15):
    top_words = list()
    for i in range(len(beta)):
        top_words.append(" ".join([feature_names[j] for j in beta[i].argsort()[:-n_top_words - 1:-1]]))
        # print(top_words[-1])

    with open(otherModule.define_relativepath(True,"\\{}\\top_words_T{}_K{}_{}th.txt".format(output_dir, n_top_words, args.topic_num, args.test_index)), 'w') as file:
        for line in top_words:
            file.write(line + '\n')

def print_topic_words(beta, theta, feature_names, n_topic_selection=1, n_top_words=1):
    top_words = list()
    doc_topic_word = list()

    for i in range(len(beta)):
        top_words.append(" ".join([feature_names[j] for j in beta[i].argsort()[:-n_top_words - 1:-1]]))
    for i in range(len(theta)):
        doc_topic_word.append(" ".join([top_words[j] for j in theta[i].argsort()[:-n_topic_selection - 1:-1]]))

    with open(otherModule.define_relativepath(True,"\\{}\\topic_words_T{}_K{}_{}th.txt".format(output_dir, n_top_words, args.topic_num, args.test_index)), 'w') as file:
        for line in doc_topic_word:
            file.write(line + '\n')

def get_theta(model, x):
    data_size = x.shape[0]
    batch_size = args.batch_size
    train_theta = np.zeros((data_size, args.topic_num))
    for i in range(int(data_size / batch_size)):
        start = i * batch_size
        end = (i + 1) * batch_size
        data_batch = x[start:end]
        train_theta[start:end] = model.sess.run(model.theta_e, feed_dict={model.x: data_batch})
    train_theta[-batch_size:] = model.sess.run(model.theta_e, feed_dict={model.x: x[-batch_size:]})
    return train_theta

def train(model, train_data, vocab, config):
    total_batch = int(train_data.shape[0] / args.batch_size)
    minibatches = create_minibatch(train_data)
    op = [model.train_op, model.loss]

    for epoch in range(args.epoch):
        omega = 0 if epoch < config['word_sample_epoch'] else 1.0
        train_loss = list()
        for i in range(total_batch):
            batch_data = minibatches.__next__()
            feed_dict = {model.x: batch_data, model.w_omega: omega}
            _, batch_loss = model.sess.run(op, feed_dict=feed_dict)
            train_loss.append(batch_loss)

        print('Epoch: ', '{:03d} loss: {:.3f}'.format(epoch + 1, np.mean(train_loss)))

    beta = model.sess.run((model.beta))
    # print_top_words(beta, vocab)

    train_theta = get_theta(model, train_data)

    print_topic_words(beta, train_theta, vocab)
    np.save(otherModule.define_relativepath(True,"\\{}\\theta_K{}_{}th".format(output_dir, args.topic_num, args.test_index)), train_theta)
    np.save(otherModule.define_relativepath(True,"\\{}\\beta_K{}_{}th".format(output_dir, args.topic_num, args.test_index)), beta)

def run_main():
    # tf.compat.v1.reset_default_graph() # Clears default graph and resets global default graph; Not Working
    tf.keras.backend.clear_session() # Deletes models and layers previously created

    config = dict()
    config.update(vars(args))
    config['active_fct'] = tf.nn.softplus

    train_data, vocab = load_data()
    config['vocab_size'] = len(vocab)
    model = NQTM(config=config)
    train(model, train_data, vocab, config)

