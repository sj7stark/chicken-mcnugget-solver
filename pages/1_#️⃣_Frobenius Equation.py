"""
This file is for creating a page describing the Frobenius Equation. The Frobenius Equation is related to the
Chicken McNugget Problem.
"""


import streamlit as st

st.markdown(
    """
   ## Frobenius Equation
   The **Frobenius equation** is
   $a_{1}x_{1} + a_{2}x_{2}+...+a_{n}x_{n}=b$
   where $a_{i}$ are positive integers and $b$ and $x_{i}$ are nonnegative integers.
   The **Frobenius number** is the largest such value for $b$, given values for $a_{i}$, 
   no solution exists. In the example given in the Intro, :red[**$43$**] is the Frobenius number.
   ## Closed Form Solution
   If there are only two $a_{i}$ values, then the Frobenius number $g(a_{1},a_{2})$ is given by
   $g(a_{1},a_{2}) = a_{1}a_{2} - (a_{1}+a_{2})$
   where:
   * $0 < a_{1} < a_{2}$  
   * $a_{1}$ and $a_{2}$ are both integers  
   ## Other Problems
   For problems in which we have three or more $a_{i}$, including the Chicken McNugget Problem,
               no-closed form solution exists. This problem is NP-hard for the general case.
               
   ## No Solution
   Depending on the $a_{i}$ values, it's possible to have no solution. For instance, suppose we
   could purchase McNuggets in packs of $2,4,$ and $6$. This would mean that we would only be able to purchase
   McNuggets in even quanities. Thus, there is no Frobenius number, because we could just keep on finding
   a larger odd number. There are other cases that result in no solution as well. Having to buy in packs of
   $5, 10,$ and $20$ would also result in there being no Frobenius number. In order for there to be a Frobenius
   number, we need the **Greatest Common Divisor** among the pack sizes ($a_{i}$) to be $1$. 
   """
)