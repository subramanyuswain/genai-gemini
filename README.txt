List all python Environments
    conda env list

Activate training environment
    conda activate venv/

Create python environment
    conda create -p python=3.10.4 -y

Install project reqired libraries - reading library names from requirements.txt file
    pip install -r requirements.txt

Run Streamlit app
    streamlit run app.py