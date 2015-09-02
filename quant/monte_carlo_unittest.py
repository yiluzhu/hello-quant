from unittest import TestCase, main
import time

from monte_carlo import MonteCarlo
from option import OptionType


class MonteCarloTestCase(TestCase):
    
    def setUp(self):
        self.t0 = time.time()

    def test_eu_call_opt(self):
        '''2-year European put option, spot price 50, strike 52
        risk-free rate 5%, volatility 30%
        '''
        mc = MonteCarlo(50, 52, 0.05, 2, 0.3)
        self.assertAlmostEqual(6.7601, mc.run(OptionType.PUT, 300000, 0), 1) # single process

    def test_eu_call_opt_with_mp(self):
        '''Run the same test but in multiprocess mode
        '''
        mc = MonteCarlo(50, 52, 0.05, 2, 0.3)
        self.assertAlmostEqual(6.7601, mc.run(OptionType.PUT, 300000, 4), 1) # 4 processes seems to be the fastest on a quad-core pc

    def tearDown(self):
        print '{} takes {} seconds'.format(self.__str__(), time.time() - self.t0)

if __name__ == '__main__':
    main()
