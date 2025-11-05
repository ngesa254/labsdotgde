# Create a Virtual Environment & Install Dependencies

## Why Use a Virtual Environment?

Before starting any Python project, it's good practice to create a virtual environment. This isolates the project's dependencies, preventing conflicts with other projects or the system's global Python packages.

> **Note:** We'll be using `uv` to create our virtual environment instead of the standard `venv` package. It's an incredibly fast Python package and project manager written in Rust. You can learn more about it in the official [uv documentation](https://docs.astral.sh/uv/).

## Setup Instructions

1. Create a folder named `wanderbot` to store the code for your travel assistant app. Run the following code in the terminal:

   ```shell
   mkdir wanderbot && cd wanderbot
   ```

2. Create and activate a virtual environment:

   ```shell
   uv venv --python 3.12
   source .venv/bin/activate
   ```

   You'll see `(wanderbot)` prefixing your terminal prompt, indicating the virtual environment is active. It would look something like this:

   ```
   (wanderbot) user@cloudshell:~/wanderbot$
   ```

---

> **💡 Important**  
> If you close the terminal and return later, you will need to go into the `wanderbot` folder and execute `source .venv/bin/activate` again.

---

**Next Steps:** With your virtual environment activated, you're ready to install project dependencies and begin development.