# imports
import streamlit as st
from mcnugget_solver import nugget_solve

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


