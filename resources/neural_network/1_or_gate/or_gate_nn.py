import unittest

#       _______
#  A -- |       \
#       |       |----- Y
#  B -- |______/
#
#  f(x) = {
#           1 if SUM(w_i * x_i) > 0;
#           0 otherwise
#         }
def or_gate(x):
    y = 0
    for i in x:
        y += i
    return (y > 0)

def update_or_gate_weights(w):
    w[0]

# Here's our "unit tests".
class two_input_or_gate_tests(unittest.TestCase):

    def test_both_false(self):
        # set up expectations
        x = [0,0]
        w = [0,0]
        self.assertFalse(or_gate(x))

        # call function under test
        update_or_gate_weights(w)

        # Test that weights are not updated
        self.assertFalse(w[0])
        self.assertFalse(w[1])

    def test_both_true(self):
        # set up expectations
        x = [1,1]
        w = [0,0]
        self.assertTrue(or_gate(x))

        # call function under test
        update_or_gate_weights(w)

        # Test that weights are updated
        self.assertFalse(w[0])
        self.assertFalse(w[1])

    def test_A_true(self):
        x = [0,1]
        self.assertTrue(or_gate(x))

    def test_B_true(self):
        x = [1,0]
        self.assertTrue(or_gate(x))

    def test_3_true_inputs(self):
        x = [1,1,1]
        self.assertTrue(or_gate(x))

    def test_3_true_1_false_inputs(self):
        x = [1,1,0,1]
        self.assertTrue(or_gate(x))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
