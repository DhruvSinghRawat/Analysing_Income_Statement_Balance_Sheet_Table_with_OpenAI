# 📄 PDF Table Extraction & Summarization
Welcome to the PDF Table Extraction & Summarization project! This application allows you to effortlessly upload PDF documents, extract tables from them, and generate concise summaries using advanced AI models. Built with Streamlit, this tool offers a seamless and interactive user experience.

🚀 Features
📤 Upload PDFs: Easily upload your PDF documents through a user-friendly interface.
👀 Preview PDFs: View the content of your PDFs directly within the application.
📊 Extract Tables: Automatically detect and extract tables from your uploaded PDFs.
📝 Summarize Tables: Generate insightful summaries of each extracted table using AI-powered summarization.
🧹 Automatic Cleanup: Ensures temporary files are deleted after processing to maintain security and efficiency.
🛠️ Installation
Follow these steps to set up the project locally:

🔀 Clone the Repository:

git clone https://github.com/jitendra-789/Analysing_Income_Statement_with_LLM.git
📥 Install Required System Dependencies:

⚠️ Python Compatibility: This project requires Python version 3.9 to 3.11 (3.10 recommended). Python 3.13 is not supported by some dependencies.

Version Notes:

✅ Python 3.9: Fully compatible
✅ Python 3.10: Recommended version (best stability)
✅ Python 3.11: Compatible but some packages might need additional setup
❌ Python 3.8: Too old, missing required features
❌ Python 3.12+: Not supported by key dependencies
First, ensure you have the correct Python version:

# Check Python version
python --version  # Windows
python3 --version  # macOS/Linux
Windows:

# Install Python 3.10 if needed
winget install Python.Python.3.10

# Create virtual environment with Python 3.10
py -3.10 -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Verify Python version
python --version  # Should show Python 3.10.x
macOS/Linux:

# Install Python 3.10 if needed
brew install python@3.10

# Create virtual environment with Python 3.10
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip3 install --upgrade pip

# Verify Python version
python3 --version  # Should show Python 3.10.x
If you have multiple Python versions installed, you can also use these alternative paths:

# Windows alternative
C:\Python310\python -m venv venv

# macOS alternative (Intel)
/usr/local/opt/python@3.10/bin/python3.10 -m venv venv

# macOS alternative (Apple Silicon)
/opt/homebrew/opt/python@3.10/bin/python3.10 -m venv venv
If you encounter any PyTorch-related errors:

Visit PyTorch Get Started
Select your operating system and preferences
Use the provided installation command before installing other requirements
Windows:

# Install Poppler
winget install poppler
# OR download from: http://blog.alivate.com.au/poppler-windows/

# Install Tesseract
winget install tesseract-ocr
# OR download installer from: https://github.com/UB-Mannheim/tesseract/wiki
macOS:

First, install Homebrew if you haven't already:

# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# After installation, add Homebrew to your PATH:
# For Intel Macs
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zshrc
# For Apple Silicon Macs
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc

# Reload your shell configuration
source ~/.zshrc
Then install the required dependencies:

# Install Poppler
brew install poppler

# Install Tesseract
brew install tesseract
📦 Install Dependencies:

pip install -r requirements.txt
🔑 Configure Hugging Face:

a. Create a Hugging Face account at https://huggingface.co/

b. Generate an access token:

Go to https://huggingface.co/settings/tokens
Click "New token"
Name your token and select "read" role
Copy the generated token
c. Login using the CLI:

Windows:

huggingface-cli login
# Enter your token when prompted
macOS/Linux:

huggingface-cli login
# Enter your token when prompted
d. Set up environment variable:

Windows:

setx HUGGING_FACE_TOKEN "your_token_here"
macOS/Linux:

echo "export HUGGING_FACE_TOKEN='your_token_here'" >> ~/.zshrc
# OR for bash
echo "export HUGGING_FACE_TOKEN='your_token_here'" >> ~/.bashrc
🖥️ Usage
Run the Streamlit application using the following command:

streamlit run app.py

Once the application starts, follow these steps:

📂 Upload Your PDF:

Navigate to the sidebar and use the file uploader to select your PDF document.
🔍 Preview the PDF:

After uploading, the application will display a preview of your PDF.
📑 Extract Tables:

The app will automatically extract tables from the PDF. View them in expandable sections.
📝 Summarize Tables:

Generate and view summaries for each extracted table.
📁 Project Structure
pdf-table-extraction/

├── app.py
├── requirements.txt
├── utils/
│ ├── table_extraction.py
│ └── summarization.py
├── README.md
└── assets/
└── icons/

app.py: The main Streamlit application file.
requirements.txt: Lists all the project dependencies.
utils/: Contains utility modules for table extraction and summarization.
assets/: (Optional) Directory to store images, icons, or other assets.
🧰 Dependencies
The project relies on the following key libraries:

Streamlit: For building the interactive web application.
Pandas: For data manipulation and analysis.
PyPDF2: For reading and handling PDF files.
Mistralai: For AI-powered summarization (ensure it's correctly installed and configured).
Full List of Dependencies:

streamlit pandas PyPDF2 mistralai

🌐 Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the Repository

Create a New Branch:

git checkout -b feature/YourFeature
Commit Your Changes:

git commit -m "Add your message here"
Push to the Branch:

git push origin feature/YourFeature
Open a Pull Request


