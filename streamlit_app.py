# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

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

my_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
pd_df = my_df.to_pandas()


MAX_INGREDIENTS: int = 6
ingredients_list = st.multiselect(
    label=f"Choose up to {MAX_INGREDIENTS} ingredients:",
    options=my_df,
    max_selections=MAX_INGREDIENTS,
)

if ingredients_list:
    ingredients_string = ""

    for chosen_fruit in ingredients_list:
        ingredients_string += chosen_fruit + " "

        search_on = pd_df.loc[pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"].iloc[0]
        # st.write("The search value for ", fruit_chosen, " is ", search_on, ".")

        st.subheader(f"{chosen_fruit} Nutrition Information")
        smoothiesfroot_response = requests.get(
            f"https://fruityvice.com/api/fruit/{search_on.lower()}"
        )
        sf_df = st.dataframe(
            data=smoothiesfroot_response.json(), use_container_width=True
        )

    # st.write(ingredients_string)

    my_insert_stmt = (
        """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('"""
        + ingredients_string
        + """','"""
        + name_on_order
        + """')
    """
    )

    # st.write(my_insert_stmt)

    submitted = st.button("Submit Order")

    if submitted:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
