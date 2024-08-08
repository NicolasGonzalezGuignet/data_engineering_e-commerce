<!DOCTYPE html>
<html lang="en">
<body>

<h1>Data engineering e-commerce project</h1>
<h3>A fully dockerized ELT pipeline project, using MYSQL, mongoDB, Apache Airflow, and PowerBI.</h3>
<h2>Overview</h2>
<p>SoftCart is an e-commerce company that employs a hybrid data platform architecture, combining both on-premises and cloud-based databases to manage its operations.</p>

<h2>Tools and Technologies</h2>
<ul>
    <li><strong>OLTP Database</strong>: MySQL</li>
    <li><strong>NoSQL Database</strong>: MongoDB</li>
    <li><strong>Production Data Warehouse</strong>: MySQL</li>
    <li><strong>Staging Data Warehouse</strong>: MySQL</li>
    <li><strong>Business Intelligence Dashboard</strong>: Power BI</li>
    <li><strong>Data Pipelines</strong>: Apache Airflow</li>
</ul>

<h2>Architecture Description</h2>

<h3>1. Online Presence</h3>
<p>The platform’s functionality is supported by two primary databases:</p>
<ul>
    <li><strong>MySQL</strong>: Stores all transactional data such as inventory and sales.</li>
    <li><strong>MongoDB</strong>: Houses all product catalog data.</li>
</ul>

<h3>2. Data Flow and Storage</h3>
<p>Data from <strong>MySQL</strong> and <strong>MongoDB</strong> is regularly extracted and transferred to the staging data warehouse on <strong>MySQL</strong>. The production data warehouse resides on <strong>MySQL</strong>, where the data is prepared for analysis.</p>

<h3>3. Business Intelligence</h3>
<p>The BI team connects to the <strong>MySQL</strong> production warehouse to create operational dashboards.</p>

<h3>4. Data Pipelines</h3>
<p>Data movement between OLTP, NoSQL, and the data warehouse is managed by ETL pipelines running on <strong>Apache Airflow</strong>.</p>


</body>
</html>
