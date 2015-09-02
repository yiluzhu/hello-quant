'''
Delta: changes in the underlying asset price

    delta_call = exp((b - r) * T) * N(d1)         > 0
    delta_put  = exp((b - r) * T) * (N(d1) - 1)   < 0
    
    where 
        b: is cost of carry
        r: risk free interest rate
'''

from black_scholes import BlackScholes
from option import OptionType, OptionTypeError, cdf
from math import exp

class BlackScholesGreeks(BlackScholes):
    
    def get_delta_greeks(self, otype, round_digit=4):
        if otype == OptionType.CALL:
            delta = exp((self.cost_of_carry - self.rate) * self.expiry) * cdf(self.get_d1_d2()[0])
        elif otype == OptionType.PUT:
            delta = exp((self.cost_of_carry - self.rate) * self.expiry) * (cdf(self.get_d1_d2()[0]) - 1)
        else:
            raise OptionTypeError

        return round(delta, round_digit)

