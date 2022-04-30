import unittest

import main
from unittest.mock import patch
from main import read_input


class MyTestCase(unittest.TestCase):
    def test_public_cases(self):
        for i in range(1, 11):
            i = str(i).zfill(2)
            pub_in = "datapub/pub" + i + ".in"
            # print(pub_in)
            with open(pub_in, "r") as f:
                with patch('builtins.input', side_effect=f):
                    tree = read_input()
                    tree.set_LER()
            pub_out = "datapub/pub" + i + ".out"
            with open(pub_out, "r") as f:
                result = f.read()
                # print(blob.get_optimal_pairs())
                # print(result)
                print("testing ", pub_in)
                self.assertEqual(tree.get_LER(), result)


if __name__ == '__main__':
    unittest.main()
