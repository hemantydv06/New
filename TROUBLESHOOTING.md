# Troubleshooting Missing Imports (Pandas)

If you see `ImportError: No module named 'pandas'` or similar in your IDE (VS Code, PyCharm, etc.), verify the following:

1.  **Check Python Interpreter**: Ensure your IDE is using the Python interpreter where dependencies are installed.
    *   **Current Interpreter Path**: `/usr/bin/python3` (or check with `which python3` in terminal)
    *   **Package Install Location**: `~/Library/Python/3.9/lib/python/site-packages`

2.  **Select Interpreter in VS Code**:
    *   Press `Cmd+Shift+P` -> Type "Python: Select Interpreter"
    *   Choose the interpreter path `/usr/bin/python3` (or the one matching your system python 3.9)

3.  **Verify Installation**:
    Run this command in your ter
    minal to confirm everything is installed:
    ```bash
    python3 -c "import pandas, streamlit; print('All good!')"
    ```

4.  **Run the App**:
    Use this command to start the app:
    ```bash
    python3 -m streamlit run app_light.py
    ```
