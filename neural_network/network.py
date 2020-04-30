import numpy as np
import random
import json
import datetime
import time
from IPython.display import display, clear_output

def sig(x):
    return 1/(1 + np.exp(-x))

def d_sig(x):
    return np.exp(-x)/((np.exp(-x)+1)**2)

class network:
    def __init__(self, shape, w_spread=1, b_spread=1):
        self.shape   = shape
        self.layers  = len(shape)
        self.nodes   = np.array([np.ndarray([col,1]) for col in shape])
        self.z       = self.nodes.copy()
        self.weights = np.array([2*(np.random.random([shape_f, shape_i]) - 0.5)*w_spread for shape_i, shape_f in zip(shape, shape[1:])])
        self.biases  = np.array([2*(np.random.random([col,1]) - 0.5)*b_spread for col in shape[1:]])
    
    def run(self, input):
        input = np.array(input)
        if input.shape != self.nodes[0].shape:
            raise Exception(f'Input shape does not match the input shape of the network!\n {input.shape} should be {self.nodes[0].shape}')
        self.nodes[0] = input
        
        for i in range(self.layers - 1):
            self.z[i+1] = self.weights[i] @ self.nodes[i] + self.biases[i]
            self.nodes[i+1] = sig(self.z[i+1])
        
        return self.nodes[-1]

    def run_u(self, input):
        nodes = self.nodes.copy()
        nodes[0] = np.array(input)
        for i in range(self.layers - 1):
            nodes[i+1] = sig(self.weights[i] @ nodes[i] + self.biases[i])

        return nodes[-1]

    def cost(self, input, target):
        target = np.array(target)
        result = self.run(input)
        cost = np.sum((result - target)**2)
        # print("--> ", self.nodes[0])
        # print('\nThe result is: \n', result)
        # print('\nThe cost is: ', cost)
        
        return cost

    def cost_grad(self, input,target):
        grad_bias   = np.array([np.ndarray([shape, 1]) for shape in self.shape[1:]])
        grad_weight = np.array([np.ndarray([shape_f, shape_i]) for shape_i, shape_f in zip(self.shape, self.shape[1:])])

        result = self.run(input)

        delta = self.nodes.copy()
        delta[-1] = (result - target) * d_sig(self.z[-1])

        for l in reversed(range(self.layers - 1)):
            delta[l] = (self.weights[l].T@delta[l+1])* d_sig(self.z[l])

        grad_bias = delta[1:]
        # grad_weight[:-1] = delta[1:] * self.nodes[:-1].T
        for l in range(self.layers - 1):
            grad_weight[l] = delta[l+1] * self.nodes[l].T


        grad = {
            0: grad_weight,
            1:   grad_bias
        }
        return grad

    def grad_descent(self, data, learning_rate=0.1, batch_size=5, repeat=10):
        for i in range(repeat):
            print('', end='\r')
            batch = random.sample(data, batch_size)
            # itime = time.time()
            for bat in batch:
                grad = self.cost_grad(bat["image"], bat["label"])
                self.weights -= grad[0]*(learning_rate/batch_size)
                self.biases  -= grad[1]*(learning_rate/batch_size)
                # print('\nS: ', self.weights.shape)
                # print('\nA: ', grad['bias'].shape)
                # print('\n👉 Before: \n',self.weights[1])
                # print('\n👉 After:\n ', self.weights[1])
                # print(i)
            # print(f'batch time: {str(time.time()-itime)[0:5]} sec')
            # print('', end='\r')
            clear_output(wait=True)
            N = 56
            prog = int(N*float(i+1)/repeat)
            print('👉 Batch ', i+1, '/', repeat, '\n[' + '⬛'*prog + '⬜'*(N-prog) + ']')
        parameters = {
            "biases":  self.biases,
            "weights": self.weights
        }
        # js = json.dumps(parameters)
        # date_str = str(datetime.datetime.now())[:16]
        # f = open(f'data\\{date_str}\\parameters.json', 'w')
        # f.write(js)
        # f.close()
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