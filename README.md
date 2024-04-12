# Shape's Data Engineering Interview Tech Case
The **FPSO** vessel contains some equipment and each equipment have multiple sensors. Every time a failure happens, we get all the sensors data from the failed equipment, and we store this information in a log file (the time is in GMT time zone).

You are provided 3 files: the log file named “**equipment_failure_sensors.txt**”; the file named “**equipment_sensors.csv**” with the relationships between sensors and equipment’s; and the file named “**equipment.json**” with the equipment data.

### OBS: This test can be done either *BEFORE* or *DURING* the tech interview.

> ## Steps

> - **Fork** or **Clone** this repository before starting the tech test.

> - *Extract **equipment_failure_sensors.rar** to a path/folder so you can read the .txt data.*

> - You **must** structure your data in a way that queries will be optimized according to the data retrieval process regarding equipment, sensors, and dates. Data can also be manipulated in **ACID** transactions.

> - **Use Python, SQL and/or PySpark as the languages/frameworks - you may use other tools if necessary for recommended and/or plus actions.**

> - **You're free to modify the files into any extension, as long as the main data is preserved. If you wish to modify the source data, make sure you use a copy method to keep the new data decoupled from the source data.**

1. Total equipment failures that happened?

2. Which equipment name had most failures?

3. Average amount of failures across equipment group, ordered by the number of failures in ascending order?

4.  Rank the sensors which present the most number of errors by equipment name in an equipment group.

### Recommendations: 

>- Use OOP to structure your pipeline.
>- Use PEP or Black coding style.
>- Use a GIT provider for code versioning.
>- Diagram of your resolution(s).

### Plus:

>- Tests.
>- Simulate a streaming pipeline.
>- Dockerize your app.
>- Orchestration architecture.
