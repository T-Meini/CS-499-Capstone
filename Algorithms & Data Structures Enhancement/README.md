# Installation and How To Run

1. Ensure that the following are installed on your system (This guide will be only support Windows PCs):
	- Python 3.8 or later (https://www.python.org/downloads/)
	- MongoDB (https://www.mongodb.com/try/download/community)

2. Download, Unzip, and Move the "Algorithms & Data Structures Enhancement" folder to a location of your choosing

3. Open Command Prompt (make sure to "Run as Administrator" to avoid any issues"

4. Navigate to the location in which the dashboard is located using "cd" command in Command Prompt(ie. "cd C:\Users\<user>\Desktop\Algorithms & Data Structures Enhancement")

5. Now you will set up a Python Virtual Environment, for this run the following commands:
```
python -m venv venv
```
```
venv\Scripts\activate
```	
6. You will now need the following dependencies for this project to work:
	- Flask
	- pandas
	- plotly
	- pymongo
	- numpy
	- Werkzeug
	
	You will run this command after you have set up and activated your virtual environment: 
```
pip install flask pandas plotly pymongo numpy werkzeug
```
**(IF YOU UPLOADED THE CSV FOR THE PREVIOUS ENHANCEMENT, SKIP STEP 7)**

7. Run the "csv_to_mongodb" python file to import the csv into MongoDB using the following command:
```
python csv_to_mongodb.py
```
8. Once the csv has been successfully imported to MongoDB, run the following command to start the web app:
```
python app.py
```
9. Once you confirm that it is running in the command prompt, navigate to the following address to see the page:

	http://127.0.0.1:5000/
