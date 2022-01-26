import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from app_functions import *

image = Image.open('images/cryptopunks-image.jpg')

with st.sidebar: 
    st.sidebar.image(image)
    st.sidebar.header('What do you want?')

    menu = st.sidebar.selectbox(
        "Select one below.",
        ("Search by Punk ID", "Highest Estimated Value Punks", "Highest Rarity Scores", "Averages of Types & Accessories", "Project Terms & Info")
    )

    st.sidebar.markdown('---')
    st.sidebar.write('Website Last Updated: Jan. 25, 2022')
    st.sidebar.write('Transaction Data Last Updated: Nov. 25, 2021')

if menu == 'Search by Punk ID':
    set_home()
elif menu == 'Highest Estimated Value Punks':
    set_value()
elif menu == 'Highest Rarity Scores':
    set_rarity()
elif menu == 'Averages of Types & Accessories':
    set_averages()
elif menu == 'Project Terms & Info':
    set_about()
