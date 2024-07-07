# Resume Dataset and Semantic Search System

## Introduction
This repository contains code for building a semantic search system for resumes using Python. The system allows you to input a query and find the top matching resumes from a dataset of PDF files.

## Setup Instructions

### Step 1: Clone the Repository
Clone this repository to your local machine using Git:
```bash
git clone https://github.com/your-username/resume-semantic-search.git
cd resume-semantic-search


resume-semantic-search/
├── resume_dataset/
│   ├── resume1.pdf
│   ├── resume2.pdf
│   ├── ...
│   └── resumeN.pdf
├── backend/
│   ├── semantic_search_with_api.py
│   └── ...
├── main_app.py
└── README.md

To run the Streamlit application, execute the following command from the root directory:
streamlit run main_app.py

Navigate to the backend folder:
cd backend

Run the FastAPI server for the semantic search API:

python semantic_search_with_api.py
