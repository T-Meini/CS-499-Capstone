Installation and How To Run

1. Ensure that the following are installed on your system (This guide will be only support Windows PCs):
	- Python 3.8 or later (https://www.python.org/downloads/)
	- MongoDB (https://www.mongodb.com/try/download/community)

2. Download, Unzip, and Move the "Databases Enhancement" folder to a location of your choosing

3. Open Command Prompt (make sure to "Run as Administrator" to avoid any issues"

4. Navigate to the location in which the dashboard is located using "cd" command in Command Prompt(ie. "cd C:\Users\<user>\Desktop\Databases Enhancement")

5. Now you will set up a Python Virtual Environment, for this run the following commands:
```
python -m venv venv
```
```
venv\Scripts\activate
```
6. You will now need the following dependencies for this project to work:
    - blinker
    - click
    - colorama
    - dnspython
    - Flask
    - itsdangerous
    - Jinja2
    - MarkupSafe
    - narwhals
    - numpy
    - packaging
    - pandas
    - plotly
    - pymongo
    - python-dateutil
    - python-dotenv
    - pytz
    - six
    - tzdata
    - Werkzeug

	You will run this command after you have set up and activated your virtual environment:
```
pip install blinker click colorama dnspython Flask itsdangerous Jinja2 MarkupSafe narwhals numpy packaging pandas plotly pymongo python-dateutil python-dotenv pytz six tzdata Werkzeug
```
7. You are also provided a .env file that has your unique credentials to access the MongoDB Atlas database (this replaces having the database locally).
   
	Put your .env file into the root "dashboard" folder for the program to work

8. Run the following command to start the web app:
```
python app.py
```
9. Once you confirm that it is running in the command prompt, navigate to the following address to see the page:

	http://127.0.0.1:5000/
