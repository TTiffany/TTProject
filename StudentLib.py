import requests,json
from cfg import g_vcode
from pprint import pprint
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

class  StudentLib:
    URL = "http://ci.ytesting.com/api/3school/students"

    def __init__(self):
        self.vcode = g_vcode

    def set_vcode(self,vcode):
        self.vcode = vcode


    def list_student(self):

        params = {
                'vcode': self.vcode,
                'action': 'search_with_pagenation'
            }


        response = requests.get(self.URL, params=params)


        bodyDict = response.json()
        pprint (bodyDict,indent=2)

        return bodyDict


    def add_student(self, username, realname, gradeid,
                    classid,phonenumber, idSavedName=None):



        payload = {
            'vcode': self.vcode,
            'action': 'add',
            'username': username,
            'realname': realname,
            'gradeid': gradeid,
            'classid': classid,
            'phonenumber': phonenumber,
        }
        response = requests.post(self.URL, data=payload)


        bodyDict = response.json()
        pprint (bodyDict,indent=2)

        # 需要存储学生ID到全局变量表中

        if idSavedName:
            BuiltIn().set_global_variable('${%s}'%idSavedName,
                                          bodyDict['id'])
            print(f"global var set: ${idSavedName}:{bodyDict['id']}")

        return bodyDict



    def modify_student(self, studentid,realname=None,
                       phonenumber=None):


        payload = {
            'vcode': self.vcode,
            'action': 'modify'
        }
        if realname is not None:
            payload['realname'] = realname

        if phonenumber is not None:
            payload['phonenumber'] = phonenumber


        url = '{}/{}'.format(self.URL, studentid)

        response = requests.put(url, data=payload)

        bodyDict = response.json()
        pprint (bodyDict,indent=2)

        return bodyDict



    def delete_student(self,studentid):

        payload = {
            'vcode'  : self.vcode,
        }

        url = '{}/{}'.format(self.URL,studentid)
        response = requests.delete(url,data=payload)


        bodyDict = response.json()
        pprint (bodyDict,indent=2)

        return bodyDict



    def delete_all_students(self):
        # 列出所有学生
        rd =  self.list_student()
        if rd['retcode'] != 0:
            raise Exception('cannot list student!!')

        # 删除列出的所有学生
        for one in rd['retlist']:
            self.delete_student(one['id'])

        #再列出所有学生
        rd =  self.list_student()

        # 如果没有删除干净，通过异常报错给RF
        if rd['retlist'] != []:
            raise  Exception("cannot delete all student!!")


    def studentlist_should_contain(self,
                                   studentlist,
                                   username,
                                   realname,
                                   studentid,
                                   phonenumber,
                                   classid,
                                   expectedtimes=1):

        item = {
            "username": username,
            "realname": realname,
            "id": int(studentid),
            "phonenumber": phonenumber,
            "classid": int(classid)
        }

        occurTimes = studentlist.count(item)
        logger.info('occur {} times'.format(occurTimes),
                    also_console=True)

        if  occurTimes != int(expectedtimes):
            raise Exception(f'学生列表包含了{occurTimes}次指定信息,期望包含{expectedtimes}!!')



if __name__ == '__main__':
    sl  = StudentLib()
    sl.list_student()



    sl.add_student('lihuo2','藜藿',1,10076,'1234324')


    sl.list_student()