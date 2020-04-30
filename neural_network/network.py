import numpy as np
import random
import json
import datetime
import time
import pickle
import os
import logging
from IPython.display import display, clear_output

logger = logging.getLogger(' FILE MANAGER📂')
logger.setLevel(logging.INFO)


def sig(x):
    return 1/(1 + np.exp(-x))


def d_sig(x):
    return np.exp(-x)/((np.exp(-x)+1)**2)


class network:
    def __init__(self, shape, w_spread=1, b_spread=1):
        self.shape = shape
        self.layers = len(shape)
        self.nodes = np.array([np.ndarray([col, 1]) for col in shape])
        self.z = self.nodes.copy()
        self.weights = np.array([2*(np.random.random([shape_f, shape_i]) - 0.5)
                                 * w_spread for shape_i, shape_f in zip(shape, shape[1:])])
        self.biases = np.array(
            [2*(np.random.random([col, 1]) - 0.5)*b_spread for col in shape[1:]])

    def run(self, input):
        """
        Runs the neural network for a desired input
        :input numpy.ndarray: Array of the shape of the first layer

        :return: numpy.ndarray of the result in the shape of the last layer 
        """
        input = np.array(input)
        if input.shape != self.nodes[0].shape:
            raise Exception(
                f'Input shape does not match the input shape of the network!\n {input.shape} should be {self.nodes[0].shape}')
        self.nodes[0] = input

        for i in range(self.layers - 1):
            self.z[i+1] = self.weights[i] @ self.nodes[i] + self.biases[i]
            self.nodes[i+1] = sig(self.z[i+1])

        return self.nodes[-1]

    def cost(self, input, target):
        """
        Calculate the cost function for a given input and desired target.
        :input:  numpy.ndarray() of the size of the first layer
        :target: numpy.ndarray() of the size of the last layer

        :return float: The value of the cost function 
        """
        target = np.array(target)
        result = self.run(input)
        cost = np.sum((result - target)**2)

        return cost

    def cost_grad(self, input, target):
        """
        Return the gradient of the cost function of the input for a specific input and desired target.
        :input:  numpy.ndarray() of the size of the first layer
        :target: numpy.ndarray() of the size of the last layer

        :return: Dictionary with the gradient of each weight and bias
        """
        grad_bias = np.array([np.ndarray([shape, 1])
                              for shape in self.shape[1:]])
        grad_weight = np.array([np.ndarray([shape_f, shape_i])
                                for shape_i, shape_f in zip(self.shape, self.shape[1:])])

        result = self.run(input)

        delta = self.nodes.copy()
        delta[-1] = (result - target) * d_sig(self.z[-1])

        for l in reversed(range(self.layers - 1)):
            delta[l] = (self.weights[l].T@delta[l+1]) * d_sig(self.z[l])

        grad_bias = delta[1:]
        # grad_weight[:-1] = delta[1:] * self.nodes[:-1].T
        for l in range(self.layers - 1):
            grad_weight[l] = delta[l+1] * self.nodes[l].T

        grad = {
            0: grad_weight,
            1:   grad_bias
        }
        return grad

    def grad_descent(self, data, learning_rate=0.1, batch_size=64, batch_num=10):
        """
        Train your neural network using stochastic gradient decsent.
        :data list(dict): List of dictionaries containing the images and labels. Dictionary of the form 
        data = {
            "image": np..ndarray([size of initial layer])
            "label": np.ndarray([10])
        }
        :learning_rate float: Proportional to the gradient descent step size
        :batch_size int:      Number of images to be sampled randomly from the full data set each batch
        :batch_num int:       Number of batches

        :return: Dict with the biases and weights of the optimized network. {'biases': ..., 'weights': ...}
        """
        for i in range(batch_num):
            batch = random.sample(data, batch_size)
            for bat in batch:
                grad = self.cost_grad(bat["image"], bat["label"])

                self.weights -= grad[0]*(learning_rate/batch_size)
                self.biases -= grad[1]*(learning_rate/batch_size)
            clear_output(wait=True)
            N = 40
            prog = int(N*float(i+1)/batch_num)
            print('👉 Batch ', i+1, '/', batch_num,
                  '\n[' + '⬛'*prog + '⬜'*(N-prog) + ']')
        parameters = {
            "biases":  self.biases,
            "weights": self.weights
        }

        time.sleep(0.1)
        # --- Save to file ---
        if not os.path.exists('data'):
            os.makedirs('data')
        date_str = str(datetime.datetime.now())[:16].replace(' ', '_').replace(':','-')
        file_str = 'data\\' + date_str + '_params.pkl'
        logger.info(f'Saving parameter data to: {file_str}')
        f = open(file_str, "wb")
        pickle.dump(parameters, f)
        f.close()

        return parameters

# i_size = 748
# t_size = 10
# n    = network([i_size,16,16,t_size])
# data = []
# for _ in range(100):
#     init   = np.random.random([i_size,1])
#     target = np.random.random([t_size,1])
#     data.append({
#         'label': target,
#         'image': init
#     })

# params = n.grad_descent(data)


# n = network([784, 16, 16, 10])

# # init = np.array([[1],
# #                  [2],
# #                  [3]])
# # target = np.array([[1],
# #                    [0],
# #                    [0]])
# init = np.random.random([784,1])
# target = np.array([[1],  # 0
#                    [0],  # 1
#                    [0],  # 2
#                    [0],  # 3
#                    [0],  # 4
#                    [0],  # 5
#                    [0],  # 6
#                    [0],  # 7
#                    [0],  # 8
#                    [0]]) # 9
# n.cost(init, target)

# n.cost_grad(init, target)

# print('Initial col:\n', self.nodes[i])
# print('Weights:\n'    , self.weights[i])
# print('Biases:\n'     , self.biases[i])
# print('result:\n'     , col)
# print('-------------------------------')
