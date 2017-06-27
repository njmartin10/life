import numpy as np
import random
from keras.layers import Input, GRU, Embedding, Dense, Activation, Dropout
from keras.layers import merge, Permute, TimeDistributed, Lambda, Reshape, Bidirectional
from keras.layers.merge import dot, add, concatenate
from keras.models import Model, load_model, save_model
from keras.utils import plot_model
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam, Adagrad, Adamax, Nadam
from keras.preprocessing.sequence import pad_sequences


class DQN(object):
    def __init__(self, n_sensors, n_actions, train_frames=100000, batch_size=32, train=True):
        self.n_sensors = n_sensors
        self.n_actions = n_actions
        self.train_frames = train_frames
        self.batch_size = batch_size
        self.train = train
        if self.train:
            self.model = self.action_value_f()
            self.model.compile(loss="mean_squared_error", optimizer="rmsprop")

        self.t = 0
        self.replay_buffer_length = 100
        self.replay_buffer = []
        self.last_state = None
        self.last_action = None

    def save_model(self):
        pass

    def load_model(self):
        pass

    def action_value_f(self):
        input = Input(shape=(self.n_sensors,), name="input")
        x = Dense(units=32, activation="relu", kernel_initializer="lecun_uniform", name="layer_1")(input)
        x = Dropout(rate=0.2)(x)
        x = Dense(units=16, activation="relu", kernel_initializer="lecun_uniform", name="layer_2")(x)
        x = Dropout(rate=0.2)(x)
        output = Dense(units=self.n_actions, kernel_initializer="lecun_uniform", name="output")(x)
        return Model(inputs=input, outputs=output)

    def process_minibatch(self, minibatch):
        """This does the heavy lifting, aka, the training. It's super jacked."""
        X_train = []
        y_train = []
        # Loop through our batch and create arrays for X and y
        # so that we can fit our model at every step.
        for memory in minibatch:
            # Get stored values.
            old_state_m, action_m, reward_m, new_state_m = memory
            # Get prediction on old state.
            old_qval = self.model.predict(old_state_m, batch_size=1)
            # Get prediction on new state.
            newQ = self.model.predict(new_state_m, batch_size=1)
            # Get our best move. I think?
            maxQ = np.max(newQ)
            y = np.zeros((1, 3))
            y[:] = old_qval[:]
            # Check for terminal state.
            # TODO : health == 0 --> big negative reward
            if reward_m != -500:  # non-terminal state
                update = (reward_m + (GAMMA * maxQ))
            else:  # terminal state
                update = reward_m
            # Update the value for the action we took.
            y[0][action_m] = update
            X_train.append(old_state_m.reshape(self.n_sensors,))
            y_train.append(y.reshape(self.n_actions,))

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        return X_train, y_train

    def run_train(self, sensors_values, rewards):
        self.t += 1

        # Experience replay storage.
        self.replay_buffer.append((self.last_state, self.last_action, rewards, sensors_values))

        # Choose an action.
        if self.t < self.replay_buffer_length:
            action = np.random.randint(0, self.n_actions)  # random
            #print "\nTimestep {0} :\naction --> {1}\nprob --> {2}".format(self.t, action, "none")
        else:
            # Get Q values for each action.
            #print sensors_values.shape
            qval = self.model.predict(sensors_values, batch_size=1)
            action = (np.argmax(qval))
            #print "\nTimestep {0} :\naction --> {1}\nprob --> {2}".format(self.t, action, qval)

        if len(self.replay_buffer) > self.replay_buffer_length:
            #print ("Replay memory full")
            self.replay_buffer.pop(0)

        if self.t > self.replay_buffer_length:
            # Randomly sample our experience replay memory
            minibatch = random.sample(self.replay_buffer, self.batch_size)

        self.last_state = sensors_values
        self.last_action = action

        return action

    def run_test(self):
        pass