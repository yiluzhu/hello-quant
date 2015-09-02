
from unittest import TestCase, main
from black_scholes import BlackScholes
from option import OptionType
from black_scholes_greeks import BlackScholesGreeks

class BlackScholesModelTestCase(TestCase):

    def test_vanilla_call_option(self):
        '''
        Q:  (Vanilla option)
            A European call option, 3 month to expiry, stock price is 60, the strike
            price is 65, risk free interest rate is 8% per year, volatility is 30% per year
        A:
            2.1334
        '''
        bsm = BlackScholes('stock_option', 60, 65, 0.08, 0.25, 0.3)
        self.assertEqual(2.1334,
                         bsm.get_option_price(OptionType.CALL))
        
        #bsm.get_option_price(BlackScholes::put, BlackScholes::stock_option, 60, 65, 0.08, 0.25, -0.3)
        #pp + 60 - 65*exp(- 0.08 * 0.25) 

    
    def test_vanilla_option_with_dividend(self):
        '''
        Q:  (Vanilla option with yield)
            A European put option, 6 month to expiry, stock price is 100, the strike
            price is 95, risk free interest rate is 10% per year, 
            the dividend is 5% per year, volatility is 20% per year
        A:
            2.4648
        '''
        bsm = BlackScholes('stock_option_with_dividend', 100, 95, 0.1, 0.5, 0.2, 0.05)
        self.assertEqual(2.4648,
                         bsm.get_option_price(OptionType.PUT))
 
    def test_options_on_futures(self):
        ''' 
        Q:  (Options on Futures)
            A European option on futures, 9 month to expiry, future price is 19, the strike
            price is 19, risk free interest rate is 10% per year, volatility is 28% per year
        A:
            c = p = 1.7011
        '''
        bsm = BlackScholes('futures_option', 19, 19, 0.1, 0.75, 0.28, 0.1)
        self.assertEqual(1.7011,
                         bsm.get_option_price(OptionType.CALL))
        self.assertEqual(1.7011,
                         bsm.get_option_price(OptionType.PUT))
    
    def test_options_on_FX(self):
        ''' 
        Q:  (Options on FX)
            A European USD-call/EUR-put option, 6 month to expiry, USD/EUR exchange rate is 1.56, 
            the strike strike rate is 1.6, the domestic risk free interest rate in EUR is 8% per year, 
            the foreign risk-free interest rate in USD is 6%, volatility is 12% per year
        A:
            c = 0.0291
        '''
        bsm1 = BlackScholes('currency_option', 1.56, 1.6, 0.06, 0.5, 0.12, 0.08)
        self.assertEqual(0.0291,
                         bsm1.get_option_price(OptionType.CALL))
        bsm2 = BlackScholes('currency_option', 1/1.56, 1/1.6, 0.08, 0.5, 0.12, 0.06)
        self.assertEqual(0.0117,
                         bsm2.get_option_price(OptionType.PUT))
        #self.assertEqual(0.0291 / 1.56, # Percentage of EUR
        #                 0.0117 * 1.6)  # Percentage of USD

    def test_compare_binomial_tree(self):
        '''
        European put option, 2 years to expiry, spot price 50, strike price 52, risk free rate 5%,
        volatility 30%
        
        The result from binomial trees with steps == 10 : 6.747
                                                     100: 6.7781
                                                     500: 6.7569
        '''
        bsm = BlackScholes('stock_option', 50, 52, 0.05, 2, 0.3)
        self.assertEqual(6.7601,
                         bsm.get_option_price(OptionType.PUT))


class BlackScholesGreeksTestCase(TestCase):
    def test_delta_greeks(self):
        ''' 
        Q:  (Delta Greeks)
            A future option, 6 month to expiry, the futures price is 105, 
            the strike strike price is 100, risk free interest rate is 10% per year, 
            volatility is 36% per year
        A:
            delta_call = 0.5946
            delta_put = -0.3566
        '''
        bsg = BlackScholesGreeks('futures_option', 105, 100, 0.1, 0.5, 0.36)
        self.assertEqual(0.5946,
                         bsg.get_delta_greeks(OptionType.CALL))
        self.assertEqual(-0.3566,
                         bsg.get_delta_greeks(OptionType.PUT))

    def test_delta_greeks2(self):
        '''
        Q:
            A commodity option with two years to expiration. The commodity price
            is 90, the strike price is 40, the risk-free interest rate is 3% per year,
            the cost-of-carry is 9% per year, and the volatility is 20%. 
            What's the delta of a call option?
        A:
            delta_call = 1.1273
            This implies that the call option price will increase/decrease 1.1273 USD
            if the spot price increase/decrease by 1 USD
            
        '''
        bsg = BlackScholesGreeks(None, 90, 40, 0.03, 2, 0.2, cost_of_carry=0.09)
        self.assertEqual(1.1273,
                         bsg.get_delta_greeks(OptionType.CALL))

        # For every 1 dollar increase/decrease of the spot price, the option price increase/decrease 1.1273
        opt_price = BlackScholes(None, 90, 40, 0.03, 2, 0.2, cost_of_carry=0.09).get_option_price(OptionType.CALL)
        self.assertAlmostEqual(opt_price + 1.1273,
                               BlackScholes(None, 91, 40, 0.03, 2, 0.2, cost_of_carry=0.09).get_option_price(OptionType.CALL),
                               3)
        self.assertEqual(round(opt_price - 1.1273, 4),
                         BlackScholes(None, 89, 40, 0.03, 2, 0.2, cost_of_carry=0.09).get_option_price(OptionType.CALL))
        


if __name__ == '__main__':
    main()
