DEBUG_FOR_CONNECTION = False
DEBUG_FOR_ADDING_DATA = False

import pickle as pk
from user import *
from data_paths import USERLIST_PATH

userlist: list[User] = []

patient = Patient('정재욱', 22, '남', 'uk3181', 'uk3181@', '010-9494-5836',\
        'uk3181@daum.net', '개인 사용자')
parent = Parent('김부모', 50, '남', 'parent123', 'parent123@', '010-1111-2222',\
        'uk3181@knu.ac.kr', '보호자')
doctor = Doctor('김의사', 40, '남', 'doc123', 'doc123@', '010-1234-5678',\
        'uk3181@naver.com', '주치의')

if DEBUG_FOR_CONNECTION:
    patient.setConnectedParentId(parent.getId()); parent.addPatientById(patient.getId())
    patient.setMainDoctorId(doctor.getId()); doctor.addPatientById(patient.getId())

if DEBUG_FOR_ADDING_DATA:
    patient.addData(Data(2025, 12, 10, [158, 106], 75, True, True, 300, 200, 400, 140))
    patient.addData(Data(2025, 12, 12, [108, 66], 75, False, False, 300, 200, 400, 140))

userlist.append(patient)
userlist.append(parent)
userlist.append(doctor)

userlistFile = open(USERLIST_PATH, mode = 'wb')
pk.dump(file = userlistFile, obj = userlist)
userlistFile.close()

print('파일 설정이 완료되었습니다.')