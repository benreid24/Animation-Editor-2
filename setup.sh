pip install virtualenv
virtualenv venv
source venv/Scripts/activate
pip install -r requirements.txt
python compile.py build
cp -R build/*/* ./
