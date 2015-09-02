
import unittest
from binomial_trees import BinomialTree
from black_scholes import OptionType


class BinomialTreeTestCase(unittest.TestCase):

    def test_basic(self):
        '''European option, spot price 50, strike price 52, risk free interest rate 5%
        expiry 2 years, volatility 30%
        '''
        bt = BinomialTree(50, 52, 0.05, 2, 0.3, steps=100)
        self.assertEqual(6.7781, # steps = 100
                         bt.get_option_price(OptionType.PUT))
        

if __name__ == '__main__':
    unittest.main()