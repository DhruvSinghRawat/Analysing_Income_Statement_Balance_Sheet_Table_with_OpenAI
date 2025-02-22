
import streamlit as st
from utils.table_extraction import extract_tables_from_pdf
from utils.summarization import  summarize_table
import pandas as pd
import os
import uuid
from mistralai import Mistral
from PyPDF2 import PdfReader  # Added for PDF previewpip install opencv-python-headless

import base64


def main():
    # Set page configuration
    st.set_page_config(
        page_title="📄 PDF Table Extraction & Summarization",
        layout="wide",
        page_icon="📈",
    )
    
    # Custom CSS for additional styling
    st.markdown("""
        <style>
            /* Header Container Styling */
            .header-container {
                background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            /* Section Container Styling */
            .section {
                background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            /* Header Text Styling */
            .header {
                font-size: 2.5em;
                font-weight: 800;
                text-align: center;
                background: linear-gradient(120deg, #0D6EFD 0%, #0B5ED7 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
                padding: 10px;
                letter-spacing: 1px;
            }

            /* Subheader Styling */
            .subheader {
                font-size: 1.8em;
                font-weight: 600;
                background: linear-gradient(120deg, #0D6EFD 0%, #0B5ED7 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-top: 20px;
                margin-bottom: 10px;
                text-align: left;
            }

            /* Table Container Styling */
            .table-container {
                background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }

            /* Dark mode adjustments */
            @media (prefers-color-scheme: dark) {
                .header-container {
                    background: linear-gradient(135deg, #212529 0%, #343A40 100%);
                }
                
                .section {
                    background: linear-gradient(135deg, #212529 0%, #2B3035 100%);
                }
                
                .table-container {
                    background: linear-gradient(135deg, #212529 0%, #2B3035 100%);
                }
                
                .header {
                    background: linear-gradient(120deg, #6EA8FE 0%, #9EC5FE 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                
                .subheader {
                    background: linear-gradient(120deg, #6EA8FE 0%, #9EC5FE 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
            }

            /* Button Styling */
            .stButton > button {
                background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                transition: all 0.3s ease;
            }

            .stButton > button:hover {
                background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            }

            /* Tab Styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 24px;
                background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
                padding: 10px;
                border-radius: 10px;
            }

            .stTabs [data-baseweb="tab"] {
                background-color: transparent;
                border-radius: 4px;
                color: #1976D2;
                font-weight: 600;
                padding: 10px 16px;
            }

            .stTabs [aria-selected="true"] {
                background: linear-gradient(120deg, #2196F3 0%, #1976D2 100%);
                color: white;
            }

            /* Dark mode tab adjustments */
            @media (prefers-color-scheme: dark) {
                .stTabs [data-baseweb="tab-list"] {
                    background: linear-gradient(135deg, #212529 0%, #343A40 100%);
                }
                
                .stTabs [data-baseweb="tab"] {
                    color: #82B1FF;
                }
                
                .stTabs [aria-selected="true"] {
                    background: linear-gradient(120deg, #448AFF 0%, #2979FF 100%);
                }
            }

            /* Message Styling */
            .success {
                background: linear-gradient(135deg, #43A047 0%, #2E7D32 100%);
                color: white;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }

            .error {
                background: linear-gradient(135deg, #E53935 0%, #C62828 100%);
                color: white;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }

            .warning {
                background: linear-gradient(135deg, #FB8C00 0%, #F57C00 100%);
                color: white;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Update the header with container
    st.markdown("""
        <div class="header-container">
            <h1 class="header">📄 PDF Table Extraction and Summarization</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Move temp_filename to session state to persist across reruns
    if 'temp_filename' not in st.session_state:
        st.session_state.temp_filename = None
    
    # Sidebar for file upload
    with st.sidebar:
        st.markdown('<h2 style="color: white;">Upload Your PDF</h2>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            # Clean up previous temporary file if it exists
            if st.session_state.temp_filename and os.path.exists(st.session_state.temp_filename):
                try:
                    os.remove(st.session_state.temp_filename)
                except Exception as e:
                    st.warning(f"Could not delete previous temporary file: {e}")
            
            # Save uploaded file to a unique temporary location
            st.session_state.temp_filename = f"temp_{uuid.uuid4().hex}.pdf"
            with open(st.session_state.temp_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.markdown('<div class="success">✅ PDF Uploaded Successfully!</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        try:
            # ------------------ Preview Section ------------------
            st.markdown('<div class="section">', unsafe_allow_html=True)

            # Create columns for the header and controls
            header_col, control_col = st.columns([3, 1])

            with header_col:
                st.markdown('<div class="subheader">📖 PDF Preview</div>', unsafe_allow_html=True)

            with control_col:
                # Add zoom controls
                zoom_level = st.select_slider(
                    "Zoom",
                    options=[50, 75, 100, 125, 150, 200],
                    value=100,
                    format_func=lambda x: f"{x}%"
                )

            try:
                with open(st.session_state.temp_filename, "rb") as f:
                    pdf_bytes = f.read()
                    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                    
                    # Get PDF info
                    pdf_reader = PdfReader(st.session_state.temp_filename)
                    num_pages = len(pdf_reader.pages)
                    
                    # Create tabs for different view modes
                    preview_tab, info_tab = st.tabs(["📄 Preview", "ℹ️ Document Info"])
                    
                    with preview_tab:
                        # Add page navigation if multiple pages
                        if num_pages > 1:
                            current_page = st.slider("Page", 1, num_pages, 1)
                            st.markdown(f"**Page {current_page} of {num_pages}**")
                        
                        # Enhanced PDF display with zoom control
                        pdf_display = f"""
                            <div style="display: flex; justify-content: center;">
                                <iframe 
                                    src="data:application/pdf;base64,{base64_pdf}#page={current_page if num_pages > 1 else 1}" 
                                    width="100%" 
                                    height="600" 
                                    style="zoom: {zoom_level}%;"
                                    type="application/pdf">
                                </iframe>
                            </div>
                        """
                        st.markdown(pdf_display, unsafe_allow_html=True)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_bytes,
                            file_name="document.pdf",
                            mime="application/pdf"
                        )
                    
                    with info_tab:
                        # Display PDF metadata and information
                        st.markdown("### 📑 Document Information")
                        
                        # Create two columns for metadata
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Pages:** {num_pages}")
                            if pdf_reader.metadata:
                                if pdf_reader.metadata.get('/Title'):
                                    st.markdown(f"**Title:** {pdf_reader.metadata.get('/Title')}")
                                if pdf_reader.metadata.get('/Author'):
                                    st.markdown(f"**Author:** {pdf_reader.metadata.get('/Author')}")
                        
                        with col2:
                            st.markdown(f"**File Size:** {len(pdf_bytes)/1024:.1f} KB")
                            if pdf_reader.metadata:
                                if pdf_reader.metadata.get('/CreationDate'):
                                    st.markdown(f"**Created:** {pdf_reader.metadata.get('/CreationDate')}")
                                if pdf_reader.metadata.get('/ModDate'):
                                    st.markdown(f"**Modified:** {pdf_reader.metadata.get('/ModDate')}")

            except Exception as e:
                st.markdown(f'<div class="error">⚠️ Error previewing PDF: {str(e)}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # ------------------ Extracted Tables Section ------------------
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="subheader">📊 Extracted Tables</div>', unsafe_allow_html=True)

            with st.spinner("🔄 Extracting tables from PDF..."):
                try:
                    dfs, table_html = extract_tables_from_pdf(st.session_state.temp_filename)
                except Exception as e:
                    st.markdown(f'<div class="error">⚠️ Error extracting tables: {e}</div>', unsafe_allow_html=True)
                    return

            if dfs:
                # Display tables one after another
                for idx, df in enumerate(dfs):
                    st.markdown('<div class="table-container">', unsafe_allow_html=True)
                    
                    # Table header
                    st.markdown(f"### 📋 Table {idx + 1}")
                    
                    # Display table
                    st.dataframe(df, use_container_width=True)
                    
                    # Download button for table
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=f"📥 Download Table {idx + 1} as CSV",
                        data=csv,
                        file_name=f"table_{idx + 1}.csv",
                        mime="text/csv",
                    )
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning">⚠️ No tables found in the uploaded PDF.</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # ------------------ Summarization Section ------------------
            st.markdown('<div class="section"><div class="subheader">📝 Summarization</div>', unsafe_allow_html=True)
            if dfs:
                # llm_pipeline = initialize_llm_pipeline()
                # Summarization
                st.header("📝 Summarization")
                try:
                    for idx, df in enumerate(dfs):
                        table_text = df.to_string(index=False)
                        summary = summarize_table(table_text)
                        st.subheader(f"Summary of Table {idx + 1}")
                        
                        st.write(summary)
                except Exception as e:
                    st.markdown(f'<div class="error">⚠️ Error during summarization: {e}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        finally:
            # Clean up temporary file after all operations
            if st.session_state.temp_filename and os.path.exists(st.session_state.temp_filename):
                try:
                    # Close any open file handles
                    import gc
                    gc.collect()  # Force garbage collection
                    
                    # Try to delete the file
                    os.remove(st.session_state.temp_filename)
                    st.session_state.temp_filename = None
                except Exception as e:
                    st.warning(f"⚠️ Could not delete temporary file: {e}. The file will be cleaned up in the next session.")
                    # Log the error for debugging
                    print(f"File cleanup error: {e}")


if __name__ == "__main__":
    main()
