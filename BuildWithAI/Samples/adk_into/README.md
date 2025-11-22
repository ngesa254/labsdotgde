Install uv

curl -LsSf https://astral.sh/uv/install.sh | sh

Make it usable in your current shell by sourcing the environment file the installer mentioned.

Run this exactly as shown:

source $HOME/.local/bin/env


Then confirm it worked:

uv --version


Create a virtual environment
uv venv .venv

🧠 2️⃣ Activate it
source .venv/bin/activate


You can confirm activation by checking:

echo $VIRTUAL_ENV

uv sync


pip install google-adk

deactivate
