
#First create Datapao virtual environment and activate it
python -m virtualenv Datapao
Datapao\Scripts\activate

#Second install the required packages
pip install -r requirements.txt

# to run the main code
python imdb.py

# to run the test code
python test_imdb.py
