# imports
import streamlit as st
import math
from mcnugget_solver import nugget_solve

# adjust the appearance of the tab in the web browser 
st.set_page_config(
    page_title="Solver",
    page_icon="🔍"
)

# solver page description

st.markdown(
    """
    # Solver

    This page allows you to set up and solve your very own Chickent McNugget Problem. First, set 
    the pack sizes using the sliders on the left side of the page. Once you have set your pack sizes,
    simply click the **Solve** button.

    """
)


# Chicken McNugget Solver

# side bar for pack size
with st.sidebar:
    st.header('Pack Sizes')

    # sliders to set the values
    pack_size_1 = st.slider('Pack Size 1',min_value=0,max_value=20,value=6,step=1)
    pack_size_2 = st.slider('Pack Size 2',min_value=1,max_value=20,value=9,step=1)
    pack_size_3 = st.slider('Pack Size 3',min_value=1,max_value=20,value=20,step=1)

    # button to initiate solve
    solve_btn = st.button('Solve')

if solve_btn:

    # for the two pack size case:
    if (pack_size_1 == 0) and (pack_size_2 != pack_size_3):
        mcnuggets_sol = pack_size_2 * pack_size_3 - (pack_size_2 + pack_size_3)
        st.markdown(f" ## Solution: {mcnuggets_sol} McNuggets")

    # for the three pack size case
    elif math.gcd(math.gcd(pack_size_1,pack_size_2),pack_size_3) == 1:
        mcnuggets_sol = nugget_solve(pack_size_1, pack_size_2, pack_size_3, threshold_solve=100)
        st.markdown(f" ## Solution: {mcnuggets_sol} McNuggets")
    
    # when there is no solution
    else:
        st.markdown(f" ## There is no solution")

