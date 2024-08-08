<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SoftCart Data Platform Architecture</title>
</head>
<body>

<h1>SoftCart Data Platform Architecture</h1>

<h2>Overview</h2>
<p>SoftCart is an e-commerce company that employs a hybrid data platform architecture, combining both on-premises and cloud-based databases to manage its operations.</p>

<h2>Tools and Technologies</h2>
<ul>
    <li><strong>OLTP Database</strong>: MySQL</li>
    <li><strong>NoSQL Database</strong>: MongoDB</li>
    <li><strong>Production Data Warehouse</strong>: IBM DB2 on Cloud</li>
    <li><strong>Staging Data Warehouse</strong>: PostgreSQL</li>
    <li><strong>Big Data Platform</strong>: Hadoop</li>
    <li><strong>Big Data Analytics Platform</strong>: Apache Spark</li>
    <li><strong>Business Intelligence Dashboard</strong>: IBM Cognos Analytics</li>
    <li><strong>Data Pipelines</strong>: Apache Airflow</li>
</ul>

<h2>Architecture Description</h2>

<h3>1. Online Presence</h3>
<p>SoftCart's online store is accessible via various devices, including laptops, mobiles, and tablets. The platform’s functionality is supported by two primary databases:</p>
<ul>
    <li><strong>MySQL</strong>: Stores all transactional data such as inventory and sales.</li>
    <li><strong>MongoDB</strong>: Houses all product catalog data.</li>
</ul>

<h3>2. Data Flow and Storage</h3>
<p>Data from <strong>MySQL</strong> and <strong>MongoDB</strong> is regularly extracted and transferred to the staging data warehouse on <strong>PostgreSQL</strong>. The production data warehouse resides on <strong>IBM DB2 Cloud</strong>, where the data is prepared for analysis.</p>

<h3>3. Big Data and Analytics</h3>
<p><strong>Hadoop</strong> serves as the big data platform where all the company’s data is accumulated for in-depth analytics. <strong>Apache Spark</strong> processes and analyzes the data stored on the Hadoop cluster.</p>

<h3>4. Business Intelligence</h3>
<p>The BI team connects to the <strong>IBM DB2</strong> production warehouse to create operational dashboards. <strong>IBM Cognos Analytics</strong> is utilized for the creation and management of these dashboards.</p>

<h3>5. Data Pipelines</h3>
<p>Data movement between OLTP, NoSQL, and the data warehouse is managed by ETL pipelines running on <strong>Apache Airflow</strong>.</p>

<h2>Summary</h2>
<p>SoftCart's hybrid data architecture leverages a mix of on-premises and cloud technologies to ensure robust data management, seamless analytics, and effective business intelligence reporting.</p>

</body>
</html>
