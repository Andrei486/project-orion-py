python -m venv
"./venv/Scripts/activate.bat"
pip install -r requirements.txt
mkdir "./venv/Lib/site-packages/fpdf/font"
robocopy "./resources/font" "./venv/Lib/site-packages/fpdf/font"