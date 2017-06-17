import unittest
import random

#       _______
#  A -- \\      \
#       ||       |----- Y
#  B -- //______/
#
#  f(x) = {
#           1 if SUM(w_i * x_i) > 0;
#           0 otherwise
#         }
def activation_fn(y,x,w):
    y = 0
    for i in range(len(x)):
        y += x[i] * w[i]
    return (y > 0)

def train_agent(x,w,d):
    for i in range(len(x)):
        w = x[i] * (d - w)

def train_or(w):
    x = [
        [1, 1],
    ]

    print
    print w

    d = [1]

    for i in range(len(x)):
        simple_train(x[i], w, d[i])

    print w
    print

def train_and(w):
    x = [
        [0, 0],
        [1, 0],
        [0, 1],
        [1, 1],
    ]

    print
    print w

    d = [0,0,0,1]

    for i in range(len(x)):
        simple_train(x[i], w, d[i])

    print w
    print
    return w


def simple_train(x, w, d):
    for i in range(len(x)):
        w[i] += x[i] * (d - w[i])

def check_test_activation(self, x,w,d):
    self.assertEquals(d, activation_fn(x, w))


# Here's our unit tests
class two_input_xor_gate_tests(unittest.TestCase):

    def test_both_false(self):

        x = [0, 0]

        w = [random.random(), random.random()]
        # w = [0, 0]

        d = 0

        print
        print w
        # simple_train(x, w, d)
        print w
        print

        check_test_activation(self, x, w, d)


    def test_both_true(self):

        x = [1, 1]

        # w = [random.random(), random.random()]
        w = [0, 0]

        d = 1

        print
        print w
        simple_train(x, w, d)
        print w
        print

        check_test_activation(self, x, w, d)

    def test_first_true(self):

        x = [1, 0]

        # w = [random.random(), random.random()]
        w = [0, 0]

        d = 1

        print
        print w
        simple_train(x, w, d)
        print w
        print

        check_test_activation(self, x, w, d)

    def test_second_true(self):

        x = [0, 1]

        # w = [random.random(), random.random()]
        w = [0, 0]

        d = 1

        print
        print w
        simple_train(x, w, d)
        print w
        print

        check_test_activation(self, x, w, d)

    def test_train_then_test_multiple_or(self):

        # initialize weights
        w = [0, 0]

        train_or(w)

        x = [
            [1, 0],
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
            [0, 1],
            [0, 0],
            [0.5, 0],
        ]

        d = [
            1,
            0,
            1,
            1,
            1,
            1,
            0,
            1,
        ]

        for i in range(len(x)):
            check_test_activation(self, x[i], w, d[i])

    def test_train_then_test_multiple_and(self):

        # initialize weights
        w = [0.1, 0.1]

        train_and(w)

        x = [
            [1, 0],
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
            [0, 1],
            [0, 0],
            [0.5, 0],
        ]

        d = [
            0,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
        ]

        for i in range(len(x)):
            print i
            check_test_activation(self, x[i], w, d[i])


def main():
    unittest.main()

if __name__ == '__main__':
    main()
