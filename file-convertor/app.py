import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Convertor", layout="wide")
st.title("File Convertor & Cleaner")
st.write("upload your files , clean your data and convert formats.")

files = st.file_uploader("Upload your files here" , type = ["csv", "xlsx" ,"excel"],accept_multiple_files=True)
if files :
    for file in files :
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("successfully Removed Duplicates")
            st.dataframe(df.head())
    #  # Condition 01:
    #         if st.checkbox(f"File Missing values - {file.name}"):
    #             if not df.select_dtypes(include=["number"]).empty:
    #               df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
    #               st.success("Missing values filled with mean")
    #   # Conditio 02: 
    #             elif not df.select_dtypes(include=["object"]) .empty:
    #               for column in df.select_dtypes(include=["object"]).columns: 
    #                 df[column] .fillna(df[column] .mode()[0] , inplace=True)
    #                 st.succes("Missing values filled with mode")   
    #   # Condition 03:  
    #             else:
    #               df.fillna("Unknown" , inplace = True) 
    #               st.success("Missing values filled with Unknown")           
                  
    #               st.dataframe(df.head())


            selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
            df = df[selected_columns]
            st.dataframe(df.head())

            if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
              st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])


            format_Choice = st.radio(f"Convert {file.name} to:" ,["csv","Excel"], key=file.name)

            if st.button(f"Download {file.name} as {format_Choice}"):
                output = BytesIO()
                if format_Choice == "csv":
                    df.to_csv(output , index = False)
                    mine = "text/csv"
                    new_name = file.name.replace(ext , "csv")
                else:
                    df.to_excel(output , index = False , engine="openpyxl")
                    mine = "application/vnd openxmlformats.officedocument.spreadsheetml.sheet"
                    new_name = file.name.replace(ext , "xlsx")

                    output.seek(0)
                    st.download_button("Download file" ,file_name=new_name , data=output , mime=mine)
                    st.success("Processing Complete!")    