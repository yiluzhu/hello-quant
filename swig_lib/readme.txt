build a python module:

1. generate wrapper cpp
d:\apps\swigwin-2.0.5\swig.exe -python monte_carlo.i

2. compile cpp
c:\apps\Dev-Cpp\bin\g++ -c monte_carlo.cpp monte_carlo_wrap.c -Id:\apps\python27\include

c:\apps\Dev-Cpp\bin\g++ -shared monte_carlo.o monte_carlo_wrap.o -o _swig_monte_carlo.lib