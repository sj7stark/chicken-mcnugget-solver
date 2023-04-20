# imports
import streamlit as st
from mcnugget_solver import nugget_solve

# header
st.header('McNugget Problem Solver')

# side bar for pack size
with st.sidebar:
    st.header('Pack Sizes')

    # sliders to set the values
    pack_size_1 = st.slider('Pack Size 1',min_value=3,max_value=9,value=3,step=6)
    pack_size_2 = st.slider('Pack Size 2',min_value=2,max_value=8,value=4,step=2)
    pack_size_3 = st.slider('Pack Size 3',min_value=1,max_value=20,value=10,step=1)

    # button to initiate solve
    solve_btn = st.button('Solve')

if solve_btn:
    mcnuggets_sol = nugget_solve(pack_size_1, pack_size_2, pack_size_3, threshold_solve=100)
    st.write(f"Solution: {mcnuggets_sol} McNuggets")

