
''' 
 1. Black-Scholes formula for vanilla option without yield:
    
    c = S * N(d1) - X * exp(-rT) * N(d2)
    p = X * exp(-rT) * N(-d2) - S * N(-d1)
    where:
        d1 = (ln(S/X) + (r + vol*vol/2) * T) / (vol * sqrt(T))
        d2 = d1 - vol * sqrt(T)    
    
    while:
        c: call option price
        P: put option price
        S: spot price (stock current price)
        X: strike price
        r: risk-free interest rate
        T: time to expiration in years
        vol: volatility of the relative price change of the underlying stock price
        N(x): the cumulative normal distribution function
        exp(x): e to the x power 
 
    Note: 
        N(x) is given by integral and has no closed-form solution, so a numerical
        approximation must be used. Here we use Hart algorithm.

********************************************************************************
   
 2. Black-Scholes formula for vanilla option with yield:
    
    c = S * exp(-qT) * N(d1) - X * exp(-rT) * N(d2)
    p = X * exp(-rT) * N(-d2) - S * exp(-qT) * N(-d1)
    where:
        d1 = (ln(S/X) + (r - q + vol*vol/2) * T) / (vol * sqrt(T))
        d2 = d1 - vol * sqrt(T)    
    
    while:
        q: dividend yield

    Note:
        this is a more general case of formula 1, thus can be integrated easily 
        with formular 1.

********************************************************************************

 3. Black-Scholes formula for option on futures:
    
    c = F * exp(-rT) * N(d1) - X * exp(-rT) * N(d2)
    p = X * exp(-rT) * N(-d2) - F * exp(-rT) * N(-d1)
    where:
        d1 = (ln(F/X) + (vol*vol/2) * T) / (vol * sqrt(T))
        d2 = d1 - vol * sqrt(T)    
    
    while:
        F: future spot price

    Note:
        this is a special case of formula 2 where r == q

********************************************************************************

 4. Black-Scholes formula for FX option (currency option):
    
    Note:
        it is the same as formula 2 where q is risk-free rate of foreign currency rf
        
********************************************************************************

 5. Generalized Black-Scholes formula:
        
    c = S * exp(bT-rT) * N(d1) - X * exp(-rT) * N(d2)
    p = X * exp(-rT) * N(-d2) - S * exp(bT-rT) * N(-d1)
  
    where:
        d1 = (ln(S/X) + (b + vol*vol/2) * T) / (vol * sqrt(T))
        d2 = d1 - vol * sqrt(T)    

    while:
        b: cost of carry rate
    and
        b = r           stock option model
        b = r - q       stock option model with dividend yield q
        b = 0           futures option model
        b = r = 0       margined futures option model
        b = r - rf      currency option model

********************************************************************************

 6. Put-Call Supersymmetry:
        
    p(S, X, T, r, b, vol) == -c(S, X, T, r, b, -vol)

    This simplifies coding. No need to code seperate formulas for put and call.

'''

from math import exp, log, sqrt
#from scipy.stats import norm  # much slower than cdf
from option import Option, OptionType, OptionTypeError, cdf

class BlackScholes(Option):

    def __init__(self, product, spot, strike, rate, expiry, vol, dividend=0, cost_of_carry=None):
        super(BlackScholes, self).__init__(spot, strike, rate, expiry, vol)

        self.dividend = dividend        
        self.cost_of_carry = cost_of_carry # Note: this can override "product"
        self.product_coc_map = {'stock_option': rate, 
                                'stock_option_with_dividend': rate - dividend,
                                'futures_option': 0,
                                'margined_futures_option': 0,
                                'currency_option': rate - dividend,
                               }
        if self.cost_of_carry is None:
            if product is None:
                raise Exception('Both "product" and "cost_of_carry" are None. Cannot decide "cost of carry" rate')
            elif product in self.product_coc_map:
                self.cost_of_carry = self.product_coc_map[product]
            else:
                raise Exception('Unknow product type: "{}". Cannot decide "cost of carry" rate.'.format(product))

    def get_d1_d2(self):
        d1 = (log(self.spot * 1.0 / self.strike) + (self.cost_of_carry + self.vol ** 2 / 2) * self.expiry) / (self.vol * sqrt(self.expiry))
        d2 = d1 - self.vol * sqrt(self.expiry)

        return d1, d2

    def get_option_price(self, otype, round_digit=4):
 
        # This is the generalized Black_Scholes formula
        d1, d2 = self.get_d1_d2()
        
        if otype == OptionType.CALL:
            price = self.spot * exp((self.cost_of_carry - self.rate) * self.expiry) * cdf(d1) - self.strike * exp(- self.rate * self.expiry) * cdf(d2)
            #price = self.spot * exp((self.cost_of_carry - self.rate) * self.expiry) * norm.cdf(d1) - self.strike * exp(- self.rate * self.expiry) * norm.cdf(d2)
        elif otype == OptionType.PUT:
            price = self.strike * exp(- self.rate * self.expiry) * cdf(-d2) - self.spot * exp((self.cost_of_carry - self.rate) * self.expiry) * cdf(-d1)
            #price = self.strike * exp(- self.rate * self.expiry) * norm.cdf(-d2) - self.spot * exp((self.cost_of_carry - self.rate) * self.expiry) * norm.cdf(-d1)
        else:
            raise OptionTypeError
        
        return round(price, round_digit)
