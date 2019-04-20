*** Settings ***
Library    pylib.WebOpLib
Library    pylib.TeacherLib
Variables   cfg.py

Suite Setup    open browser
Suite Teardown   close browser


*** Test Cases ***
老师登录2 - tc005002
# 添加 老师
    ${addRet}=    add teacher    tuobahong   拓跋宏   ${g_subject_math_id}
           ...  ${suite_g7c1_classid}  13000000001  1301@g.com  320520001

    should be true     $addRet['retcode']==0

#老师登录

    teacher login   tuobahong   888888


    ${ateacherinfo}=  get teacher homepage info
    ${eteacherinfo}=   create list   松勤学院0001   拓跋宏  初中数学  0   0   0
    should be equal    ${ateacherinfo}    ${eteacherinfo}

    ${aclassstudents}=  get teacher class students info

#    七年级   1班 中间有几个空格  可以由日志中拷贝出来
    should be true     $aclassstudents=={'七年级1班':['谢玄']}


    [Teardown]    delete teacher   &{addRet}[id]

