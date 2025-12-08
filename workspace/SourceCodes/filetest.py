import pickle as pk
from user import *

userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
userlist: list[User] = pk.load(file = userlistFile)
userlistFile.close()

doctor = Doctor('김의사', 40, '남', 'doc123', 'doc123@', '010-1234-5678',\
        'uk3181@naver.com', '주치의')
doctor.addPatientById('uk3181')
userlist.append(doctor)

userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
pk.dump(file = userlistFile, obj = userlist)
userlistFile.close()