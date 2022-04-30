import unittest

import main
from unittest.mock import patch
from main import load_input


class MyTestCase(unittest.TestCase):
    def test_public_cases(self):
        for i in range(1, 11):
            i = str(i).zfill(2)
            pub_in = "datapub/pub" + i + ".in"
            # print(pub_in)
            with open(pub_in, "r") as f:
                with patch('builtins.input', side_effect=f):
                    tree = main.PGEBinaryTree(load_input())
                    tree.init_tree()
                    tree.go_trough_tree()
            pub_out = "datapub/pub" + i + ".out"
            with open(pub_out, "r") as f:
                result = f.read()
                # print(blob.get_optimal_pairs())
                # print(result)
                self.assertEqual(tree.get_solution(), result)


if __name__ == '__main__':
    unittest.main()
