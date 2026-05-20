Lab: SQL Table Relations
Overview

we use SQL JOINs, GROUP BY, and subqueries with the Northwind CRM database. You will connect multiple related tables to analyze employees, customers, orders, and products.

This lab focuses on:

Writing different types of JOINs
Filtering and aggregating data
Using subqueries / CTEs
Producing business-style reports from relational data
Setup

Install dependencies and activate the environment:

pipenv install
pipenv shell

Run your script with:

python3 main.py

Run tests with:

pytest
Database Connection

You will use SQLite:

import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

pd.read_sql("SELECT * FROM sqlite_master", conn)
Tasks
Part 1: JOIN + Filtering
Step 1 — Employees in Boston

Return:

firstName
lastName
jobTitle

For employees working in Boston.

Step 2 — Offices with No Employees

Return:

officeCode
city

For offices that have zero employees.

Part 2: JOIN Types
Step 3 — All Employees with Office Info

Return:

firstName
lastName
city
state

Include all employees, even if they have no office.
Sort by firstName, then lastName.

Step 4 — Customers With No Orders

Return:

contactFirstName
contactLastName
phone
salesRepEmployeeNumber

Only customers who have never placed an order (24 total expected).
Sort by lastName.

Part 3: Built-in Functions
Step 5 — Payments Report

Return:

contactFirstName
contactLastName
amount
paymentDate

Sort by amount (descending).
Ensure numeric sorting for amount if needed.

Part 4: GROUP BY + Aggregation
Step 6 — High Credit Customers per Employee

Return:

employeeNumber
firstName
lastName
num_customers

Only employees whose customers have:

average creditLimit > 90,000

Sort by num_customers (desc).
Expected result: 4 employees.

Step 7 — Product Sales Summary

Return:

productName
numorders (count of orders)
totalunits (sum of quantityOrdered)

Sort by totalunits (desc).

Part 5: Multiple JOINs
Step 8 — Product Reach

Return:

productName
productCode
numpurchasers (unique customers)

Sort by numpurchasers (desc).

Step 9 — Customers per Office

Return:

officeCode
city
n_customers

Count customers assigned to each office via employees.

Part 6: Subquery / CTE
Step 10 — Employees Selling Low-Reach Products

Return:

employeeNumber
firstName
lastName
city
officeCode

Find employees who sold products purchased by:

fewer than 20 unique customers

Use a subquery or CTE.

Cleanup
conn.close()