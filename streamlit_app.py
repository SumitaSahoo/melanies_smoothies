# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title( f":cup_with_straw: Cutomize Your Smoothies:cup_with_straw:")
st.write(
  """
    **Add your favourite Fruits to the Smoothies**"""
)

name_on_order=st.text_input('Name on the Smoothies:')
st.write('The name on your Smoothies is:', name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list=st.multiselect('choose upto 5 ingredient:',my_dataframe)

if ingredient_list:
    st.write('you choose:',ingredient_list)
    st.text(ingredient_list)
    ingredient_string=''
    for fruit_chosen in ingredient_list:
        ingredient_string += fruit_chosen + ' '
    st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredient_string + """','""" + name_on_order + """')""" +';'

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit Order')
    

    if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")

import streamlit as st
import requests

url = "https://my.smoothiefroot.com/api/fruit/watermelon"

smoothiefroot_response = requests.get(url)

# ✅ Display properly
if smoothiefroot_response.status_code == 200:
    st.json(smoothiefroot_response.json())
else:
    st.error("API call failed")
