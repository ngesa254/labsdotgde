## ⚙️ Project Setup and Google Cloud Authentication (README.md)

Follow these steps to initialize your project environment, install necessary dependencies, and authenticate with Google Cloud for API access.

### Prerequisites

  * **Python 3.x**
  * **`gcloud` CLI** installed and configured.

-----

### Step 1: Initialize Project Directory

Create the project folder and navigate into it.

```bash
mkdir wanderbot
cd wanderbot
```

### Step 2: Create and Activate Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Python Packages

Install the project dependencies, including Streamlit, Google GenAI SDK, and requests.

```bash
pip install --upgrade pip
pip install streamlit google-genai requests
```

### Step 4: Verify Directory Contents

Confirm the virtual environment and potential project files are present.

```bash
ls -la
```

-----

## 🔑 Google Cloud Authentication

The following steps are required to authenticate your local environment with Google Cloud, allowing the application to use your configured services.

> **Note:** **Replace `<YOUR_EMAIL>`** in the commands below with the email address you wish to use for Google Cloud authentication.

### Step 5: Check Authentication Status

View the currently logged-in `gcloud` accounts.

```bash
gcloud auth list
```

### Step 6: Revoke Previous Credentials (Optional Cleanup)

It is often helpful to clear old credentials before logging in again.

```bash
gcloud auth revoke <YOUR_EMAIL>
gcloud auth revoke <YOUR_EMAIL> || true
```

### Step 7: Log In to Google Cloud and Update ADC

This command will open a browser window for you to complete the login process and update your Application Default Credentials (ADC).

```bash
gcloud auth login --account=<YOUR_EMAIL> --update-adc
```

### Step 8: Set the Active Account

Ensure the application uses the correct account for configuration.

```bash
gcloud config set account <YOUR_EMAIL>
```

### Step 9: Confirm Final Status

Verify that the authentication and configuration settings are correct.

```bash
gcloud auth list
gcloud config list
```