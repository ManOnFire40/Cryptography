import socket

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 4242

userName=input('please enter the userName:')
password=input('please enter the password:')
message_type=input('please enter the message type ,you have 2 message type login or signUp:')
message=''
if(message_type=='login' or message_type=='signUp'):
    message='{'+message_type+','+userName+','+password+'}'    
else:    
    print('undefined message type')
    exit()#break before esatblishing the connection 

with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        while(True):            
            server_address = (SERVER_IP, SERVER_PORT)    
            s.connect((SERVER_IP, 4242))
            arr = bytes(message, 'utf-8')
            s.send(arr)
            res=s.recv(1024)
            r=res.decode('utf-8')
            res_str=str(r)
            print(res_str)
            break

