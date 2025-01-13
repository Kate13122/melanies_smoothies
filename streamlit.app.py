## Import python packages
import streamlit as st
cnx = st.connection ("snowflake")
session = cnx.session()
import requests
import pandas as pd


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

#option = st.selectbox(
   # "What is your favourite fruit?",
    #('Banana','Strawberies', 'Peaches'))

name_on_order = st.text_input("Name on Smoothie:")



#st.write('You selected:', option)
from snowflake.snowpark.functions import col

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function

pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredients_list = st.multiselect( 'Choose up to 5 ingredients:', 
                                   my_dataframe
                                  ,max_selections = 5)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        # Correct indentation here
        st.write(f"The search value for {fruit_chosen} is {search_on}.")
        st.subheader(f'{fruit_chosen} Nutrition Information')  # This line is properly indented
        
        # Make the API call for each selected fruit
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        
        if smoothiefroot_response.status_code == 200:
            sf_df = smoothiefroot_response.json()
            st.dataframe(data=sf_df, use_container_width=True)
        else:
            st.write("Error: Nutrition information not found.")



#st.write(my_insert_stmt)
            my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','"""+ name_on_order + """')"""
    #st.write(my_insert_stmt)
    #st.stop()
    
        time_to_insert = st.button('Submit Order')
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered, ' + name_on_order + '!',icon='✅')




   

