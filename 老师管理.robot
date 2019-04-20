*** Settings ***
Library    pylib.TeacherLib
Variables   cfg.py


*** Test Cases ***
添加老师2 - tc001002

# 添加一个 老师 教7年级1班 科学

    ${addRet}=    add teacher    murongke   慕容恪
            ...  ${g_subject_science_id}
            ...  ${suite_g7c1_classid}
            ...  13000000002  1302@g.com  320520002

    should be true     $addRet['retcode']==0

#列出老师，检验一下
    ${listRet}=    list teacher

    teacherlist should contain   &{listRet}[retlist]
            ...  murongke   慕容恪   &{addRet}[id]
            ...  ${suite_g7c1_classid}
            ...  13000000002  1302@g.com  320520002

    [Teardown]    delete teacher   &{addRet}[id]



添加老师3 - tc001003


#列出老师
    ${listRet1}=    list teacher


# 添加 老师 教7年级1班 科学
    ${addRet}=    add teacher    tuobahong   拓跋宏2
           ...  ${g_subject_science_id}
           ...  ${suite_g7c1_classid}
           ...  13000000002  1302@g.com  320520002

    should be true     $addRet['retcode']==1
    should be true     $addRet['reason']=="登录名 tuobahong 已经存在"

#列出老师，检验一下
    ${listRet2}=    list teacher

    should be equal   ${listRet1}    ${listRet2}



删除老师1 - tc001081


#列出老师
    ${listRet1}=    list teacher


#删除老师，不存在的ID
    ${delRet}=   delete teacher   99999999
    should be true     $delRet['retcode']==404
    should be true     $delRet['reason']==u"id 为`99999999`的老师不存在"

#列出老师，检验一下
    ${listRet2}=    list teacher

    should be equal   ${listRet1}    ${listRet2}



删除老师2 - tc001082


#列出老师
    ${listRet1}=    list teacher


# 添加 老师 教7年级1班 科学
    ${addRet}=    add teacher    murongke   慕容恪
           ...  ${g_subject_science_id}
           ...  ${suite_g7c1_classid}
           ...  13000000002  1302@g.com  320520002

    should be true     $addRet['retcode']==0

#删除老师
    delete teacher   &{addRet}[id]

#列出老师，检验一下
    ${listRet2}=    list teacher

    should be equal   ${listRet1}    ${listRet2}
