python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip list

pip freeze > requirements.txt

pip install -r requirements.txt


# File: requirements.txt
streamlit==1.31.0
pandas==2.2.0
requests==2.31.0
openpyxl==3.1.2
lxml==4.9.3
