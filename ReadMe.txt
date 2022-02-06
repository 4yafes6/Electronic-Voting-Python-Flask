this program is under construction
database -> MySql
code editor -> Visual Studio Code
used

The purpose of this program is biometric-based on the web.
electronic voting

While registering, it asks for your e-mail address and sends you a code.
If you enter the code sent correctly, it requests and saves your face data.
Afterwards, when you enter the correct ID number and password while logging in, you will be asked.
asks for your face data and sees whether it matches the face you provided when registering.
checking is true, login is successful

1- PYTHON INSTALLATION
You have run the file named " python-3.8.0-amd64.exe " and
Check "ADD PATH" option during installation

2- DOWNLOADING MODULES
Open cmd, go to the folder where the files are and write the following codes
' python -m pip install --upgrade pip '
' pip install -r requirements.txt '

3- DATABASE SETUP
database only works in MySql, download MySql
To create databases, open a database named " flask_db "
open a query and write the codes in database.txt and work
Thus, 3 tables will be created in the flask_db database.

4- EDIT DATABASE
Code sections between lines 12 and 17 in the app.py file
edit according to your own database
(such as host, user, passwd)

5- MAIL ORGANIZATION
Open the mail2.py file
Write your own e-mail in the mailaddress = "deme@mail.com" field on line 19.
Type your own password in the password = "password" field on line 20.
