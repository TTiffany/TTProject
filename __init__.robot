*** Settings ***
Library    pylib.StudentLib
Variables   cfg.py

Suite Setup    add student   xiexuan   谢玄
        ...  ${g_grade_7_id}
        ...  ${suite_g7c1_classid}    13200000001
        ...  suite_student_id

Suite Teardown    delete student   ${suite_student_id}
