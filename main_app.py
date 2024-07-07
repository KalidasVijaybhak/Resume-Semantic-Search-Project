import streamlit as st
import re
import os
import numpy as np
import webbrowser  # For opening in default PDF viewer
from response import Analyst
import requests
import json
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
 
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'edit_inputs' not in st.session_state:
    st.session_state.edit_inputs = {}
st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

st.markdown("""<style>.css-zt5igj svg{display:none}</style>""", unsafe_allow_html=True)

analyst = Analyst()
pdf_content_directory = os.path.join(os.path.dirname(__file__), 'resume_content')

# Load the data from the NumPy file into a numpy array
file_path = os.path.join(pdf_content_directory, 'pdf_content.npy')
pdf_contents = np.load(file_path, allow_pickle=True)
loaded_dict = dict(pdf_contents)

# print(loaded_dict['21dcs013@charusat.edu.in_resume.pdf'])

def open_pdf(directory, filename):
    """
    Opens a PDF file from the specified directory using the user's default PDF viewer.

    Args:
        directory (str): The path to the directory containing the PDF file.
        filename (str): The name of the PDF file to open.

    Returns:
        None
    """

    # Construct the complete file path
    full_path = os.path.join(directory, filename)

    # Check if the file exists
    if not os.path.isfile(full_path):
        print(f"Error: File '{filename}' not found in directory '{directory}'.")
        return

    # Open the PDF using the default PDF viewer
    try:
        webbrowser.open(full_path)
    except webbrowser.exceptions.OSError:
        print("Error: Could not open PDF using the default viewer. "
            "Please ensure you have a PDF viewer installed.")
    
# Example usage


def result(str):
    response = analyst.generate_response(str)
    return response

def send_query(query_text):
    url = "http://localhost:8000/retrieve"
    payload = {"text": query_text}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.search_results = data['metadata']
            display_results()
        else:
            st.error(f"Error: Received status code {response.status_code}")
            st.text(response.text)

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
    except json.JSONDecodeError:
        st.error("Failed to decode the response as JSON")
    except KeyError:
        st.error("The response doesn't contain the expected 'metadata' key")

def display_results():
    pdf_directory = os.path.join(os.path.dirname(__file__), 'resume_dataset')
    if st.session_state.search_results:
        st.subheader("Search Results")
        for i, item in enumerate(st.session_state.search_results):
            source = item.get('source', 'No source available')
            with st.container(border=True):
                pattern = r'(?<=\/content\/drive\/MyDrive\/RESUMES\/resume_dataset \(1\)\/)([^@]+)(?=@gmail\.com_resume\.pdf)'
                match = re.search(pattern, source)
                pdf_open = r'(?<=\/content\/drive\/MyDrive\/RESUMES\/resume_dataset \(1\)\/)([^\/]+)$' 
                match_pdf = re.search(pdf_open, source)

                if match_pdf:
                    filename_pdf = match_pdf.group(0)
                    # st.subheader(filename)
                if match:
                    filename = match.group(0)
                    st.subheader(filename)
                 
                      
                    st.session_state.edit_inputs[i] = loaded_dict[filename_pdf]
                col1, col2, col3 = st.columns([1,1,1])
                with col1:
                    edit_button_key = f"edit_{i}"
                    c_edit_button = st.button('Generate Report', key=edit_button_key)
                    if c_edit_button:
                        with st.spinner('Loading'):
                            st.write(result(st.session_state.edit_inputs[i]))
                            
                    # st.write(source)
                with col2:
                    open_button_key = f"open_{i}"
                    open_button = st.button('Open Resume', key=open_button_key)
                    if open_button:
                        with st.spinner('Loading'):
                            open_pdf(pdf_directory, filename_pdf)
                            
                st.code(filename_pdf)

def main():
    st.title("Resume Semantic Search Project")

    query = st.text_input("Enter your search query")
    
    if st.button("Search"):
        if query:
            with st.spinner('Loading'):
                send_query(query)
    
    # Display results if they exist in session state
    try: 
        if st.session_state.search_results:
            display_results()
    except:
        "End"

if __name__ == "__main__":
    main()