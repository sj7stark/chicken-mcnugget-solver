# imports
import streamlit as st
from mcnugget_solver import nugget_solve

# header
st.markdown('<font size="7">**# McNugget Problem Solver**')

# Separate into tabs
readme_tab, solve_tab = st.tabs(["ReadMe", "Solve"])

with readme_tab:
   st.header("ReadMe")
   st.markdown("# Introduction")
   st.markdown("When you go to McDonald's, you can order their popular Chicken McNuggets in various quantities. In the past, these quantities were ")


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
    st.write(f"Solution: {mcnuggets_sol} McNuggets")

