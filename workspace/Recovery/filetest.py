import pickle as pk
from user import User

userFile = open('..//Datas//userlist.bin', mode = 'rb')
userlist = pk.load(file = userFile)
userFile.close()

user = userlist[0]
print(user.getName())
print(user.getAge())
print(user.getGender())