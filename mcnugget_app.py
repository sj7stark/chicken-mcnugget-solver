# imports
import streamlit as st
from mcnugget_solver import nugget_solve

# header
st.markdown("# McNugget Problem Solver")

# Separate into tabs
readme_tab, frobenius_num_tab, solve_tab = st.tabs(["Intro", "Frobenius Number","Solve"])

with readme_tab:
   st.markdown("## Introduction")
   st.markdown("""When you go to McDonald's, you can order their popular Chicken McNuggets in various quantities. 
   In the past, you could purchase McNuggets in packs of 6, 9, and 20 [1]. Given that you could only order 
   in these quantities, there are quantities of McNuggets you would not be able to purchase. 
   For instance, you would not be able to order 5 or less McNuggets because 6 was the smallest quantity 
   that you could purchase. For this particular case, it turns out that you can order any quantity of McNuggets
   that is greater than :red[**43**]. In other words,""")
   st.markdown("$6x + 9y + 20y = N$")
   st.markdown("where")
   st.markdown("* $x$: number of $6$ packs purchased")
   st.markdown("* $y$: number of $9$ packs purchased")
   st.markdown("* $z$: number of $20$ packs purchased")
   st.markdown("* $N$: total number of McNuggets purchased")
   st.markdown("always has a solution if **N is greater than or equal to 44.**")
   st.markdown("Notes:")
   st.markdown("* $x, y, z$ are varaibles, while $N$ is a given.")
   st.markdown("* $x, y, z, N$ are all nonnegative integers.")
   
with frobenius_num_tab:
   st.markdown("## Frobenius Equation")
   st.markdown("The **Frobenius equation** is")
   st.markdown("$a_{1}x_{1} + a_{2}x_{2}+...+a_{n}x_{n}=b$")
   st.markdown("where $a_{i}$ are positive integers and $b$ and $x_{i}$ are nonnegative integers.")
   st.markdown("""The **Frobenius number** is the largest such value for $b$, given values for $a_{i}$, 
   no solution exists. In the example given in the Intro, :red[**$43$**] is the Frobenius number.""")
   st.markdown("## Closed Form Solution")
   st.markdown("If there are only two $a_{i}$ values, then the Frobenius number $g(a_{1},a_{2})$ is given by")
   st.markdown("$g(a_{1},a_{2}) = a_{1}a_{2} - (a_{1}+a_{2})$")
   st.markdown("where:")
   st.markdown("* $0 < a_{1} < a_{2}$ ") 
   st.markdown("* $a_{1}$ and $a_{2}$ are both integers ") 
   st.markdown("## Other Problems")
   st.markdown("""For problems in which we have three or more $a_{i}$, including the Chicken McNugget Problem,
               no-closed form solution exists. This problem is NP-hard for the general case.
               """)
   st.markdown("## No Solution")
   st.markdown("""Depending on the $a_{i}$ values, it's possible to have no solution. For instance, suppose we
   could purchase McNuggets in packs of $2,4,$ and $6$. This would mean that we would only be able to purchase
   McNuggets in even quanities. Thus, there is no Frobenius number, because we could just keep on finding
   a larger odd number. There are other cases that result in no solution as well. Having to buy in packs of
   $5, 10,$ and $20$ would also result in there being no Frobenius number. In order for there to be a Frobenius
   number, we need the **Greatest Common Divisor** among the pack sizes ($a_{i}$) to be $1$. 
   
   
   """)

with solve_tab:

    # side bar for pack size
    with st.sidebar:
        st.header('Pack Sizes')

        # sliders to set the values
        pack_size_1 = st.slider('Pack Size 1',min_value=1,max_value=20,value=6,step=1)
        pack_size_2 = st.slider('Pack Size 2',min_value=1,max_value=20,value=9,step=1)
        pack_size_3 = st.slider('Pack Size 3',min_value=1,max_value=20,value=20,step=1)

        # button to initiate solve
        solve_btn = st.button('Solve')

    if solve_btn:
        mcnuggets_sol = nugget_solve(pack_size_1, pack_size_2, pack_size_3, threshold_solve=100)
        if type(mcnuggets_sol) != str:
            st.markdown(f" ## Solution: {mcnuggets_sol} McNuggets")
        else: 
            st.markdown(f" ## There is no solution")

