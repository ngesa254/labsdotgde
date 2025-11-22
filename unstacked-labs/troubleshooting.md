mkdir wanderbot && cd wanderbot
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install streamlit google-genai requests



ls -la



gcloud auth list


gcloud auth revoke marvinngesa@gmail.com

gcloud auth revoke marvinngesa@gmail.com || true


gcloud auth login --account=ngesa.marvin@gmail.com --update-adc


gcloud config set account ngesa.marvin@gmail.com


gcloud auth list
gcloud config list



# Add login credentials for ngesa.marvin@gmail.com (you'll get a browser link)
gcloud auth login --account=ngesa.marvin@gmail.com --update-adc

# Set that as the active account
gcloud config set account ngesa.marvin@gmail.com


