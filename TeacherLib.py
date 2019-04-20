import requests,json
from cfg import g_vcode
from pprint import pprint
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

class  TeacherLib:
    URL = "http://ci.ytesting.com/api/3school/teachers"

    def __init__(self):
        self.vcode = g_vcode

    def set_vcode(self,vcode):
        self.vcode = vcode

    def list_teacher(self, subjectid=None):
        if subjectid != None:
            params = {
                'vcode': self.vcode,
                'action': 'search_with_pagenation',
                'subjectid': int(subjectid)
            }
        else:
            params = {
                'vcode': self.vcode,
                'action': 'search_with_pagenation'
            }

        response = requests.get(self.URL, params=params)


        bodyDict = response.json()
        pprint (bodyDict,indent=2)

        return bodyDict

    def add_teacher(self, username, realname, subjectid, classlist,
                    phonenumber, email, idcardnumber, idSavedName=None):

        # 确保是字符串，而不是整数
        classlist = str(classlist)

        # classlist 是这种格式的字符串 "1,2,3"，需要转换为python列表
        newClassList = [{'id': oneid} for oneid in classlist.split(',') if oneid]

        payload = {
            'vcode': self.vcode,
            'action': 'add',
            'username': username,
            'realname': realname,
            'subjectid': subjectid,
            'classlist': json.dumps(newClassList),
            'phonenumber': phonenumber,
            'email': email,
            'idcardnumber': idcardnumber,
        }
        response = requests.post(self.URL, data=payload)


        bodyDict = response.json()
        pprint (bodyDict,indent=2)

        # 需要存储老师ID到全局变量表中

        if idSavedName:
            BuiltIn().set_global_variable('${%s}'%idSavedName,
                                          bodyDict['id'])
            print(f"global var set: ${idSavedName}:{bodyDict['id']}")

        return bodyDict

    def modify_teacher(self, teacherid,realname=None,
                       subjectid=None,classlist=None,
                       phonenumber=None,email=None,idcardnumber=None):


        payload = {
            'vcode': self.vcode,
            'action': 'modify'
        }
        if realname is not None:
            payload['realname'] = realname
        if subjectid is not None:
            payload['subjectid'] = subjectid
        if phonenumber is not None:
            payload['phonenumber'] = phonenumber
        if email is not None:
            payload['email'] = email
        if idcardnumber is not None:
            payload['idcardnumber'] = idcardnumber
        if classlist is not None:
            # classlist 是这种格式的字符串 "1,2,3"，需要转换为python列表
            classlist = str(classlist)
            newClassList = [{'id': oneid} for oneid in classlist.split(',') if oneid]
            payload['classlist'] = json.dumps(newClassList)

        url = '{}/{}'.format(self.URL, teacherid)

        response = requests.put(url, data=payload)


        bodyDict = response.json()
        pprint (bodyDict,indent=2)

        return bodyDict




    def delete_teacher(self,teacherid):

        payload = {
            'vcode'  : self.vcode,
        }

        url = '{}/{}'.format(self.URL,teacherid)
        response = requests.delete(url,data=payload)


        bodyDict = response.json()
        pprint (bodyDict,indent=2)

        return bodyDict


    def delete_all_teachers(self):
        # 列出所有老师
        rd =  self.list_teacher()
        if rd['retcode'] != 0:
            raise Exception('cannot list teachers!!')

        # 删除列出的所有老师
        for one in rd['retlist']:
            self.delete_teacher(one['id'])

        #再列出所有老师
        rd =  self.list_teacher()

        # 如果没有删除干净，通过异常报错给RF
        if rd['retlist'] != []:
            raise  Exception("cannot delete allteachers!!")

    def teacherlist_should_contain(self,
                                   teacherlist,
                                   username,
                                   realname,
                                   id,
                                   teachclasslist,
                                   phonenumber,
                                   email,
                                   idcardnumber,
                                   expectedtimes=1):

        # 确保是字符串，而不是整数
        teachclasslist = str(teachclasslist)

        item = {
            "username": username,
            "realname": realname,
            "id": int(id),
            "teachclasslist": [int(one) for one in teachclasslist.split(',')],
            "phonenumber": phonenumber,
            "email": email,
            "idcardnumber": idcardnumber
        }

        occurTimes = teacherlist.count(item)
        logger.info('occur {} times'.format(occurTimes),
                    also_console=True)

        if  occurTimes != int(expectedtimes):
            raise Exception(f'老师列表包含了{occurTimes}次指定信息,期望包含{expectedtimes}!!')






if __name__ == '__main__':
    scm = TeacherLib()
    ret = scm.list_teacher()


    ret = scm.add_teacher('helianbobo','赫连勃勃',5,'10076,10077','13000000002',
                          '0002@gmail.com','120789232322')

    # ret = scm.delete_teacher(33)

    # ret = scm.modify_teacher(32,'司马中')
    #
    # ret = scm.list_teacher()

    #
    # scm.delete_all_teacheres()
