# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
import requests
cnx = st.connection("snowflake")





# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

#option = st.selectbox(
   # "What is your favourite fruit?",
    #('Banana','Strawberies', 'Peaches'))

name_on_order = st.text_input("Name on Smoothie:")



#st.write('You selected:', option)
from snowflake.snowpark.functions import col

#session = get_active_session()
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect( 'Choose up to 5 ingredients:', 
                                   my_dataframe
                                  ,max_selections = 5)

if ingredients_list:
    #st.write(ingredients_list)
    st.text(ingredients_list)
    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
        st_df =st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)



#st.write(my_insert_stmt)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order + """')"""
    #st.write(my_insert_stmt)
    #st.stop()

    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!',icon='✅')
    



