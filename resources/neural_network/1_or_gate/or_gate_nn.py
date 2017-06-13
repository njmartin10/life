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
def or_gate(a, b):
    return 0

# Here's our "unit tests".
class or_gate_tests(unittest.TestCase):

    def test_both_false(self):
        self.assertFalse(or_gate(0,0))

    def test_both_true(self):
        self.assertTrue(or_gate(1,1))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
