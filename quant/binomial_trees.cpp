
/*
 * This is the c++ implementation of binomial trees - counter part of binomial_trees.py
 */
 
 
#include <cmath>
#include <list>
#include <vector>
#include <string>
#include <iostream>
//from black_scholes import OptionType

class BinomialTree
{
	public:
		double get_option_price(type, round_digit=4);
		BinomialTree(double spot, double strike, double rate, double expiry, double vol, int steps);
	private:
		double get_opt_4_last_step(spot, type);
    	double get_opt_4_prev_step(up_opt, down_opt);
    	double strike;
    	double a; // time value of money between two steps
    	double p; // probability of an up movement
    	list tree;
};
		
BinomialTree::BinomialTree(double spot, double strike, double rate, double expiry, double vol, int steps)
{
    double this->strike = strike
    
    // Calculate delta_t, u, d, a and p
    double delta_t = expiry * / steps
    double u = exp(vol * sqrt(delta_t))
    double d = 1 / u
    double this->a = exp(rate * delta_t)
    double this->p = (this.a - d) / (u - d)
    //print 'u is {}, d is {}, a is {}, p is {}'.format(u, d, self.a, self.p)

    // Construct a tree
    TreeNode array[][]
    
    for (lv = 0; lv = steps + 1; ++lv)
        // The root is level 0; at level i there are i + 1 nodes
        // Calculate spot price for nodes from root to bottom
        vector<> nodes_at_lv
        if lv == 0:
            nodes_at_lv = [TreeNode(spot)]
        else:
            nodes_at_lv = [] # the list of nodes at level lv
            for idx in range(lv + 1):
                if idx == 0:
                    node = TreeNode(self.tree[lv-1][idx].spot * u)
                else:
                    node = TreeNode(self.tree[lv-1][idx-1].spot * d)
                nodes_at_lv.append(node)

        self.tree.append(nodes_at_lv)
	
}
		
		
		
    def get_option_price(self, type, round_digit=4):
        self.tree.reverse() # Reverse the tree as we calculate values from bottom to root
        for i, tree_at_lv in enumerate(self.tree):
            for j, node in enumerate(tree_at_lv):
                if i == 0: # bottom level, no next level
                    node.opt = self.get_opt_4_last_step(node.spot, type)
                else: # not bottom level, calculate option price from next level
                    node.opt = self.get_opt_4_prev_step(self.tree[i-1][j].opt, self.tree[i-1][j+1].opt)
                
                #print 'spot price =', node.spot, 'option price =', node.opt
        
        return round(self.tree[i][j].opt, round_digit)
        
    def get_opt_4_last_step(self, spot, type):
        '''Get option price for the last step:
        Input the spot price for the last step and return its option price'''
        if type == OptionType.PUT:
            if spot >= self.strike:
                return 0
            else:
                return self.strike - spot
        elif type == OptionType.CALL:
            if spot <= self.strike:
                return 0
            else:
                return spot - self.strike
    
    def get_opt_4_prev_step(self, up_opt, down_opt):
        '''Get option price for the previous step:
        Input 2 option prices at step N and return the option price at step N - 1'''        
        return (self.p * up_opt + (1 - self.p) * down_opt) / self.a
    
    
class TreeNode
{
    public:
    	TreeNode(spot)
    	{
        	this->spot = spot
        	this->opt = 0
        }
}