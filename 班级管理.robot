*** Settings ***
Library    pylib.SchoolClassLib
Variables   cfg.py


*** Test Cases ***
添加班级2 - tc000002
# 添加 7年级2班
    ${ret1}=    add school class    ${g_grade_7_id}     2班     60
    should be true     $ret1['retcode']==0

#列出班级，检验一下
    ${ret2}=    list school class    ${g_grade_7_id}
    ${retlist}=   evaluate   $ret2['retlist']
    classlist should contain   ${retlist}
    ...  2班  七年级    &{ret1}[invitecode]   60   0   &{ret1}[id]

    [Teardown]    delete_school_class   &{ret1}[id]


添加班级3 - tc000003

#  添加7年级1班
    ${ret1}=    add school class    ${g_grade_7_id}     1班     60
    should be true     $ret1['retcode']==1
    should be true     $ret1['reason']=='duplicated class name'

#列出班级，检验一下
    ${ret2}=    list school class    ${g_grade_7_id}

    classlist should not contain   &{ret2}[retlist]
                               ...  1班   七年级
                               ...  &{ret1}[invitecode]
                               ...  60  0  &{ret1}[id]



修改班级1 - tc000051

#  添加7年级2班
    ${ret1}=    add school class    ${g_grade_7_id}     2班     60
    should be true     $ret1['retcode']==0
    ${classid}=    evaluate  $ret1['id']

#  修改为7年级  222班

    ${modifyRet}=    modify school class   ${classid}   222班     60
    should be true     $modifyRet['retcode']==0


#  列出班级，检验一下
    ${ret2}=    list school class    ${g_grade_7_id}

    classlist should contain   &{ret2}[retlist]
                               ...  222班   七年级   &{ret1}[invitecode]   60  0  &{ret1}[id]

    [Teardown]    delete_school_class   ${classid}



修改班级2 - tc000052

#  添加7年级2班
    ${ret1}=    add school class    ${g_grade_7_id}     2班     60
    should be true     $ret1['retcode']==0
    ${classid}=    evaluate  $ret1['id']

#  先列出班级
    ${listret1}=    list school class    ${g_grade_7_id}

#  修改为7年级1班
    ${modifyRet}=    modify school class   ${classid}   1班     60
    should be true     $modifyRet['retcode']==1
    should be true     $modifyRet['reason']=='duplicated class name'


#  再次列出班级，检验一下，应该和之前列出的相同
    ${listret2}=    list school class    ${g_grade_7_id}
    should be equal    ${listret1}     ${listret2}

    [Teardown]    delete_school_class   ${classid}


修改班级3 - tc000053

#  修改班级，ID号为一个不存在的ID
    ${modifyRet}=    modify school class   99999999    1班     60
    should be equal     &{modifyRet}[retcode]       ${404}
    should be equal     &{modifyRet}[reason]     id 为`99999999`的班级不存在


删除班级1 - tc000081

#  删除班级，ID号为一个不存在的ID
    ${delRet}=    delete_school_class   99999999
    should be equal     &{delRet}[retcode]       ${404}
    should be equal     &{delRet}[reason]     id 为`99999999`的班级不存在


删除班级2 - tc000082

#  先列出班级
    ${listret1}=    list school class    ${g_grade_7_id}


#  添加7年级2班
    ${addRet}=    add school class    ${g_grade_7_id}     2班     60
    should be true     $addRet['retcode']==0
    ${classid}=    evaluate  $addRet['id']


# 再列出班级，检验一下
    ${listret2}=    list school class    ${g_grade_7_id}

    classlist should contain   &{listret2}[retlist]
                               ...  2班   七年级   &{addRet}[invitecode]
                               ...  60  0  &{addRet}[id]


#  删除7年级2班
    ${delRet}=    delete_school_class   ${classid}
    should be equal     &{delRet}[retcode]       ${0}


#  第三次列出班级，检验一下
    ${listret3}=    list school class    ${g_grade_7_id}
    should be equal    ${listret1}     ${listret3}


