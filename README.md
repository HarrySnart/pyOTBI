# pyOTBI
simply python library for connecting to Fusion OTBI (unofficial)

# What is pyOTBI?
pyOTBI is a simple python library which acts as a wrapper to the embedded analytics of Oracle Fusion Application, OTBI (Oracle Transactional BI).
Note – pyOTBI is an unofficial and unlicensed python library. It comes with no warranty and is currently under beta build. It has been built and tested with Python 3.7 and Windows 10

# Why use pyOTBI?
The native SOAP APIs can be difficult to use to run queries against OTBI, however these APIs can be incredibly useful for both administrative and analytical tasks. pyOTBI gives a simple python library to post and parse complex SOAP requests in very few lines of code

# How to install pyOTBI?
You can install pyOTBI from github using Python’s pip library.
python –m pip install git+https://github.com/HarrySnart/pyOTBI

# Code examples
```python
# set environment details (consider keyring instead of storing passwords in plain text)
import pyOTBI
host = 'https://myfusionpod.oracledemos.com' # don’t add /analytics to OTBI host
user = 'my.user' # add username of OTBI account
password = 'mypassword' # user password
# create an OTBI connection object
OTBI = pyOTBI.connect(host,user,password)
# viewing your current user
myUser = OTBI.getCurlUser()
print(myUser)
# search for a user
userDetails = OTBI.searchUser(‘lisa.jones’)
print(userDetails)
# document all subject areas as a pandas dataframe
subject_areas = OTBI.listSubjectAreas()
subject_areas.head()
# execute logical SQL query to pandas dataframe
sql_query = '''SELECT "Sales - CRM Contacts"."Contact"."Full Name" FROM "Sales - CRM Contacts"'''
sqldf = OTBI.logicalSQLtoPandas(sql=sql_query)
# export BI Answers report to Pandas DataFrame
data = OTBI.exportAnswersReportPandas(reportPath='/shared/Custom/OTBI_TESTING_HS/SALES_REPORT')
data.head()
```
