import streamlit as st
import eda
import inference

st.set_page_config(
    page_title='Video Game Critic Score',
    layout='wide',
    initial_sidebar_state='expanded'
)

page = st.sidebar.selectbox('Pilih Page', ('EDA','Prediction'))
if page == 'EDA':
    eda.run()
else:
    inference.run()