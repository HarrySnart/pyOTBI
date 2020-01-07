# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:38:26 2020

@author: hsnart
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64
import io
import xmltodict
import re

''' pyOTBI - Unofficial Python library for connecting to Oracle Cloud Fusion Applications Oracle Transactional Business Intelligence

This library is writen by Harry Snart 

It is not best practice to enter your password in plain text, please look at projects such as Keyring for more secure options

'''

class connect:
    def __init__(self,host,user,password):
        ''' class initialisation, allows you to set OTBI connection details'''
        self.host = host
        self.user = user
        self.password = password
        
        
    def logon(self,host,user,password):
        ''' This function is used in the background by pyOTBI to get WSDL Session IDs. For simplicity, we generate a new session ID with each WSDL call'''
        host=self.host
        user=self.user
        password=self.password
        host = host+'/analytics-ws/saw.dll?SoapImpl=nQSessionService'
        body = '''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v7="urn://oracle.bi.webservices/v12">
           <soapenv:Header/>
           <soapenv:Body>
              <v7:logon>
                 <v7:name>'''+ str(user) + '''</v7:name>
                 <v7:password>'''+ str(password) + '''</v7:password>
              </v7:logon>
           </soapenv:Body>
        </soapenv:Envelope>
        '''
        headers = {'content-type': 'text/xml; charset=UTF-8'}
        
        response = requests.post(host,data=body,headers=headers)
        
        soup = BeautifulSoup(response.content,'xml')
        
        sessionid = str(soup.text).strip()
            
        return(sessionid)

    def getCurlUser(self):
        ''' Use this to confirm which user you are logged in as '''
        host=self.host
        user=self.user
        password=self.password
        sessionid = connect.logon(self,host=host,user=user,password=password)
        host = host+'/analytics-ws/saw.dll?SoapImpl=nQSessionService'
        body = '''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v12="urn://oracle.bi.webservices/v12">
           <soapenv:Header/>
           <soapenv:Body>
              <v12:getCurUser>
                 <v12:sessionID>'''+str(sessionid)+'''</v12:sessionID>
              </v12:getCurUser>
           </soapenv:Body>
        </soapenv:Envelope>
        '''
        #need to test if anything is returned
        headers = {'content-type': 'text/xml; charset=UTF-8'}
        
        response = requests.post(host,data=body,headers=headers)
        
        soup = BeautifulSoup(response.content,'xml')
        
        curluser = str(soup.text).strip()
        #message = 'success'
        return(curluser)
        
    def exportAnswersReportPandas(self,reportPath):
        '''Use this function to run a BI Answers report and export the data directly into a Pandas DataFrame.'''
        host=self.host
        user=self.user
        password=self.password
        sessionid = connect.logon(self,host=host,user=user,password=password)
        
        host = host+'/analytics-ws/saw.dll?SoapImpl=analysisExportViewsService'
        body = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v10="urn://oracle.bi.webservices/v10">
           <soapenv:Header/>
           <soapenv:Body>
              <v10:initiateAnalysisExport>
                 <v10:report>
                    <v10:reportPath>'''+reportPath+'''</v10:reportPath>
                    <v10:reportXml></v10:reportXml>
                 </v10:report>
                 <v10:outputFormat>csv</v10:outputFormat>
                 <v10:executionOptions>
                    <v10:async></v10:async>
                    <v10:useMtom></v10:useMtom>
                    <v10:refresh></v10:refresh>
                 </v10:executionOptions>
                 <v10:reportParams>
                    <!--Zero or more repetitions:-->
                    <v10:filterExpressions></v10:filterExpressions>
                    <!--Zero or more repetitions:-->
                    <v10:variables>
                       <v10:name></v10:name>
                       <v10:value></v10:value>
                    </v10:variables>
                    <!--Zero or more repetitions:-->
                    <v10:nameValues>
                       <v10:name></v10:name>
                       <v10:value></v10:value>
                    </v10:nameValues>
                    <!--Zero or more repetitions:-->
                    <v10:templateInfos>
                       <v10:templateForEach></v10:templateForEach>
                       <v10:templateIterator></v10:templateIterator>
                       <!--Zero or more repetitions:-->
                       <v10:instance>
                          <v10:instanceName></v10:instanceName>
                          <!--Zero or more repetitions:-->
                          <v10:nameValues>
                             <v10:name></v10:name>
                             <v10:value></v10:value>
                          </v10:nameValues>
                       </v10:instance>
                    </v10:templateInfos>
                    <!--Optional:-->
                    <v10:viewName></v10:viewName>
                 </v10:reportParams>
                 <v10:reportViewName></v10:reportViewName>
                 <v10:sessionID>'''+sessionid+'''</v10:sessionID>
              </v10:initiateAnalysisExport>
           </soapenv:Body>
        </soapenv:Envelope>'''
    
        headers = {'content-type': 'text/xml; charset=UTF-8'}
                
        response = requests.post(host,data=body,headers=headers)
    
        soup = BeautifulSoup(response.content,'xml')
        
        dataset = str(soup.text).strip()[:-8]
        decoded_dataset = base64.b64decode(dataset)
        bytes_dataset = io.BytesIO(decoded_dataset)
        df = pd.read_csv(bytes_dataset)
        return(df)

    def listSubjectAreas(self):
        ''' Documents the list of Subject Areas available to your user as a Pandas dataframe complete with descriptions. '''
        host=self.host
        user=self.user
        password=self.password
        sessionid = connect.logon(self,host=host,user=user,password=password)
        host = host+'/analytics-ws/saw.dll?SoapImpl=metadataService'
        body = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v10="urn://oracle.bi.webservices/v10">
   <soapenv:Header/>
   <soapenv:Body>
      <v10:getSubjectAreas>
         <v10:sessionID>'''+sessionid+'''</v10:sessionID>
      </v10:getSubjectAreas>
   </soapenv:Body>
</soapenv:Envelope>'''
        #need to test if anything is returned
        headers = {'content-type': 'text/xml; charset=UTF-8'}
        
        response = requests.post(host,data=body,headers=headers)
        
        SOAPdict = xmltodict.parse(response.text)

        name = []
        displayName = []
        description = []
        
        for i in range(len(SOAPdict['soap:Envelope']['soap:Body']['sawsoap:getSubjectAreasResult']['sawsoap:subjectArea'])):
            name.append(SOAPdict['soap:Envelope']['soap:Body']['sawsoap:getSubjectAreasResult']['sawsoap:subjectArea'][i]['sawsoap:name'])
            displayName.append(SOAPdict['soap:Envelope']['soap:Body']['sawsoap:getSubjectAreasResult']['sawsoap:subjectArea'][i]['sawsoap:displayName'])
            description.append(SOAPdict['soap:Envelope']['soap:Body']['sawsoap:getSubjectAreasResult']['sawsoap:subjectArea'][i]['sawsoap:description'])
            
        SAdf = pd.DataFrame({'Name':name,'Display_Name':displayName,'Description':description})
        
        return(SAdf)

    def searchUser(self,userAccount):
        ''' Use this to confirm which user you are logged in as '''
        host=self.host
        user=self.user
        password=self.password
        sessionid = connect.logon(self,host=host,user=user,password=password)
        host = host+'/analytics-ws/saw.dll?SoapImpl=securityService'
        body = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v10="urn://oracle.bi.webservices/v10">
   <soapenv:Header/>
   <soapenv:Body>
      <v10:getAccounts>
         <!--1 or more repetitions:-->
         <v10:account>
            <!--Optional:-->
            <v10:name>'''+userAccount+'''</v10:name>
            <v10:accountType></v10:accountType>
            <!--Optional:-->
            <v10:guid></v10:guid>
            <!--Optional:-->
            <v10:displayName></v10:displayName>
         </v10:account>
         <v10:sessionID>'''+sessionid+'''</v10:sessionID>
      </v10:getAccounts>
   </soapenv:Body>
