# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col

import streamlit as st

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!")
st.write(
  """
  Choose fruits you want in your custom smoothie!
  """
)

cnx = st.connection("snowflake")
session = cnx.session()

# customer inserts their name here...
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

my_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_df, use_container_width=True)

MAX_INGREDIENTS: int = 6
ingredients_list = st.multiselect(
    label=f"Choose up to {MAX_INGREDIENTS} ingredients:",
    options=my_df,
    max_selections=MAX_INGREDIENTS
)

if ingredients_list:
    ingredients_string = ''

    for chosen_fruit in ingredients_list:
        ingredients_string += chosen_fruit + ' '

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order +"""')
    """

    # st.write(my_insert_stmt)

    submitted = st.button("Submit Order")

    if submitted:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon='✅')
