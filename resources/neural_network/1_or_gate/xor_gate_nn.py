#!/usr/local/bin/python
import unittest
from random import choice
from numpy import array, dot, random
import matplotlib.pyplot as plt


#       _______
#  A -- \\      \
#       ||       |----- Y
#  B -- //______/
#
#  f(x) = {
#           1 if SUM(w_i * x_i) > 0;
#           0 otherwise
#         }
# Be able to discuss what you understand of this and what are it's limitations

unit_step_prediction = lambda x: 0 if x < 0 else 1


w = random.rand(3)
errors = []
eta = 0.2
n = 100

def train(training_data, w):
    for i in xrange(n):
        x, expected = choice(training_data)
        result = dot(w, x)
        error = expected - unit_step_prediction(result)
        errors.append(error)
        w += eta * error * x

def print_data(training_data, w):
    print ""
    for x, _ in training_data:
        result = dot(x, w)
        print("{}: {} -> {}".format(x[:2], result, unit_step_prediction(result)))

    fig1 = plt.figure()
    plt.plot(errors)

    # plt.show()

def check_data(training_data, w, self):
    for x, _ in training_data:
        result = dot(x, w)
        self.assertEquals(_, unit_step_prediction(result))


# Here's our unit tests
class two_input_xor_gate_tests(unittest.TestCase):
    def setUp(self):
        w = random.rand(3)

    def test_or_gate(self):
        training_data = [
            (array([0,0,1]), 0),
            (array([0,1,1]), 1),
            (array([1,0,1]), 1),
            (array([1,1,1]), 1),
        ]

        train(training_data, w)

        print_data(training_data, w)
        check_data(training_data, w, self)


    def test_and_gate(self):
        training_data = [
            (array([0,0,1]), 0),
            (array([0,1,1]), 0),
            (array([1,0,1]), 0),
            (array([1,1,1]), 1),
        ]

        train(training_data, w)

        print_data(training_data, w)
        check_data(training_data, w, self)

    def test_xor_gate(self):
        training_data = [
            (array([0,0,1]), 0),
            (array([0,1,1]), 1),
            (array([1,0,1]), 1),
            (array([1,1,1]), 0),
        ]

        train(training_data, w)

        print_data(training_data, w)
        check_data(training_data, w, self)

    def test_nand_gate(self):
        training_data = [
            (array([0,0,1]), 1),
            (array([0,1,1]), 1),
            (array([1,0,1]), 1),
            (array([1,1,1]), 0),
        ]

        train(training_data, w)

        print_data(training_data, w)
        check_data(training_data, w, self)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
