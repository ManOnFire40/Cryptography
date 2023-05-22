import socket
import hashlib
import secrets
# you need to run the server then client 
userNames=[]
hashed_password=[]
salts=[]

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 4242

def load_accounts():#
    try:
        with open('accounts.txt', 'r') as fp:
            line = fp.readline()
            while line != '':
                acc=line.split(',')
                userNames.append(acc[0])
                salts.append(acc[1])
                hashed_password.append(acc[2])
                line = fp.readline()                
    except FileNotFoundError:
        print("Please check the path")        


def num_of_lines():
        i=0
    
        with open('accounts.txt', 'r') as fp:
            line = fp.readline()
            while line != '':
                i=i+1
                line = fp.readline()
        return i        


def get_index(element,arr):
    for i in range(len(arr)):
        if(arr[i]==element):
            return i
    return -2    


def split_message(mes):#method to split content of message into array of strings
    arr=mes.split(',')    
    tmp=arr[0]
    message_type=tmp[1:]
    userName=arr[1]
    TMP=arr[2]
    password=TMP[:-1]
    res=[message_type,userName,password]    
    return res



def sign_up(userName,password):#sign Up method
    i=get_index(userName,userNames)
    if(i==-2):
        salt=secrets.token_hex(16)
        salted_password=password+salt
        hashed_salted_password = hashlib.sha512( str( salted_password ).encode("utf-8") ).hexdigest()
        salts.insert(-1,salt)
        userNames.insert(-1,userName)
        hashed_password.insert(-1,hashed_salted_password)
        saved_data=userName+','+salt+','+hashed_salted_password
        fp = open("accounts.txt", 'a')
        fp.write('\n')##########################################
        fp.write(saved_data)##########################################
#f.write("text to write\n")        
        print('data saved succfully')
        fp.close()
        return 'successful sigh up'
    else:
        return 'try another userName' 


def login(userName,password):#login method
    index=get_index(userName,userNames)
    response_message="failed Authentication"
    if(index==-2):
        response_message='failed Authentication'
    else:
        salt=salts[index]
        entered_salted_pass=password+salt
        hashed_entered_salted_pass= hashlib.sha512( str( entered_salted_pass ).encode("utf-8") ).hexdigest()    
        real_pass=hashed_password[index]
        if(real_pass==hashed_entered_salted_pass):
            response_message='successful Authentication'
        else:
            response_message='failed Authentication'    
    return response_message



with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    print('Server is listening')
    s.listen(5)  
    conn,addr = s.accept()
    print(f'Connection accepted from :{addr}')
    load_accounts()
    with conn:
        while(True):
        # conn.send(b'Hello World')
            data =  conn.recv(1024)
            data1=data.decode('utf-8')
            data2=str(data1)
            print(data2)
            if(data2!=''): 
                mes=split_message(data2)#modifications
                respone='unidentified request'
                if(mes[0]== 'login'):
                    print('login')
                    respone=login(mes[1],mes[2])
                if(mes[0]== 'signUp'):
                    print('sign up')                
                    respone=sign_up(mes[1],mes[2])
                arr = bytes(respone, 'utf-8')
                print(arr)
                conn.send(arr)
                break
                
