import config
from ai import AI
from luna import Luna
from vectordb import vectorDB
from pathlib import Path
import uuid
ai = AI()
luna = Luna()
db = vectorDB()

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
from PyPDF2 import PdfReader
from tempfile import NamedTemporaryFile
import pathlib
import os
from asposeCloud import updatePdf
from asposeWords import updatePdfLocally

def extractLinesFromPdf(pdfFilePath):
    lineArr = []
    with open(pdfFilePath, 'rb') as file:
        pdfReader = PdfReader(file)
        numPages = len(pdfReader.pages)

        for pageNum in range(numPages):
            page = pdfReader.pages[pageNum]
            pageText = page.extract_text()
            lines = pageText.split('\n\n')
            for line in lines:
                if line != "":
                    lineArr.append(line)
    return lineArr

# SETUP ------------------------------------------------------------------------
#favicon = Image.open("/home/obiraj77/star/favicon.ico")
st.set_page_config(
    page_title="Lunaris: NASA Standards Copilot",
    #page_icon=favicon,
    layout="wide",
    initial_sidebar_state="auto",
)


# Sidebar contents ------------------------------------------------------------------------
with st.sidebar:
    st.title("Lunaris: NASA Standards Copilot")
    st.markdown(
        """
    ## About
    This app is designed by couple of high schoolers to assist in reviewing NASA Technical Standards for clarity, consistency, identifying and rectifying any ambiguities.
    """
    )
    st.write(
        "Developed  by [Sid D](https://www.linkedin.com/in/sid-darapuram-259778275/) and [Karthik D](https://www.linkedin.com/in/karthik-darisi-68a896294/)"
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
        <h1>Lunaris: NASA Standards Copilot</h1>
        <h2>Upload your standards file and get AI generated suggestions</h2>
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
    # with NamedTemporaryFile(dir='.', suffix='.csv') as f:
    #     f.write(uploaded_files.getbuffer())
    # Define a temporary directory
    temp_dir = "host-star"

    # Create the temporary directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)

    # Check if a file was uploaded
    if uploaded_files is not None:
        # Save the uploaded file to the temporary directory
        file_path = os.path.join(temp_dir, uploaded_files[0].name) 
        file_path.replace("'", "")
        with open(file_path, "wb") as f:
            f.write(uploaded_files[0].read())
        
        # Display the saved file path
        st.write(f"File saved to: {file_path}")

        lineArray = extractLinesFromPdf(file_path)
        updated_lineArray = []
        
        #collection_name = "nasa_base"
        #fulltext = ""
        #context = db.get_context_documents(collection_name, "Get the gist of the document")
        #ds = db.splitText(str(context.page_content))
        #r = ""
        #for d in ds:
        #    r += luna.prompt("", "Get the top 10 important points from " + str(d))
        #print(r)
        for line in lineArray:
            updated_lineArray.append(luna.prompt(s_prompt="", user_prompt = line))


    if True: #st.button("Start Processing") or st.session_state.processing_button_clicked == True:
        st.session_state.file_name = uploaded_files[0]
        st.session_state.processing_button_clicked = True

        if uploaded_files is None or len(uploaded_files) != 1:
            st.warning("Upload exactly 1 PDf files")
            st.stop()

        srcText = get_text_splitter(uploaded_files[0])
        edited_df = None
        try:
            st.write(
                    "LIST OF SUGGESTIONS. PLEASE SELECT AND ACCEPT"
                )

            # Cache the dataframe so it's only loaded once
            # @st.cache_data
            def load_data():
                d = []
                for i in range(len(lineArray)):
                    tmpStr = lineArray[i].strip()
                    if (len(tmpStr) > 0):
                        d.append({"Original Text":lineArray[i], "Editable Text":lineArray[i], "NASA Standards Copilot": updated_lineArray[i]})
                return pd.DataFrame(d
                    # [
                    #     for i in range(len(lineArray)):
                    #         tmpStr = lineArray[i].strip()
                    #         if (len(tmpStr) > 0):
                    #             {"Original Text":lineArray[i], "Editable Text": lineArray[i], "apply_Selection": True},
                    #     # {"Original Text":lineArray[0], "Editable Text": lineArray[0], "apply_Selection": True},
                    #     # {"Original Text":lineArray[1], "Editable Text": lineArray[1], "apply_Selection": True},
                    #     # {"Original Text":lineArray[2], "Editable Text": lineArray[2], "apply_Selection": True},
                    #     # {"Original Text":lineArray[3], "Editable Text": lineArray[3], "apply_Selection": True},
                    #     # {"Original Text":lineArray[4], "Editable Text": lineArray[4], "apply_Selection": True},
                    #     # {"Original Text":lineArray[5], "Editable Text": lineArray[5], "apply_Selection": True},
                    # ]
                )

            df = load_data()
            edited_df = st.data_editor(df, use_container_width = True,column_config = {
                "before Text": st.column_config.TextColumn(width="large"),
                "Editable Text": st.column_config.TextColumn(),
                "NASA Standards Copilot": st.column_config.TextColumn(),
            })
            #st.table(df)
            #edited_df = st.data_editor(df, column_config={
            #    "widgets": st.column_config.TextColumn(
            #        "Widgets",
            #        max_chars=5000,
            #    )
            #}) # 👈 An editable dataframe


        except Exception as e:

            st.error("Something went grong...")
            st.exception(e)
            st.stop()


        #st.snow()
        #edited_df = edited_df[(edited_df["apply_Selection"] ==True)] # & (edited_df["Original Text"] != edited_df["Editable Text"])]


        beforeArr = []
        afterArr = []

        #print("This is the length of the edited dtatafram: " + str(len(edited_df)))
        for i in range(len(edited_df)):
            fmatStr = edited_df.loc[i, "Original Text"].lstrip().rstrip()
            fmatAfterStr = edited_df.loc[i, "Editable Text"].lstrip().rstrip()
            #print(len(fmatStr))
            #print(fmatStr)
            if (fmatStr != "" and (edited_df.loc[i, "Original Text"] != edited_df.loc[i, "Editable Text"])):
                # now identify words changed
                print(fmatStr)
                print(fmatAfterStr)
                fmatStrArr = fmatStr.split()
                fmatAfterStrArr = fmatAfterStr.split()
                for i in range(len(fmatStrArr)):
                    if(fmatStrArr[i] !=  fmatAfterStrArr[i]):
                        beforeArr.append(fmatStrArr[i])
                        afterArr.append(fmatAfterStrArr[i]) 


            #print(edited_df.loc[i, "Original Text"], edited_df.loc[i, "Editable Text"], edited_df.loc[i, "apply_Selection"])
        print("pring array versions of changes in######################")
        print(beforeArr)
        print(afterArr)


        def load_final_changes():
            d = []
            for i in range(len(beforeArr)):
                d.append({"Original":beforeArr[i], "Changed": afterArr[i]})
            return pd.DataFrame(d)

        finalChangesDf = load_final_changes()
        st.write("SUMMARY OF CHANGES TO BE COMMITTED")
        st.table(finalChangesDf)

        if st.button("Apply Changes"):
            # Call the aspos cloud code to update pdf
            # print(edited_df["Original Text"])
            updatedFileName = updatePdf(file_path, beforeArr, afterArr)
            st.write(updatedFileName)

            # Display new updated pdf for downloading in browser 



########################### END OF CODE ################################

        # for i in range(len(edited_df)):
        #     #if(edited_df.loc[i, "apply_Selection"] == True):
        #     print(edited_df.loc[i, "Original Text"], edited_df.loc[i, "Editable Text"], edited_df.loc[i, "apply_Selection"])
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
        #             print(edited_df.loc[i, "Original Text"], edited_df.loc[i, "Editable Text"], edited_df.loc[i, "apply_Selection"])
        #         # else:
        #         #     edited_df = data.drop(0)
        #     edited_df = edited_df.loc[edited_df["apply_Selection"] ==True]
        #     st.table(edited_df)

   



