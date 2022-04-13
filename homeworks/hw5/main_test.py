import unittest

import main
import main as p
from unittest.mock import patch


class MyTestCase(unittest.TestCase):
    def test_public_cases(self):
        for i in range(1, 11):
            i = str(i).zfill(2)
            pub_in = "datapub/pub" + i + ".in"
            # print(pub_in)
            with open(pub_in, "r") as f:
                with patch('builtins.input', side_effect=f):
                    blob = main.PGEBinaryTree()
            pub_out = "datapub/pub" + i + ".out"
            with open(pub_out, "r") as f:
                result = f.read()
                # print(blob.get_optimal_pairs())
                # print(result)
                self.assertEqual(blob.get_optimal_pairs(), result)


if __name__ == '__main__':
    unittest.main()
