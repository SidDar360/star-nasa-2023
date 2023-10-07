import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import numpy as np
from lang_utils import ask_to_all_pdfs_sources, create_qa_retrievals, get_text_splitter
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

# SETUP ------------------------------------------------------------------------
#favicon = Image.open("/home/obiraj77/star/favicon.ico")
st.set_page_config(
    page_title="STAR: Revolutionizing Technical Standards with AI Using Llama 2 ",
    #page_icon=favicon,
    layout="wide",
    initial_sidebar_state="auto",
)


# Sidebar contents ------------------------------------------------------------------------
with st.sidebar:
    st.title("STAR - Revolutionizing Technical Standards with AI Using Llama 2")
    st.markdown(
        """
    ## About
    This app is to Revolutionize Techincal Standards with AI (Llama 2 -powered), built using:
    - [Streamlit](https://streamlit.io/)
    - [Meta Llama 2 model](https://ai.meta.com/llama/) 
    """
    )
    st.write(
        "Developed  by [Sid D](https://www.linkedin.com/in/sid-darapuram-259778275/) and [Karthik D]"
    )


# ROW 1 ------------------------------------------------------------------------

Title_html = """
    <style>
        .title h1{
          user-select: none;
          font-size: 43px;
          color: white;
          background: repeating-linear-gradient(-45deg, red 0%, yellow 7.14%, rgb(0,255,0) 14.28%, rgb(0,255,255) 21.4%, cyan 28.56%, blue 35.7%, magenta 42.84%, red 50%);
          background-size: 300vw 300vw;
          -webkit-text-fill-color: transparent;
          -webkit-background-clip: text;
          animation: slide 10s linear infinite forwards;
        }
        .title h2{
          user-select: none;
          font-size: 30px;
          color: white;
          background: repeating-linear-gradient(-45deg, red 0%, yellow 7.14%, rgb(0,255,0) 14.28%, rgb(0,255,255) 21.4%, cyan 28.56%, blue 35.7%, magenta 42.84%, red 50%);
          background-size: 300vw 300vw;
          -webkit-text-fill-color: transparent;
          -webkit-background-clip: text;
          animation: slide 10s linear infinite forwards;
        }
        @keyframes slide {
          0%{
            background-position-x: 0%;
          }
          100%{
            background-position-x: 600vw;
          }
        }
    </style> 
    
    <div class="title">
        <h1>Revolutionizing Technical Standards</h1>
        <h2>Add more details here.........</h2
    </div>
    """
components.html(Title_html)

uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf"],
    key="file_upload_widget",
    accept_multiple_files=True,
)

if uploaded_files is not None and len(uploaded_files) > 0:
    st.session_state.processing_button_clicked = False

    if True: #st.button("Start Processing") or st.session_state.processing_button_clicked == True:
        st.session_state.file_name = uploaded_files[0]
        st.session_state.processing_button_clicked = True

        if uploaded_files is None or len(uploaded_files) != 1:
            st.warning("Upload exactly 1 PDf files")
            st.stop()

        srcText = get_text_splitter(uploaded_files[0])

        try:
            st.write(
                    "LIST OF SUGGESTIONS. PLEASE SELECT AND ACCEPT"
                )

            # Cache the dataframe so it's only loaded once
            # @st.cache_data
            def load_data():
                return pd.DataFrame(
                    [
                        {"beforText":"VASUKI DIVYA PONDURI", "afterText": "Sid Darapuram", "apply_Selection": True},
                        { "beforText":"vasukidivya006@gmail.com", "afterText": "smartsid2007@gmail.com", "apply_Selection": False},
                        { "beforText":"Sample original text", "afterText": "Revised New Text", "apply_Selection": True},
                    ]
                )

            df = load_data()
            edited_df = st.data_editor(df) # 👈 An editable dataframe

        except Exception as e:

            st.error("Something went grong...")
            st.exception(e)
            st.stop()


        #st.snow()
        edited_df = edited_df[edited_df["apply_Selection"] ==True]

        st.table(edited_df)



########################### END OF CODE ################################

        # for i in range(len(edited_df)):
        #     #if(edited_df.loc[i, "apply_Selection"] == True):
        #     print(edited_df.loc[i, "beforText"], edited_df.loc[i, "afterText"], edited_df.loc[i, "apply_Selection"])
        # row0_toggle = edited_df.loc[0, "apply_Selection"]
        # st.markdown(f"Row 0 is  **{row0_toggle}** 🎈")
        # row1_toggle = edited_df.loc[1, "apply_Selection"]
        # st.markdown(f"Row 1 is  **{row1_toggle}** 🎈")
    # st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
        # st.markdown(f"Your favorite command is **{favorite_command}** 🎈")


        # df2 = pd.DataFrame(
        #     [
        #         {"command": "st.selectbox", "rating": 4, "is_widget": True},
        #         {"command": "st.balloons", "rating": 5, "is_widget": False},
        #         {"command": "st.time_input", "rating": 3, "is_widget": True},
        #     ]
        # )
        # edited_df2 = st.data_editor(df2)

        # favorite_command = edited_df2.loc[edited_df2["rating"].idxmax()]["command"]
        # st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

        # confirm_changes_btn = st.form_submit_button("Confirm Changes")
        # if confirm_changes_btn:
        #     for i in range(len(edited_df)):
        #         if(edited_df.loc[i, "apply_Selection"] == True):
        #             print(edited_df.loc[i, "beforText"], edited_df.loc[i, "afterText"], edited_df.loc[i, "apply_Selection"])
        #         # else:
        #         #     edited_df = data.drop(0)
        #     edited_df = edited_df.loc[edited_df["apply_Selection"] ==True]
        #     st.table(edited_df)

   