</soapenv:Envelope>'''
        #need to test if anything is returned
        headers = {'content-type': 'text/xml; charset=UTF-8'}
        
        response = requests.post(host,data=body,headers=headers)
        
        data = xmltodict.parse(response.text)
        user_details = {'name':data['soap:Envelope']['soap:Body']['sawsoap:getAccountsResult']['sawsoap:accountDetails']['sawsoap:name'],
      'accountType':data['soap:Envelope']['soap:Body']['sawsoap:getAccountsResult']['sawsoap:accountDetails']['sawsoap:accountType'],
      'guid':data['soap:Envelope']['soap:Body']['sawsoap:getAccountsResult']['sawsoap:accountDetails']['sawsoap:guid'],
      'displayName':data['soap:Envelope']['soap:Body']['sawsoap:getAccountsResult']['sawsoap:accountDetails']['sawsoap:displayName']
      }
        #message = 'success'
        return(user_details)




    def exportXMLtoPandas(self, xml):
        ''' This function sends an XML query to the BI servre and returns the data as a pandas dataframe'''
        host=self.host
        user=self.user
        password=self.password
        sessionid = connect.logon(self,host=host,user=user,password=password)
        
        url = host+"/analytics-ws/saw.dll?SoapImpl=xmlViewService"
        headers = {'content-type': 'text/xml'}
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v7="urn://oracle.bi.webservices/v7">
           <soapenv:Header/>
           <soapenv:Body>
              <v7:executeXMLQuery>
                 <v7:report>
                    <v7:reportPath></v7:reportPath>
                    <v7:reportXml>"""+str(xml)+"""</v7:reportXml>
                 </v7:report>
                 <v7:outputFormat></v7:outputFormat>
                 <v7:executionOptions>
                    <v7:async></v7:async>
                    <v7:maxRowsPerPage>?</v7:maxRowsPerPage>
                    <v7:refresh></v7:refresh>
                    <v7:presentationInfo></v7:presentationInfo>
                    <v7:type></v7:type>
                 </v7:executionOptions>
                 <v7:reportParams>
                    <!--Zero or more repetitions:-->
                    <v7:filterExpressions></v7:filterExpressions>
                    <!--Zero or more repetitions:-->
                    <v7:variables>
                       <v7:name></v7:name>
                       <v7:value></v7:value>
                    </v7:variables>
                    <!--Zero or more repetitions:-->
                    <v7:nameValues>
                       <v7:name></v7:name>
                       <v7:value></v7:value>
                    </v7:nameValues>
                    <!--Zero or more repetitions:-->
                    <v7:templateInfos>
                       <v7:templateForEach></v7:templateForEach>
                       <v7:templateIterator></v7:templateIterator>
                       <!--Zero or more repetitions:-->
                       <v7:instance>
                          <v7:instanceName></v7:instanceName>
                          <!--Zero or more repetitions:-->
                          <v7:nameValues>
                             <v7:name></v7:name>
                             <v7:value></v7:value>
                          </v7:nameValues>
                       </v7:instance>
                    </v7:templateInfos>
                    <!--Optional:-->
                    <v7:viewName></v7:viewName>
                 </v7:reportParams>
                 <v7:sessionID>""" + str(sessionid) + """</v7:sessionID>
              </v7:executeXMLQuery>
           </soapenv:Body>
        </soapenv:Envelope>"""

        response = requests.post(url,data=body,headers=headers)

        soup = BeautifulSoup(response.content,'xml')

        x = str(soup.text)

        y=re.findall("Column.",x)

        dist_cols = []
        for i in y:
            if i not in dist_cols:
                dist_cols.append(i)
            
        g = globals()
        for i in range(len(dist_cols)):
            g['Column{0}'.format(i)] = []

        for i in dist_cols:
            g['{0}'.format(i)].append(re.findall("<"+i+">(.*?)</"+i+">",x))
            
        for i in range(len(dist_cols)):
            g['Column{0}_df'.format(i)] = list(itertools.chain(*g['Column{0}'.format(i)]))


        df=pd.DataFrame()


        for i in range(len(dist_cols)):
            df['Column{0}_df'.format(i)] = g['Column{0}_df'.format(i)]
            
        return(df)


    def logicalSQLtoPandas(self,sql):
        ''' Use this function to run a logical SQL query against the BI Server, returning the results as a Pandas dataframe '''
        host=self.host
        user=self.user
        password=self.password
        sessionid = connect.logon(self,host=host,user=user,password=password)
        host = host+'/analytics-ws/saw.dll?SoapImpl=xmlViewService'
        body = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v10="urn://oracle.bi.webservices/v10">
   <soapenv:Header/>
   <soapenv:Body>
      <v10:executeSQLQuery>
         <v10:sql>'''+sql+'''
</v10:sql>
         <v10:outputFormat>text/csv</v10:outputFormat>
         <v10:executionOptions>
            <v10:async></v10:async>
            <v10:maxRowsPerPage></v10:maxRowsPerPage>
            <v10:refresh></v10:refresh>
            <v10:presentationInfo></v10:presentationInfo>
            <v10:type></v10:type>
         </v10:executionOptions>
         <v10:sessionID>'''+sessionid+'''</v10:sessionID>
      </v10:executeSQLQuery>
   </soapenv:Body>
</soapenv:Envelope>'''
        #need to test if anything is returned
        headers = {'content-type': 'text/xml; charset=UTF-8'}
        
        response = requests.post(host,data=body,headers=headers)
        
        SQL = xmltodict.parse(response.text)
        
        rowset = SQL['soap:Envelope']['soap:Body']['sawsoap:executeSQLQueryResult']['sawsoap:return']['sawsoap:rowset']

        data = xmltodict.parse(rowset)
        SQLdf = pd.DataFrame(data['rowset']['Row'], columns=data['rowset']['Row'][0].keys())

        return(SQLdf)


