'''
For each path of simulation, the final price is:

    St = spot * exp((b - vol*vol/2) * T + vol * rand * sqrt(T))
    where rand is a random number in (0, 1)

    call option:
        each_price = max(St - strike, 0)
    put option: 
        each_price = max(strike - St, 0)

The overall price is:
    sum(each_price) * exp(rate * T) / simu_num

'''
from math import exp, sqrt
from random import random

from option import Option, OptionType, OptionTypeError, norminv


class MonteCarlo(Option):
    def __init__(self, spot, strike, rate, expiry, vol, coc=None):
        super(MonteCarlo, self).__init__(spot, strike, rate, expiry, vol)
        
        self.cost_of_carry = coc if coc else rate
    
    def get_price_of_one_run(self, z):
        '''Run the simulation once and return the option price'''
        st = self.spot * exp((self.cost_of_carry - self.vol**2 / 2) * self.expiry + self.vol * norminv(random()) * sqrt(self.expiry))
        return max(z * (st - self.strike), 0)
    
    def _ps_slice(self, z, num, resultq):
        sum_ = 0
        for i in xrange(num):
            sum_ += self.get_price_of_one_run(z)
            
        resultq.put(sum_)
        resultq.close()
    
    def run(self, opt_type, simu_num, ps_num=10):
        '''
        simu_num: the number of simulation runs, usually > 100000
        ps_num: If zero, run simulation in single process mode;
                otherwise run in multiprocess mode with ps_num processes to speed up 
        '''
        if opt_type == OptionType.CALL:
            z = 1
        elif opt_type == OptionType.PUT:
            z = -1
        else:
            raise OptionTypeError

        sum_ = 0
        # single process mode
        for i in xrange(simu_num):
            sum_ += self.get_price_of_one_run(z)

        return round(exp(- self.rate * self.expiry) * sum_ / simu_num, 4)
