import requests
from cfg import g_vcode
from pprint import pprint
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

class  SchoolClassLib:
    URL = "http://ci.ytesting.com/api/3school/school_classes"

    def __init__(self):
        self.vcode = g_vcode

    def set_vcode(self,vcode):
        self.vcode = vcode



    def list_school_class(self,gradeid=None):
        if gradeid != None:
            params = {
                'vcode':self.vcode,
                'action':'list_classes_by_schoolgrade',
                'gradeid':int(gradeid)
            }
        else:
            params = {
                'vcode':self.vcode,
                'action':'list_classes_by_schoolgrade'
            }

        response = requests.get(self.URL,params=params)

        bodyDict = response.json()
        pprint (bodyDict,indent=2)
        return bodyDict


    def add_school_class(self,gradeid,name,
                         studentlimit,idSavedName=None):
        payload = {
            'vcode'  : self.vcode,
            'action' : 'add',
            'grade'  : int(gradeid),
            'name'   : name,
            'studentlimit'  : int(studentlimit),
        }
        response = requests.post(self.URL,data=payload)

        bodyDict = response.json()
        pprint (bodyDict,indent=2)
        # logger.debug('添加结果：\n {}'.format(bodyDict))

        if idSavedName:
            print('before')
            BuiltIn().set_global_variable('${%s}'%idSavedName, bodyDict['id'])
            print(f"global var set: ${idSavedName}:{bodyDict['id']}")


        return bodyDict

    def modify_school_class(self, classid, newname, newstudentlimit):
        payload = {
            'vcode': self.vcode,
            'action': 'modify',
            'name': newname,
            'studentlimit': int(newstudentlimit),
        }

        url = '{}/{}'.format(self.URL, classid)

        response = requests.put(url, data=payload)

        bodyDict = response.json()
        pprint(bodyDict, indent=2)

        return bodyDict

    def delete_school_class(self,classid):
        payload = {
            'vcode'  : self.vcode,
        }

        url = '{}/{}'.format(self.URL,classid)
        response = requests.delete(url,data=payload)

        return response.json()



    def delete_all_school_classes(self):
        # 先列出所有班级
        rd =  self.list_school_class()
        pprint(rd, indent=2)

        # 删除列出的所有班级
        for one in rd['retlist']:
            self.delete_school_class(one['id'])

        #再列出七年级所有班级
        rd =  self.list_school_class(1)
        pprint (rd,indent=2)

        # 如果没有删除干净，通过异常报错给RF
        # 参考http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#reporting-keyword-status
        if rd['retlist'] != []:
            raise  Exception("cannot delete all school classes!!")

    def classlist_should_contain(self,
                                 classlist,
                                 classname,
                                 gradename,
                                 invitecode,
                                 studentlimit,
                                 studentnumber,
                                 classid,
                                 expectedtimes=1):

        item = {
            "name": classname,
            "grade__name": gradename,
            "invitecode": invitecode,
            "studentlimit": int(studentlimit),
            "studentnumber": int(studentnumber),
            "id": classid,
            "teacherlist": []
        }

        occurTimes = classlist.count(item)
        logger.info('occur {} times'.format(occurTimes))

        if  occurTimes != int(expectedtimes):
            raise Exception(f'班级列表包含了{occurTimes}次指定信息,期望包含{expectedtimes}!!')




    def classlist_should_not_contain(self,
                                 classlist,
                                 classname,
                                 gradename,
                                 invitecode,
                                 studentlimit,
                                 studentnumber,
                                 classid):

        item = {
            "name": classname,
            "grade__name": gradename,
            "invitecode": invitecode,
            "studentlimit": int(studentlimit),
            "studentnumber": int(studentnumber),
            "id": classid,
            "teacherlist": []
        }

        if  item in classlist:
            raise Exception('班级列表包含了指定的班级信息!!')



if __name__ == '__main__':
    scm = SchoolClassLib()
    ret = scm.list_school_class(1)

    ret = scm.add_school_class(1,'新测试',77)

    ret = scm.add_school_class(1,'新测试2',77)

    # print(json.dumps(ret, indent=2))
    #
    # ret = scm.delete_school_class(28)
    # print(json.dumps(ret, indent=2))
    #
    # ret = scm.list_school_class(1)
    # print(json.dumps(ret, indent=2))
    # #
    # scm.delete_all_school_classes()

