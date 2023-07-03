"""
This file is for creating a page describing the heuristic I developed using Integer Linear Programming (ILP).
"""

import streamlit as st

# adjust the appearance of the tab in the web browser 
st.set_page_config(
    page_title="ILP Heuristic",
    page_icon="💻"
)

st.markdown(
    """
    # Integer Linear Programming (ILP) Heuristic

    Below is a heuristic I developed that uses ILP to find a solution to the Chicken McNugget Problem when
    dealing with 3 nonzero pack sizes.

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

    $s.t.$ 
    $6x + 9y + 20z = N$  
    $x, y, z$ are integers $>=0$ 

    with a low value for $N$ (that you know is NOT the final answer, like 1), incrementing N by 1, and resolving the MILP. You will get to a point in which you solve a problem, see that there is no solution, and then every new solve after that results in a solution being found. The last $N$ that results in a no solution is your answer.

   """
)