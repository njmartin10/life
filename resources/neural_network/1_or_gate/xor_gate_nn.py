import unittest

#       _______
#  A -- \       \
#        |      |----- Y
#  B -- /______/
#
#  f(x) = {
#           1 if SUM(w_i * x_i) > 0;
#           0 otherwise
#         }
def xor_gate(x,w):
    y = 0
    for i in x:
        for j in w:
            y += i*j
    return (y > 0)

def train_agent(x,w,d):
    for i in range(len(x)):
        w[i] = x[i] * (d - w[i])

# Here's our unit tests
class two_input_xor_gate_tests(unittest.TestCase):

    def test_both_false(self):
        # set up expectations
        x = [0,0]
        w = [0,0]
        d = 0

        # call function under test
        self.assertFalse(xor_gate(x,w))

        train_agent(x,w,d)

        # Test that weights are not updated
        self.assertFalse(w[0])
        self.assertFalse(w[1])

        # ensure agent still gets it right after training
        self.assertFalse(xor_gate(x,w))

    def test_both_false(self):
        # set up expectations
        x = [1,1]
        w = [0,0]
        d = 0

        # initially agent gets it wrong
        self.assertTrue(xor_gate(x,w))

        train_agent(x,w,d)

        # Test that weights are updated as expected
        # self.assertTrue(w[0])
        # self.assertTrue(w[1])

        # then agent "learns"
        self.assertFalse(xor_gate(x,w))

    def test_A_true(self):
        # set up expectations
        x = [0,1]
        w = [0,0]
        d = 1

        # initially agent gets it wrong
        self.assertFalse(xor_gate(x,w))

        train_agent(x,w,d)

        # Test that weights are updated
        self.assertFalse(w[0])
        self.assertTrue(w[1])

        # then agent "learns"
        self.assertTrue(xor_gate(x,w))

    def test_B_true(self):
        # set up expectations
        x = [1,0]
        w = [0,0]
        d = 1

        # initially agent gets it wrong
        self.assertFalse(xor_gate(x,w))

        train_agent(x,w,d)

        # Test that weights are updated
        self.assertTrue(w[0])
        self.assertFalse(w[1])

        # then agent "learns"
        self.assertTrue(xor_gate(x,w))

    def test_3_true_inputs(self):
        # set up expectations
        x = [1,1,1]
        w = [0,0,0]
        d = 1

        # initially agent gets it wrong
        self.assertFalse(xor_gate(x,w))

        train_agent(x,w,d)

        # Test that weights are updated
        self.assertTrue(w[0])
        self.assertTrue(w[1])
        self.assertTrue(w[2])

        # then agent "learns"
        self.assertTrue(xor_gate(x,w))

    def test_3_true_1_false_inputs(self):
        # set up expectations
        x = [1,1,0,1]
        w = [0,0,0,0]
        d = 1

        # initially agent gets it wrong
        self.assertFalse(xor_gate(x,w))

        train_agent(x,w,d)

        # Test that weights are updated
        self.assertTrue(w[0])
        self.assertTrue(w[1])
        self.assertFalse(w[2])
        self.assertTrue(w[3])

        # then agent "learns"
        self.assertTrue(xor_gate(x,w))

    def test_two_floats(self):
        # set up expectations
        x = [0.1,0]
        w = [0,0]
        d = 1

        # initially agent gets it wrong
        self.assertFalse(xor_gate(x,w))

        train_agent(x,w,d)

        # Test that weights are updated
        self.assertEquals(w[0], 0.1)
        self.assertEquals(w[1], 0)

        # then agent "learns"
        self.assertTrue(xor_gate(x,w))

    def test_4_vectors_of_floats(self):
        # First Vector
        # set up expectations
        x = [0.1,0]
        w = [0,0]
        d = 1

        # initially agent gets it wrong
        self.assertFalse(xor_gate(x,w))

        train_agent(x,w,d)

        # Test that weights are updated
        self.assertEquals(w[0], 0.1)
        self.assertEquals(w[1], 0)

        # then agent "learns"
        self.assertTrue(xor_gate(x,w))

        # Second Vector
        x = [0,0.1]
        # w = [0,0] # keep the same weights as before!
        d = 1

        # test agent
        self.assertTrue(xor_gate(x,w))

        # Third Vector
        x = [0,0]
        # w = [0,0] # keep the same weights as before!
        d = 0

        # test agent
        self.assertFalse(xor_gate(x,w))

        # Fourth Vector
        x = [9.0,0.5]
        # w = [0,0] # keep the same weights as before!
        d = 1

        # test agent
        self.assertTrue(xor_gate(x,w))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
