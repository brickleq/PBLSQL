create table titles (
emp_no int foreign key references (employees.emp_no),
title varchar(30),
from_date date,
to_date date);
alter table titles 
add primary key (emp_no, from_date);

create table salaries (
emp_no int,
salary int,
from_date date,
to_date date);
alter table salaries
add primary key (emp_no, from_date);
alter table salaries
add constraint emp_no
foreign key (emp_no) 
references employees (emp_no);

create table employees (
emp_no int primary key,
birth_date date,
first_name varchar(30),
last_name varchar(30),
gender varchar(1),
hire_date date);

create table dept_manager (
dept_no varchar(5),
emp_no int,
from_date date,
to_date date);
alter table dept_manager
add primary key (dept_no, from_date);
alter table dept_manager
add constraint emp_no foreign key (emp_no)
references employees (emp_no);
alter table dept_manager
add constraint dept_no foreign key (dept_no)
references departments (dept_no);

create table dept_emp (
emp_no int,
dept_no varchar(4),
from_date date,
to_date date);
alter table dept_emp
add constraint emp_no
foreign key (emp_no)
references employees (emp_no);
alter table dept_emp
add constraint dept_no
foreign key (dept_no)
references departments (dept_no);

create table departments (
dept_no varchar(4) primary key,
dept_name varchar(30));