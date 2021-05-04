import snap7   # Siemens S7-1200 profinet ile haberleşmede kullanacağımız kütüphane 
import ctypes  #C'deki veri tiplerini kullanmamız için gerekli kütüphane
from ctypes import #C'deki tüm veri tiplerini dahil ediyorum bunu install etmeme gerek
# yok çünkü pure python yani doğrudan pythonun içerisinde gelmekte


#Read fonksyonunda okunacak değerinin c türüne dönüşümünde kullanılacak dictionary
enumTypesMyDB = {
     "boolean" : 'c_bool',
     "int" : 'c_int',
     "real" : 'c_long'   
}

enumSizeMyDB = {  # C türlerinin byte olarak boyutları 
     'c_bool' : 1,
      'c_int' : 4,
      'c_long': 8   
}


class DB_Abstraction(): #DataBlockun high level seviyedeki abstarctionu yapıyorum farklı datablockları için yararlı olacaktır

    def __init__(self , *args):  #args alma sebebim ileride daha fazla parametreyle oluşturulup geliştirilebilir olması
        if len(len(args) >0):
            try:
                self.DB_Number = args[0]
            except:
                print("DB Number must be integer or 0-65536") #Db block sayı aralığında olması lazım ya da int olması lazım
        else:
            print("DB block default created 1999") #Eğer block numarası girilmezse bir block numarası default olarak atıyorum
            #Daha sonra burada otomatik bir datablock yaratma kodu yazabilirim şimdilik boş bırakıyorum
        

    def showBlockInfo(self):
        return client.get_block_info("DB", self.DB_Number) #Db hakkında genel bilgi

    def readData(self , dataType , startIndex):

        cType = enumTypesMyDB[dataType]  # Dictionarye göre c türündeki değişken tipi otomatik ayarlanıyor
        if cType is not None:   #Eğer hatalı bir değer girdiyse none olacaktır
            data = (cType * size_to_read)()     # Cdeki tipinden bir obje oluşturuyorum
            result = client.as_db_read(self.DB_Number, startIndex, enumSizeMyDB[cType], data) #db_number , start , size , data # result  # 0 = success result değeri 0 ise okuma başarılıdır.
            return data #Okunan datanın geri döndürülmesi
        else:
            "Print Type not match"
            return None

    def writeData(self,dataType , startIndex,Idata): #Read işleminin bir benzeri yapılmakta fark olarak yazılacak datanın C türündeki dönüşümünün yapılması
        cType = enumTypesMyDB[dataType]
        if cType is not None:
            data = None
            if cType =="c_bool":
                data = c_bool(Idata)
            elif cType == "c_int":
                data = c_int(Idata)
            elif cType == "c_long":
                data = c_long(Idata)
            as_db_write(self.DB_Number, startIndex, enumSizeMyDB[cType], data)
            return "Writing is successfully"
        else:
            print("Something went wrong !")
            return "Error writing "
    def showAllDB(self):
        return client.list_blocks()  #Tüm blockları ve adreslerin gösterilmesi


client = snap7.client.Client() #Client tarafı olduğumuz için client olarak bir obje yaratıyorum
client.connect("192.168.2.100", 0, 0) # 2. ve 3. parametreler local_tsap  , remote_tsap bu clientin paramterlerini set etme istersek
# client = snap7.client.Client("192.168.2.100") şeklinde de yapabiliriz fakat tsaplerin ayarlanması için bu daha kullanışlı



connectionStatus = client.get_connected() #true or false Bağlantımızın sağlanığ sağlanmadığını kontrol ediyoruz.

if connectionStatus:
    print("Connection is successfully ") # Bağlantı durumu başarılı veri almanın 2 yolu var fakat ben c_type türünde kullanmak istediğim için 1. yöntemi kullanacağım
    myDataBlock = DB_Abstraction(555) #555 Numaralı dataBlocku abstract şekilde tanımladık
    print(myDataBlock.read("boolean" , 0))
    print(myDataBlock.read("int" , 8))
    print(myDataBlock.read("real" , 40))
    print(myDataBlock.write("int",8,123456)

else:
    print("Check tsaps and Plc's IP")


"""

REFERENCES : 
    https://docs.python.org/3/library/ctypes.html
    https://python-snap7.readthedocs.io/en/1.0/client.html
    https://python-snap7.readthedocs.io/en/latest/introduction.html
    http://simplyautomationized.blogspot.com/2014/12/raspberry-pi-getting-data-from-s7-1200.html?m=1
    
"""

"""

Some Documantation References

data = (ctypes.c_uint8 * size_to_read)() 
result = client.as_db_read(1, 0, size_to_read, data) #db_number , start , size , data
# result  # 0 = success result değeri 0 ise okuma başarılıdır.



import snap7
>>> client = snap7.client.Client()
>>> client.connect("192.168.0.1", 0, 0)
>>> buffer = client.db_read(1, 10, 4)  # reads the db number 1 starting from the byte 10 until byte 14.
>>> buffer
bytearray(b'\x00\x00')


>>> block_info = client.get_block_info("DB", 1)
>>> print(block_info)
Block type: 10
Block number: 1
Block language: 5
Block flags: 1
MC7Size: 100
Load memory size: 192
Local data: 0
SBB Length: 20
Checksum: 0
Version: 1
Code date: b'1999/11/17'
Interface date: b'1999/11/17'
Author: b''
Family: b''
Header: b''

>>> block_list = client.list_blocks()
>>> print(block_list)
<block list count OB: 0 FB: 0 FC: 0 SFB: 0 SFC: 0x0 DB: 1 SDB: 0>

>>> import snap7
>>> client = snap7.client.Client()
>>> client.connect("192.168.0.1", 0, 0)
>>> buffer = client.read_area(snap7.types.Areas.DB, 1, 10, 4)  # Reads the DB number 1 from the byte 10 to the byte 14.
>>> buffer
bytearray(b'\x00\x00')


""""