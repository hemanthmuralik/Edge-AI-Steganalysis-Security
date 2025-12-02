name: Model Quality Check

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3  # Updated to v3
    
    - name: Set up Python
      uses: actions/setup-python@v4 # Updated to v4
      with:
        python-version: '3.9'
        cache: 'pip'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        # Use tensorflow-cpu for faster install in CI (no GPU needed for architecture check)
        pip install tensorflow-cpu==2.15.0 numpy opencv-python-headless
        
    - name: 🔍 Debug File Structure
      run: |
        echo "Listing all files in repository:"
        find . -maxdepth 3 -not -path '*/.*'
        
    - name: Verify Model Architecture
      env:
        PYTHONPATH: ${{ github.workspace }}
      run: |
        python -c "import sys; print('Python Path:', sys.path); from models.ye_net import build_yenet; model = build_yenet(); model.summary(); print('✅ Ye-Net Compiled Successfully')"
