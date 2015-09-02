'''Yilu's Quant World'''

import os
import time

import webapp2
from google.appengine.ext.webapp import template

from quant.black_scholes import BlackScholes
from quant.binomial_trees import BinomialTree
from quant.monte_carlo import MonteCarlo
from quant.option import OptionType


class MainPage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))
        

class Pricing(webapp2.RequestHandler):
    def post(self):
        otype_map = {'call': OptionType.CALL, 'put': OptionType.PUT}
        otype = otype_map[self.request.get('option_type')]
        method = self.request.get('pricing_method')
        
        spot = float(self.request.get('spot'))
        strike = float(self.request.get('strike'))
        rate = float(self.request.get('rate'))
        expiry = float(self.request.get('expiry'))
        vol = float(self.request.get('vol'))
        coc = self.request.get('coc')
        coc = float(coc) if coc else rate
        
        price, time_ = self.get_price(otype, method, spot, strike, rate, expiry, vol, coc)
        self.show_price(price, time_)
        
    def get_price(self, otype, method, spot, strike, rate, expiry, vol, coc):
        t0 = time.time()
        if method == 'formula':
            bs = BlackScholes('', spot, strike, rate, expiry, vol, cost_of_carry=coc)
            price = bs.get_option_price(otype)
        elif method == 'bitree':
            num = int(self.request.get('bt_step_num'))
            bt = BinomialTree(spot, strike, rate, expiry, vol, steps=num)
            price = bt.get_option_price(otype)
        else: # simulation
            num = int(self.request.get('mc_simu_num'))
            mc = MonteCarlo(spot, strike, rate, expiry, vol, coc)
            price = mc.run(otype, num, 0) # 0 for single process at GAE doesn't support multiprocess

        t = time.time() - t0

        return price, t
        
    def show_price(self, price, time_):
        template_values = {
                            'price': price,
                            'time': round(time_, 3),
                          }
        
        path = os.path.join(os.path.dirname(__file__), 'result.html')        
        self.response.out.write(template.render(path, template_values))


class DisplayPlot(webapp2.RequestHandler):
    def post(self):
        sel = self.request.get('view_plot')
        
        diagram_dict = {'formula': [('black_scholes_plot.png',), 
                                    'These diagrams shows how option prices are changed with expiration, strike price, spot price and volatility'], 
                        'greek':   [('black_scholes_greeks_plot_1.png', 'black_scholes_greeks_plot_2.png'), 
                                    'These are two screen shot of a 3D diagram about delta greeks. The original diagram can rotate 360 degree.'],
                        'bitree':  [('binomial_trees_plot.png',), 
                                    '''The diagram shows how option prices calculated by Binomial Tree change with the number of steps that Binomial Tree uses.
                                    As we know the accuracy of Binomial Tree is increased when the steps increase
                                     - the diagram proves it but also shows very interesting trend.'''],
                       }
        
        template_values = {
                            'paths': diagram_dict[sel][0],
                            'note': diagram_dict[sel][1],
                          }
        
        path = os.path.join(os.path.dirname(__file__), 'plot.html')        
        self.response.out.write(template.render(path, template_values))



# __main__
app = webapp2.WSGIApplication([('/', MainPage), 
                              ('/pricing', Pricing),
                              ('/display_plot', DisplayPlot)],
                              debug=True)
