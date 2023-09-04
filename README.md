# chicken-mcnugget-solver

This repository contains a Jupyter Notebook that solves a Chicken McNugget Problem using Mixed Integer Linear Programming (MILP). It also contains a Streamlit web app. You can test out the web app here: https://chicken-mcnugget-solver.streamlit.app/.

# Introduction

McDonald's, a popular fast food restaurant, sells a food product called Chicken McNuggets. You can buy Chicken McNuggets in packs of various sizes. Suppose you can buy McNuggets in packs of 6, 9, 20.

The Chicken McNugget Problem consists of finding the largest number of Chicken McNuggets you would NOT be able to buy given the previously mentioned pack sizes. You can't buy exactly 7, 8, or 11 McNuggests. You can buy exactly 21 McNuggets though.

If you would like more information, please look take a look at this page from [Art of Problem Solving](https://artofproblemsolving.com/wiki/index.php/Chicken_McNugget_Theorem#Origins).

# Challenge

There is a closed form solution for the Chicken McNugget Problem when there are only 2 pack sizes. Please see the Art of Problem Solving link from above for more information. For 3 or more different pack sizes, however, there is no closed form solution.

# ILP Method

Consider the following equation:

$6x + 9y + 20z = N$

where: 
* $x$ is the number of size 6 packs purchased 
* $y$ is the number of size 9 packs purchased
* $z$ is the number of size 20 packs purchased
* $N$ is the total number of McNuggets purchased

We need to find the largest N such that no combination x, y, and z can satisfy the above equation. x, y, z, and N are restricted to nonnegative integer values.

For every number greater than this largest N, there exists some combination of x, y, z that satisfies the above equation.

The method consists of Solving the MILP Model Below,

$max \space 0$

$s.t.$ <br />
$6x + 9y + 20z = N$  <br />
$x, y, z$ are integers $>=0$ <br />

with a low value for $N$ (that you know is NOT the final answer, like 1), incrementing N by 1, and resolving the MILP. You will get to a point in which you solve a problem, see that there is no solution, and then every new solve after that results in a solution being found. The last $N$ that results in a no solution is your answer.

# Python Packages

The only Python package you need to run the notebook contained in this repo is `docplex`. `docplex` comes with CPLEX, a state-of-the-art mathematical programming solver from IBM. You can download a free trial of CPLEX [here](https://www.ibm.com/account/reg/us-en/signup?formid=urx-20028).

The streamlit app was made using `streamlit` and `gurobipy` packages.
