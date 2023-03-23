
def get_index_in_plain(character):
  plain_text='abcdefghijklmnopqrstuvwxyz'
  index=-1
  for i in range(len(plain_text)):
    if(character==plain_text[i]):
      index=i
  return  index



def cesar_encrypt(key, message):
  plain_text='abcdefghijklmnopqrstuvwxyz'
  enc_mesage=""
  for i in range(len(message)):
     index=get_index_in_plain(message[i])
     if(index==-1):
      enc_mesage+= message[i] 
     else:
      enc_mesage+=plain_text[index+key%26]
  return enc_mesage 

  
def cesar_decrypt(key, message):
  plain_text='abcdefghijklmnopqrstuvwxyz'
  enc_mesage=""
  for i in range(len(message)):
     index=get_index_in_plain(message[i])
     if(index==-1):
      enc_mesage+= message[i] 
     else:
      enc_mesage+=plain_text[index-key%26]
  return enc_mesage 


m=cesar_encrypt(7,'mohamed ehab osman')
print(m)
print(cesar_decrypt(7,m))
  
  