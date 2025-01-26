# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched
from snowflake.snowpark.context import get_active_session



# Write directly to the app
st.title(":cup_with_straw: Pending Smoothies Order:cup_with_straw: ")
st.write("""Orders that need to be filled are 
    """
)


#name_on_order = st.text_input("Name on Smoothie: ")
#st.write("The name of your smootie will be", name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted :
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(edited_datase
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.success('Order Updated.', icon='👍')
        except:
            st.write('Something went wrong.' ) 
else:
    st.success('There are no pending orders write now', icon='👍' )
   
