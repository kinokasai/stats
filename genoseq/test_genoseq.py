import unittest
from unittest import TestCase
from genoseq import *

class TestGenoseq(TestCase):
    def test_read_fasta(self):
        l = read_fasta("sequences/ACTG.seq")
        expected = [[0, 1, 3, 2]]
        self.assertEqual(l, expected)

    def test_ctn(self):
        l = ['A', 'T', 'T', 'C', 'G', 'D']
        expected = [0, 3, 3, 1, 2, -1]
        l = [ctn(char) for char in l]
        self.assertEqual(l, expected)

    def test_ntc(self):
        l = [0, 2, 2, -1, 3, 1]
        expected = ['A', 'G', 'G', '_', 'T', 'C']
        l = [ntc(num) for num in l]
        self.assertEqual(l, expected)

    def test_count_letters(self):
        l = [0, 2, 2, 1, 3]
        expected = (1, 1, 2, 1)
        out = count_letters(l)
        self.assertEqual(out, expected)
        l = stnl('GATTACAACT')
        expected = (4, 2, 1, 3)
        out = count_letters(l)
        self.assertEqual(out, expected)

    def test_freq_letters(self):
        l = stnl('GATTACAACT')
        expected = (4/10, 2/10, 1/10, 3/10)
        out = freq_letters(l)
        self.assertEqual(out, expected)

    def test_logprob(self):
        l = stnl('CAT')
        model = (0.2, 0.3, 0.1, 0.4)
        expected = -3.7297
        out = logprob(l, model)
        self.assertAlmostEqual(out, expected, places=4)

    def test_flogprob(self):
        tpl = count_letters(stnl('CAT'))
        model = (0.2, 0.3, 0.1, 0.4)
        expected = -3.7297
        out = flogprob(tpl, model)
        self.assertAlmostEqual(out, expected, places=4)

    def test_simul_seq(self):
        model = (1.0, 0.0, 0.0, 0.0)
        expected = [0, 0, 0, 0, 0]
        out = simul_seq(5, model)
        self.assertEqual(out, expected)
        model = (0.0, 0.0, 1.0, 0.0)
        expected = [2, 2, 2, 2, 2]
        out = simul_seq(5, model)
        self.assertEqual(out, expected)
        model = (0.8, 0.1, 0.0, 0.1)
        out = simul_seq(1000, model)
        cnt_out = count_letters(out)
        self.assertEqual(cnt_out[2], 0)
        self.assertGreater(cnt_out[0], cnt_out[1] + cnt_out[2])

if __name__ == '__main__':
    unittest.main()
