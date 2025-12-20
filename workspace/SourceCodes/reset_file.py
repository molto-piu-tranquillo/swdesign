# 파일 초기화

import pickle as pk
from user import *
from data_paths import USERLIST_PATH

userlist: list[User] = []

userlistFile = open(USERLIST_PATH, mode = 'wb')
pk.dump(file = userlistFile, obj = userlist)
userlistFile.close()

print('파일 초기화가 완료되었습니다.')