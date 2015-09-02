import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from black_scholes_greeks import BlackScholesGreeks
from option import OptionType



if __name__ == '__main__':
    '''
    # Tutorial
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,
                           linewidth=0, antialiased=False)
    #ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
    
    ax.set_zlim(-1.01, 1.01)
    
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    
    #fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()
    '''
    fig = plt.figure(figsize=plt.figaspect(0.5))
    
    ##### 1st subplot #####
    X = np.arange(1, 180, 5) # days to maturity
    lenX = len(X)
    Y = np.arange(50, 150, 2) # spot price
    lenY = len(Y)
    X, Y = np.meshgrid(X, Y)
    # Spot delta call: X = 100, r = 7%, b = 4%, vol= 30%
    Z = [[BlackScholesGreeks(None, Y[i][j], 100, 0.07, X[i][j]/365.0, 0.3, 
                             cost_of_carry=0.04).get_delta_greeks(OptionType.CALL) 
                                    for j in range(lenX)] 
                                        for i in range(lenY)]
    
    ax = fig.add_subplot(121, projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=0)#, antialiased=False)
    #ax.plot_wireframe(X, Y, Z) # Draw a wireframe diagram without color
    ax.set_zlim(0, 1)
    ax.set_xlabel('Days to maturity')
    ax.set_ylabel('Asset spot price')
    ax.set_zlabel('Delta')
   
    ##### 2nd subplot ######
    
    X = np.arange(1, 550, 10) # days to maturity
    lenX = len(X)
    Y = np.arange(1, 200, 5) # spot price
    lenY = len(Y)
    X, Y = np.meshgrid(X, Y)
    # Spot delta call: X = 100, r = 5%, b = 30%, vol= 25%
    Z = [[BlackScholesGreeks(None, Y[i][j], 100, 0.05, X[i][j]/365.0, 0.25, 
                             cost_of_carry=0.3).get_delta_greeks(OptionType.CALL) 
                                    for j in range(lenX)] 
                                        for i in range(lenY)]
    
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=0)
    ax2.set_zlim(0, 1.6)
    ax2.set_xlabel('Days to maturity')
    ax2.set_ylabel('Asset spot price')
    ax2.set_zlabel('Delta')
    
    plt.show()
