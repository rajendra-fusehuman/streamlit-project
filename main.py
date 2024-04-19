import streamlit as st
import pandas as pd
import numpy as np
import pickle

app_mode = st.sidebar.selectbox('Select Page',['Employee Data Entry','Department Data Entry', 'Visualization'])

if 'df_employee' not in st.session_state:
    st.session_state.df_employee = pd.DataFrame({'empno': [], 'ename': [], 'job': [], 'deptno': []}).set_index('empno')
if 'df_department' not in st.session_state:
    st.session_state.df_department = pd.DataFrame({'deptno': [], 'dname': [], 'loc': []}).set_index('deptno')

if app_mode=='Employee Data Entry':
    st.title('Employee Data Entry')
    ename = st.text_input("Employee Name")
    job = st.text_input("Job")

    num_departments = st.session_state.df_department.shape[0]
    if num_departments == 0:
        st.number_input("Department Number", step=1, disabled=True)
    else:
        deptno = st.number_input("Department Number", min_value=0, max_value=num_departments-1, step=1)

    if st.button("Submit"):
        if ename == "":
            st.error("Employee name cannot be empty")
        elif job == "":
            st.error("Job cannot be empty")
        elif num_departments == 0:
            st.error("Add a department first")
        else:
            new_employee_index = st.session_state.df_employee.shape[0]
            st.session_state.df_employee = pd.concat([st.session_state.df_employee, pd.DataFrame([[new_employee_index, ename, job, deptno]], columns=['empno', 'ename', 'job', 'deptno'])], ignore_index=True)
            st.success("New employee added successfully")
            st.dataframe(st.session_state.df_employee.set_index('empno'))
elif app_mode == "Department Data Entry":
    st.title('Department Data Entry')
    # deptno = st.number_input("Department Number", min_value=1, step=1)
    dname = st.text_input("Department Name")
    loc = st.text_input("Location")

    if st.button("Submit"):
        if dname == "":
            st.error("Department name cannot be empty")
        elif loc == "":
            st.error("Location cannot be empty")
        else:
            new_department_index = st.session_state.df_department.shape[0]
            st.session_state.df_department = pd.concat([st.session_state.df_department, pd.DataFrame([[new_department_index, dname, loc]], columns=['deptno', 'dname', 'loc'])], ignore_index=True)
            st.success("New department added successfully")
            st.dataframe(st.session_state.df_department.set_index('deptno'))
elif app_mode == "Visualization":
    st.title('Data Visualization')
    try:
        df_joined = st.session_state.df_employee.set_index('deptno').join(st.session_state.df_department, on="deptno")
        st.dataframe(df_joined.set_index('empno'))
    except:
        st.warning("No available data")
