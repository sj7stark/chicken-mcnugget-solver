"""
This file is the entrypoint for a multipage Streamlit app. This app allows users to setup and solve 
a Chicken McNugget Problem. This entrypoint page contains a readme for the app. Other pages will contain
a space for setting up and solving a problem, information regarding the problem, and more.
"""

# import the streamlit package
import streamlit as st

st.set_page_config(
    page_title="Chicken McNugget Problem Solver",
    page_icon="🥔"
)

st.markdown("# Chicken McNugget Problem Solver")

st.markdown(
    """
    This file is the entrypoint for a multipage Streamlit app. This app allows the user to setup and solve 
    a Chicken McNugget Problem. This entrypoint page contains a readme for the app. Other pages will contain
    a space for setting up and solving a problem, information regarding the problem, and more.

    # Introduction

    When you go to McDonald's, you can order their popular Chicken McNuggets in various quantities. 
    In the past, you could purchase McNuggets in packs of 6, 9, and 20. Given that you could only order 
    in these quantities, there are quantities of McNuggets you would not be able to purchase. 
    For instance, you would not be able to order 5 or less McNuggets because 6 was the smallest quantity 
    that you could purchase. For this particular case, it turns out that you can order any quantity of McNuggets
    that is greater than :red[**43**]. We can use the following model to describe our situation:

    $6x + 9y + 20y = N$ 

    where
    * $x$: number of $6$ packs purchased
    * $y$: number of $9$ packs purchased
    * $z$: number of $20$ packs purchased
    * $N$: total number of McNuggets purchased
    
    Notes:
    * $x, y, z, N$ are all nonnegative integers.
    * $x, y, z$ are variables, while $N$ is a given.
    * The above equation will always have a solution if **N is greater than or equal to 44.**
    """
)
