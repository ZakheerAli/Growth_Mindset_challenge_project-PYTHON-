import streamlit as st
import pandas as pd 
from io import BytesIO
import os


st.set_page_config(page_title="💾DATA SWEEPER" ,layout="wide")
st.title("💾DATA SWEEPER")
st.write("Tansform your files between csv and Excel format")

uploaded_files=st.file_uploader("Upload your files (CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext=os.path.splitext(file.name)[-1].lower()

        if file_ext==".csv":
            df=pd.read_csv(file)
        elif file_ext==".xlsx":
            df=pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

    #show file info
    st.write(f"**File Name:** {file.name}")
    st.write(f"**File Size:** {file.size/1024}")
 
    #show 5 rows of df
    st.write("Preview the Head of the DataFrame")
    st.dataframe(df.head())

    #option for data cleaning
    st.subheader("🧹Data Cleaning Options")
    if st.checkbox(f"Clean Data for {file.name}"):
        col1,col2=st.columns(2)

        with col1:
            if st.button(f"Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates Removed!")
        
        with col2:
            if st.button(f"Fill missing valuesm for {file.name}"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing Values have been Filled!")

    #choose specific columns to convert
    st.subheader("Select columns to Convert")
    columns=st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
    df=df[columns]

    #Create some visualization
    st.subheader("📊Data Visualization")
    if st.checkbox(f"Show Visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

    #Convert the file -> csv to excel
    st.subheader("🔄Conversion Options")
    conversion_type=st.radio(f"Convert {file.name} to :" , ["CSV","Excel"] , key=file.name)
    if st.button(f"Convert {file.name}"):
        buffer=BytesIO()
        if conversion_type=="CSV":
            df.to_csv(buffer, index=False)
            file_name=file.name.replace(file_ext, ".csv")
            mime_type="text/csv"
        elif conversion_type=="Excel":
            df.to_excel(buffer ,index=False)
            file_name = file.name.replace(file_ext , ".xlsx")
            mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)

        #download button
        st.download_button(
            label=f"🔽Download {file.name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )

        st.success("ALL FILES PROCESSED")
        