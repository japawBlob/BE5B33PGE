import unittest

import main
import main as p
from unittest.mock import patch


class MyTestCase(unittest.TestCase):
    def test_public_cases(self):
        for i in range(1, 14):
            i = str(i).zfill(2)
            pub_in = "datapub/pub" + i + ".in"
            # print(pub_in)
            with open(pub_in, "r") as f:
                with patch('builtins.input', side_effect=f):
                    blob = main.TripPlanner()
            pub_out = "datapub/pub" + i + ".out"
            with open(pub_out, "r") as f:
                result = f.read()
                # print(blob.get_optimal_pairs())
                # print(result)
                self.assertEqual(blob.get_optimal_pairs(), result)

    def test_correct_date(self):
        self.assertEqual(p.date_is_valid(1, 1), True)
        self.assertEqual(p.date_is_valid(31, 1), True)
        self.assertEqual(p.date_is_valid(32, 1), False)
        self.assertEqual(p.date_is_valid(1, 2), True)
        self.assertEqual(p.date_is_valid(30, 2), False)
        self.assertEqual(p.date_is_valid(38, 5), False)
        self.assertEqual(p.date_is_valid(50, 8), False)
        self.assertEqual(p.date_is_valid(11, 13), False)
        self.assertEqual(p.date_is_valid(5, 15), False)
        self.assertEqual(p.date_is_valid(1, 0), False)



if __name__ == '__main__':
    unittest.main()
