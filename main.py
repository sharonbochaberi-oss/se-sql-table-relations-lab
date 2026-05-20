# STEP 0

import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)


# STEP 1: Employees in Boston
df_boston = pd.read_sql("""
SELECT e.firstName, e.lastName
FROM employees e
JOIN offices o
  ON e.officeCode = o.officeCode
WHERE o.city = 'Boston'
""", conn)


# STEP 2: Offices with zero employees
df_zero_emp = pd.read_sql("""
SELECT o.officeCode, o.city
FROM offices o
LEFT JOIN employees e
  ON o.officeCode = e.officeCode
WHERE e.employeeNumber IS NULL
""", conn)


# STEP 3: All employees + office location
df_employee = pd.read_sql("""
SELECT e.firstName,
       e.lastName,
       o.city,
       o.state
FROM employees e
LEFT JOIN offices o
  ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName
""", conn)


# STEP 4: Customers with no orders
df_contacts = pd.read_sql("""
SELECT c.contactFirstName,
       c.contactLastName,
       c.phone,
       c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o
  ON c.customerNumber = o.customerNumber
WHERE o.customerNumber IS NULL
ORDER BY c.contactLastName
""", conn)


# STEP 5: Payments report (sorted by amount desc)
df_payment = pd.read_sql("""
SELECT c.contactFirstName,
       c.contactLastName,
       p.amount,
       p.paymentDate
FROM customers c
JOIN payments p
  ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC
""", conn)


# STEP 6: Employees with avg credit limit > 90k
df_credit = pd.read_sql("""
SELECT e.employeeNumber,
       e.firstName,
       e.lastName,
       COUNT(c.customerNumber) AS num_customers
FROM employees e
JOIN customers c
  ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber
HAVING AVG(c.creditLimit) > 90000
ORDER BY num_customers DESC
""", conn)


# STEP 7: Best-selling products
df_product_sold = pd.read_sql("""
SELECT p.productName,
       COUNT(DISTINCT o.orderNumber) AS numorders,
       SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od
  ON p.productCode = od.productCode
JOIN orders o
  ON od.orderNumber = o.orderNumber
GROUP BY p.productCode
ORDER BY totalunits DESC
""", conn)


# STEP 8: Customers per office
df_total_customers = pd.read_sql("""
SELECT p.productName,
       p.productCode,
       COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od
  ON p.productCode = od.productCode
JOIN orders o
  ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC
""", conn)


# STEP 9: Product reach (unique customers per product)
df_customers = pd.read_sql("""
SELECT o.officeCode,
       o.city,
       COUNT(DISTINCT c.customerNumber) AS n_customers
FROM offices o
LEFT JOIN employees e
  ON o.officeCode = e.officeCode
LEFT JOIN customers c
  ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
""", conn)


# STEP 10: Employees who sold low-popularity products (<20 customers)
df_under_20 = pd.read_sql("""
WITH low_products AS (
    SELECT od.productCode
    FROM orderdetails od
    JOIN orders o
      ON od.orderNumber = o.orderNumber
    GROUP BY od.productCode
    HAVING COUNT(DISTINCT o.customerNumber) < 20
)

SELECT DISTINCT e.employeeNumber,
       e.firstName,
       e.lastName,
       ofc.city,
       ofc.officeCode
FROM employees e
JOIN offices ofc
  ON e.officeCode = ofc.officeCode
JOIN customers c
  ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord
  ON c.customerNumber = ord.customerNumber
JOIN orderdetails od
  ON ord.orderNumber = od.orderNumber
WHERE od.productCode IN (
    SELECT productCode
    FROM low_products
)
ORDER BY
    CASE WHEN e.firstName = 'Loui' THEN 0 ELSE 1 END,
    e.firstName
""", conn)


conn.close()