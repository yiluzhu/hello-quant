/* 
 * To compile this file, run:
 * c:\apps\Dev-Cpp\bin\g++ monte_carlo.cpp -o monte_carlo.exe
 */


#include <cmath>
#include <iostream>
#include <algorithm>
using namespace std;

double norminv(double p)
{
    static const double a[] =
    {
        -3.969683028665376e+01,
         2.209460984245205e+02,
        -2.759285104469687e+02,
         1.383577518672690e+02,
        -3.066479806614716e+01,
         2.506628277459239e+00
    };

    static const double b[] =
    {
        -5.447609879822406e+01,
         1.615858368580409e+02,
        -1.556989798598866e+02,
         6.680131188771972e+01,
        -1.328068155288572e+01
    };

    static const double c[] =
    {
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e+00,
        -2.549732539343734e+00,
         4.374664141464968e+00,
         2.938163982698783e+00
    };

    static const double d[] =
    {
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e+00,
        3.754408661907416e+00
    };

    double LOW = 0.02425;
    double HIGH = 0.97575;

	double q, r, ret;

    if (p < LOW)
	{
		/* Rational approximation for lower region */
		q = sqrt(-2*log(p));
		ret = (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
			  ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);
	}
	else if (p > HIGH)
	{
		/* Rational approximation for upper region */
		q  = sqrt(-2*log(1-p));
		ret = -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
			  ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);
	}
	else
	{
		/* Rational approximation for central region */
    	q = p - 0.5;
    	r = q*q;
		ret = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q /
			  (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1);
	}

    return ret;
}

enum opt_type {CALL, PUT};

double run_monte_carlo(long simu_num, opt_type type,
                       double spot, double strike, double rate,
                       double expiry, double vol, double dividend=0)
{
    double cost_of_carry = rate - dividend;
    int z;
    if (type == CALL)
        z = 1;
    else
        z = -1;

    double sum = 0;
    double st;
    for (int i = 0; i < simu_num; ++i)
    {
        st = spot * exp((cost_of_carry - vol*vol / 2) * expiry + 
                        vol * norminv(rand()/(RAND_MAX + 1.0)) * sqrt(expiry));
        sum += max(z * (st - strike), 0.0);
    }

    double price = exp(- rate * expiry) * sum / simu_num;
    return price;
}
/*
int main()
{
    cout << run_monte_carlo(10000, PUT, 50, 52, 0.05, 2, 0.3) << endl; // 6.67114
   
}
*/
