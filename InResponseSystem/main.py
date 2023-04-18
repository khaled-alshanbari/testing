# from attr import s 
import streamlit as st

st.set_page_config(
    page_title="In-Response",
    page_icon="ð¥️",
    layout="wide",
    initial_sidebar_state="expanded",
)  
import utils.authenticate as stauth
import DBconn as sqlcon
import pandas as pd
import hashlib  
#import win32com.client
#import pythoncom
import numpy as np
#from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import re
#from dill import dumps, loads
#import tkinter as tk
#import tkinter.messagebox as messagebox
import multiprocessing as mp
import time

st.markdown(
    """<style>
        .element-container:nth-of-type(3) button {
            height: 3em;
        }
        </style>""",
    unsafe_allow_html=True,
)

loaded=pickle.load(open("model.sav", "rb"))
loaded2=pickle.load(open("tfidf.sav", "rb"))

def click(x,counter):
                c = sqlcon.create_conn()
                cursor7 = c.cursor()
                cursor7.execute('UPDATE tickets SET v'+str(counter-1)+' = 1 WHERE ticketid = '+str(x)+';')
                c.commit()  
#def display_alert():
    # Show the alert message
    #messagebox.showwarning("In-Response", "New Incident Detected!", Parent=None)

def run_alert():

    # Display the alert message
    #display_alert()
    pass


def cleanEmails(emails):
    emails = re.sub('http\S+\s*', ' ', emails)  # remove URLs
    emails = re.sub('RT|cc', ' ', emails)  # remove RT and cc
    emails = re.sub('#\S+', '', emails)  # remove hashtags
    emails = re.sub('@\S+', '  ', emails)  # remove mentions
    emails = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', emails)  # remove punctuations
    emails = re.sub(r'[^\x00-\x7f]',r' ', emails) #replace consecutive non-ASCII characters with a space
    emails = re.sub('\s+', ' ', emails)  # remove extra whitespace
    emails = ''.join([word for word in emails if not word.isdigit()]) #remove any numeric characters
    emails = emails.lower() #convert text to lowercase
    emails=re.sub(" caution this message is originated outside of iau domain please use caution when opening attachments clicking links or responding to requests for information", '', emails)
    return emails

class Handler_Class(object):
    def OnNewMailEx(self, receivedItemsIDs):
        try:
            for ID in receivedItemsIDs.split(","):
                mail = outlook.Session.GetItemFromID(ID)
                a=cleanEmails(mail.Body)
                x = np.array([a])
                prediction = loaded.predict(loaded2.transform(x).reshape(1, -1))
                print(prediction)
                if prediction == [1]:
                    alert_process = mp.Process(target=run_alert)
                    alert_process.start()

        
                    c = sqlcon.create_conn()
                    if c.is_connected():
                      
                      sqlQ = "INSERT INTO `tickets`(`classid`,`Flag`,`start_time`,`end_time` ) VALUES (%s,%s,%s)" 
                      values = ("1","1", "1", "3")
                      cursor = c.cursor()
                      cursor.execute(sqlQ, values)
                      c.commit()
                    c.close()

                if prediction == [2]:
                    alert_process = mp.Process(target=run_alert)
                    alert_process.start()

        
                    c = sqlcon.create_conn()
                    if c.is_connected():
                      
                      sqlQ = "INSERT INTO `tickets`(`classid`,`Flag`,`start_time`,`end_time` ) VALUES (%s,%s,%s)" 
                      values = ("2","1", "1", "3")
                      cursor = c.cursor()
                      cursor.execute(sqlQ, values)
                      c.commit()
                    c.close()

                if prediction == [3]:
                    alert_process = mp.Process(target=run_alert)
                    alert_process.start()

        
                    c = sqlcon.create_conn()
                    if c.is_connected():
                      
                      sqlQ = "INSERT INTO `tickets`(`classid`,`Flag`,`start_time`,`end_time` ) VALUES (%s,%s,%s)" 
                      values = ("3","1", "1", "3")
                      cursor = c.cursor()
                      cursor.execute(sqlQ, values)
                      c.commit() 
                    c.close()
        except Exception as e:
            print("Error: ", e)              

                  


                
        
