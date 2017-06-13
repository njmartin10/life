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

# Here's our "unit tests".
class two_input_or_gate_tests(unittest.TestCase):

    def test_both_false(self):
        x = [0,0]
        self.assertFalse(or_gate(x))

    def test_both_true(self):
        x = [1,1]
        self.assertTrue(or_gate(x))

    def test_A_true(self):
        x = [0,1]
        self.assertTrue(or_gate(x))

    def test_B_true(self):
        x = [1,0]
        self.assertTrue(or_gate(x))

    def test_weights(self):
        self.fail("Dont forget about me!")



def main():
    unittest.main()

if __name__ == '__main__':
    main()
