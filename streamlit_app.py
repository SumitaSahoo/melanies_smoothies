# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

# UI
st.title(":cup_with_straw: Customize Your Smoothies :cup_with_straw:")
st.write("**Add your favourite Fruits to the Smoothies**")

name_on_order = st.text_input('Name on the Smoothies:')
st.write('The name on your Smoothies is:', name_on_order)

# ✅ ONLY this session
session = get_active_session()

# Load data
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Convert to list (IMPORTANT FIX)
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Multiselect
ingredient_list = st.multiselect('Choose up to 5 ingredients:', fruit_list)

if ingredient_list:
    st.write('You chose:', ingredient_list)

    ingredient_string = ' '.join(ingredient_list)

    # ✅ Safe insert (better approach)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredient_string}', '{name_on_order}')
        """).collect()

        st.success('Your Smoothie is ordered!', icon="✅")
``