global c

def main():
    c= sqlcon.create_conn()
    sqlcon.call_users(c)
    usernames = sqlcon.usernames
    names = sqlcon.names
    passwords = sqlcon.passwords
    hashed_passwords = stauth.Hasher(passwords).generate()
    c.close()


    credentials = {"usernames":{}}


    for un, name, pw in zip(usernames, names, hashed_passwords):
        user_dict = {"name":name,"password":pw}
        credentials["usernames"].update({un:user_dict})
        

    _authenticator = stauth.Authenticate(credentials,'in_responseCookie', 
                                        'auth',cookie_expiry_days=0)
    
    
    def render_tickets_page(x):
       
        with st.form('form'):
             
             c = sqlcon.create_conn()
             cursor2 = c.cursor()
             cursor2.execute('SELECT ticketId,classification_type,v1,v2,v3,v4,v5,v6 FROM tickets,classification WHERE classid=classification_id AND flag = 1 LIMIT 1 OFFSET ' + str(x) + ';')
             
             fetchtickets = cursor2.fetchall()[0]
             print(fetchtickets)
             Ticket_Number='<p style="font-family:Courier; color:#1657F5; font-size: 20px;">Ticket Number: </p>'
             st.markdown(Ticket_Number, unsafe_allow_html=True)
             Ticket_Number2='<p style="font-family:Courier; color:#2F3031 ; font-size: 20px;">#'+str(fetchtickets[0])+' </p>'
             st.markdown(Ticket_Number2, unsafe_allow_html=True)

             Incident_Type='<p style="font-family:Courier; color:#1657F5; font-size: 20px;">Incident Type: </p>'
             st.markdown(Incident_Type, unsafe_allow_html=True)
             Incident_Type2='<p style="font-family:Courier; color:#2F3031 ; font-size: 20px;">'+str(fetchtickets[0])+' </p>'
             st.markdown(Incident_Type2, unsafe_allow_html=True)

            #PHISHING
             if str(fetchtickets[1]) == "phishing":
              process='<p style="font-family:Courier; color:#1657F5; font-size: 20px;">Incident Responce process: </p>'
              st.markdown(process, unsafe_allow_html=True)
              cursor3 = c.cursor()
              cursor3.execute('SELECT process_text FROM process WHERE process.classification_id=1 ;')
              fetchpro = cursor3.fetchall()
              c.commit() 
              cursor22 = c.cursor()
              cursor22.execute('SELECT COUNT(process_text) FROM process WHERE process.classification_id=1;')
              E=cursor22.fetchone()[0]
              c.commit() 
              counter=2
              for x in range(E):
               Incident_proc='<p style="font-family:Courier; color:#2F3031 ; font-size: 20px;">'+str(fetchpro[x])+' </p>'
               if fetchtickets[counter] == 1:
                    st.checkbox(str(fetchpro[x]),value=True)
               else :
                    st.checkbox(str(fetchpro[x]),value=False,on_change=click(fetchtickets[0],counter )) 
                     
               counter=counter+1  
               cursor33 = c.cursor()
               c.commit() 
               cursor33.execute('SELECT sub_process_text FROM subprocess WHERE process_id= ' + str(x+1) + ' ;')
               fetchsubpro = cursor33.fetchall()
               Incident_subproc='<p style="font-family:Courier; color:#2F3031 ; font-size: 10px;">'+str(fetchsubpro[0])+' </p>'
               st.markdown(Incident_subproc, unsafe_allow_html=True)

             #DDOS
             if str(fetchtickets[1]) == "ddos":
              process='<p style="font-family:Courier; color:#1657F5; font-size: 20px;">Incident Responce process: </p>'
              st.markdown(process, unsafe_allow_html=True)
              cursor3 = c.cursor()
              cursor3.execute('SELECT process_text FROM process WHERE process.classification_id=2 ;')
              fetchpro = cursor3.fetchall()
              c.commit() 
              cursor22 = c.cursor()
              cursor22.execute('SELECT COUNT(process_text) FROM process WHERE process.classification_id=2;')
              E=cursor22.fetchone()[0]
              c.commit() 
              counter=2
              for x in range(E):
               Incident_proc='<p style="font-family:Courier; color:#2F3031 ; font-size: 20px;">'+str(fetchpro[x])+' </p>'
               if fetchtickets[counter] == 1:
                    st.checkbox(str(fetchpro[x]),value=True,on_change=click(fetchtickets[0],counter )) 
               else :
                     st.checkbox(str(fetchpro[x]),value=False,on_change=click(fetchtickets[0],counter )) 
               counter=counter+1  
               cursor33 = c.cursor()
               c.commit() 
               counter2=201
               cursor33.execute('SELECT sub_process_text FROM subprocess WHERE process_id= ' + str(counter2+1) + ' ;')
               fetchsubpro = cursor33.fetchall()
               Incident_subproc='<p style="font-family:Courier; color:#2F3031 ; font-size: 10px;">'+str(fetchsubpro[0])+' </p>'
               st.markdown(Incident_subproc, unsafe_allow_html=True)
               counter2=counter2+1

             #data_leakage
             if str(fetchtickets[1]) == "data_leakage":
              process='<p style="font-family:Courier; color:#1657F5; font-size: 20px;">Incident Responce process: </p>'
              st.markdown(process, unsafe_allow_html=True)
              cursor3 = c.cursor()
              cursor3.execute('SELECT process_text FROM process WHERE process.classification_id=3 ;')
              fetchpro = cursor3.fetchall()
              c.commit() 
              cursor22 = c.cursor()
              cursor22.execute('SELECT COUNT(process_text) FROM process WHERE process.classification_id=3;')
              E=cursor22.fetchone()[0]
              c.commit() 
              counter=2
              for x in range(E):
        
               Incident_proc='<p style="font-family:Courier; color:#2F3031 ; font-size: 20px;">'+str(fetchpro[x])+' </p>'
               if fetchtickets[counter] == 1:
                    st.checkbox(str(fetchpro[x]),value=True)
               else :
                     st.checkbox(str(fetchpro[x]),value=False,on_change=click(str(fetchtickets[0]),counter )) 
               counter=counter+1  
               cursor33 = c.cursor()
               c.commit() 
               counter2=301
               cursor33.execute('SELECT sub_process_text FROM subprocess WHERE process_id= ' + str(counter2+1) + ' ;')
               fetchsubpro = cursor33.fetchall()
               Incident_subproc='<p style="font-family:Courier; color:#2F3031 ; font-size: 10px;">'+str(fetchsubpro[0])+' </p>'
               st.markdown(Incident_subproc, unsafe_allow_html=True)
               counter2=counter2+1 


             if st.form_submit_button('Close The Ticket'):
                 cursor7 = c.cursor()
                 cursor7.execute('UPDATE tickets SET end_time = '+datetime.now()+' AND flag = 2 WHERE ticketid = '+str(x)+';')
                 c.commit()
                 st.success(f"Ticket #{Ticket_Number} Closed")
        c.close()



            #  if st.form_submit_button('submit'):
            #     st.success('updated successfully')
                      

    def render_admin_page():
        
        st.subheader('Welcome *%s*' % (name))
        adminMenu = st.selectbox("Admin Menu", ["Opened Tickets", "Closed Tickets","Users Profiles","Add User"])
        #st.sidebar.button("Logout", key="1")
         
     
        if adminMenu == "Opened Tickets":
            st.subheader("Browse Open Tickets")
            c = sqlcon.create_conn()
            if c.is_connected():
             cursor = c.cursor()
             cursor.execute('SELECT COUNT(ticketId), ticketId  FROM tickets WHERE flag = 1;')
             E=cursor.fetchone()[0]
             cursor2 = c.cursor()
             cursor2.execute('SELECT ticketId,classification_type FROM tickets,classification WHERE classid=classification_id AND flag = 1  ;')
             fetchtickets = cursor2.fetchall()
             for x in range(E):

              if st.button("Ticket: "+str(x)) :
                 render_tickets_page(x)
            #  sqlcon.create_conn.cursor.close()
             c.close() 
                   
                    
        
            


        elif adminMenu == "Closed Tickets":
            st.subheader("Browse Closed Tickets")
            c = sqlcon.create_conn()
            if c.is_connected():
              cursor = c.cursor()
              cursor.execute('SELECT COUNT(ticketId) FROM tickets WHERE flag = 2;')
              E=cursor.fetchone()[0]
              for x in range(E):
                  st.button("ticket"+str(x), key=x)
              c.close()
        elif adminMenu == "Users Profiles":
            st.subheader("Profiles:")
            fetchUsers = []
            c = sqlcon.create_conn()
            if c.is_connected():
                cursor = c.cursor()
                cursor.execute('SELECT id, username , name, email FROM users;')
                fetchUsers = cursor.fetchall()
                c.close()
            # Displaying data using Streamlit table
            df = pd.DataFrame(fetchUsers,columns=('ID','Username','Name','Email'))
            # CSS to inject contained in a string
            hide_table_row_index = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            # Display a static table
            st.table(df)

        elif adminMenu == "Add User":  
            st.subheader("Add New User")

            # Create input fields for the user's name, email, and password
            new_username = st.text_input("Username")
            new_name = st.text_input("Name")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            
 

            # Add a button to submit the new user
            if st.button("Add User"):
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                c = sqlcon.create_conn()
                if c.is_connected():
                    cursor = c.cursor()
                    sqlQ = "INSERT INTO `users`(`username`, `password`, `name`, `email`) VALUES (%s,%s,%s,%s)" 
                    values = (new_username, hashed_password, new_name, new_email)

                    cursor.execute(sqlQ, values)
                    c.commit()
                    c.close()
                # Show a success message
                st.success(f"Added user: {new_name} ({new_email}) with username: {new_username}")



    def render_regular_page():    
        st.subheader('Welcome *%s*' % (name))
        regMenu = st.selectbox("Menu", ["Home", "Opened Tickets", "Closed Tickets"])

        if regMenu == "Opened Tickets":
            st.subheader("Browse Open Tickets")
            c = sqlcon.create_conn()
            if c.is_connected():
             cursor = c.cursor()
             cursor.execute('SELECT COUNT(ticketId) FROM tickets WHERE flag = 1;')
             E=cursor.fetchone()[0]
             for x in range(E):
                 st.button("ticket"+str(x), key=x)
             c.close()
        
            


        elif regMenu == "Closed Tickets":
            st.subheader("Browse Closed Tickets")
            c = sqlcon.create_conn()
            if c.is_connected():
             cursor = c.cursor()
             cursor.execute('SELECT COUNT(ticketId) FROM tickets WHERE flag = 2;')
             E=cursor.fetchone()[0]
             for x in range(E):
                 st.button("ticket"+str(x), key=x)
             c.close()

    name, authentication_status, username = _authenticator.login('Login','main')

    adminusername='admin'
    
    if authentication_status:
            if username == adminusername:
                render_admin_page()
                _authenticator.logout("logout","main")
                
                
                
                
                
            elif username != adminusername:
                render_regular_page()
                _authenticator.logout("logout","main")

    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')


if __name__ == '__main__':  

    #pythoncom.CoInitialize()
    main()
    
    #outlook = win32com.client.DispatchWithEvents("Outlook.Application", Handler_Class)
    #pythoncom.PumpMessages()       
