drop table if exists employees cascade;
drop table if exists departments cascade;
drop table if exists dept_emp;
drop table if exists dept_manager;
drop table if exists salaries;
drop table if exists titles;

create table if not exists employees (
emp_no int,
birth_date date,
first_name varchar(30),
last_name varchar(30),
gender varchar(1),
hire_date date,
primary key (emp_no, hire_date));
/*alter table employees
drop constraint employees_pkey cascade;
alter table employees
add primary key (emp_no, hire_date);*/

create table if not exists departments (
dept_no varchar(4) primary key,
dept_name varchar(30));

create table if not exists titles (
emp_no int, constraint emp_no foreign key (emp_no) references employees (emp_no),
title varchar(30),
from_date date,
to_date date,
primary key (emp_no, from_date));

create table if not exists salaries (
emp_no int,
salary int,
from_date date,
to_date date);

alter table salaries
add constraint emp_no
foreign key (emp_no) 
references employees (emp_no);
alter table salaries
add primary key (emp_no, from_date);

alter table dept_manager
drop constraint dept_manager_pkey;

create table if not exists dept_manager (
dept_no varchar(4),
emp_no int,
from_date date,
to_date date);

alter table dept_manager
add constraint emp_no foreign key (emp_no)
references employees (emp_no);
alter table dept_manager
add constraint dept_no foreign key (dept_no)
references departments (dept_no);
alter table dept_manager
add primary key (dept_no, emp_no);

create table if not exists dept_emp (
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

/*insert into departments values
('d001','Marketing'),
('d002','Finance'),
('d003','Human Resources'),
('d004','Production'),
('d005','Development'),
('d006','Quality Management'),
('d007','Sales'),
('d008','Research'),
('d009','Customer Service');*/
select * from employees;
