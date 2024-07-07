# Semantic Search for Resumes

## Project Overview
This project enables semantic search over a dataset of resumes in PDF format. It allows users to search for resumes based on queries and ranks them according to relevance.

## Instructions

### Setting Up the Dataset
1. **Create a Folder for Resume Dataset:**
   - Create a folder named `resume_dataset` in the root directory of this repository.
   - Add all the resume PDF files to this folder.

### Running the Streamlit App
2. **Running the Streamlit Application:**
   - Open a terminal.
   - Navigate to the root directory of the repository.
   - Run the following command:
     ```bash
     streamlit run main_app.py
     ```
   - This will start the Streamlit app for interactive use.

### Running the FastAPI Backend
3. **Running the FastAPI Backend for API Usage:**
   - Navigate to the `backend` folder.
   - Open a terminal in this folder.
   - Run the following command:
     ```bash
     python semantic_search_with_api.py
     ```
   - This will start the FastAPI server for API-based semantic search.

## Notes
- Ensure Python and necessary dependencies are installed as per `requirements.txt`.
- For detailed setup and usage instructions, refer to the respective README files in relevant folders.

Feel free to reach out for any questions or support!
