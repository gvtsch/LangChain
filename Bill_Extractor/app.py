import streamlit as st
from helper_functions import *

def main():
    st.set_page_config(page_title="PDF Bill Extractor", layout="wide")
    st.title("PDF Bill Extractor 🧾")
    st.write("Upload PDF bills to extract key information.")
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type="pdf", 
        accept_multiple_files=True)

    extract_button = st.button("Extract Data")
    if extract_button and uploaded_files:
        with st.spinner("Extracting data from PDFs..."):
            data_frame = create_docs(uploaded_files)
        st.success("Data extraction complete!")
        st.write("Average Bill Amounts:")
        data_frame["Amount"] = data_frame["Amount"].astype(float)
        st.write(data_frame['Amount'].mean())


        with st.spinner("Converting to CSV..."):
            csv_data = data_frame.to_csv(index=False).encode('utf-8')
            
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name='extracted_data.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()