# Databases Narrative

## **Briefly describe the artifact. What is it? When was it created?**

This artifact is an animal outcomes dashboard project initially created in CS‑340: Client/Server Development. The original version was a Jupyter Notebook that used a local CSV file (aac_shelter_outcomes.csv) and basic data filtering through pandas to display visualizations and perform data analysis. In contrast, the enhanced version transitions the data layer to a cloud-hosted MongoDB Atlas database, supports dynamic queries via Flask, and incorporates more advanced database features like aggregation pipelines, compound indexing, and search filtering. The enhanced version was developed as part of this capstone to demonstrate improved backend architecture and data operations.

## **Justify the inclusion of the artifact in your ePortfolio. Why did you select this item? What specific components of the artifact showcase your skills and abilities in software development? How was the artifact improved?**

I selected this artifact because it highlights a significant leap in my ability to work with databases in a professional and scalable way. The original dashboard was limited to reading static CSV data with no backend database. All logic for filtering, sorting, and analyzing had to be re-executed every time the notebook ran, and there was no concept of user-specific or real-time interactivity.
In the enhanced version, I moved the dataset to MongoDB Atlas, allowing for real-time remote access to structured animal records. I wrote modular code in crud.py to perform robust CRUD operations and implemented advanced MongoDB features like:
•	Aggregation pipelines to group and analyze data server-side
•	Compound indexes to improve query efficiency on commonly filtered fields
•	Environment-based connection configuration for secure cloud access
This upgrade transformed the dashboard into a fully functioning database-driven web application, and it showcases my skills in backend integration, NoSQL data modeling, and secure database management.

## **Did you meet the course outcomes you planned to meet with this enhancement in Module One? Do you have any updates to your outcome-coverage plans?**

Yes, I met the expected outcomes with this enhancement. It directly supports:

- Course Outcome 4: Demonstrate innovative techniques, skills, and tools in computing practices that deliver value and accomplish industry-specific goals.
-	Course Outcome 5: Develop a security mindset that anticipates exploits in software architecture, ensuring privacy and security of data.

There are no changes needed to my outcome-coverage plan for this category. The secure integration of MongoDB Atlas and indexing strategies demonstrates both technical skill and data-handling foresight.

## **Reflect on the process of enhancing and modifying the artifact. What did you learn as you were creating it and improving it? What challenges did you face?**

Enhancing the dashboard to use a remote MongoDB database taught me valuable lessons about database connectivity, security, and query design in modern web applications. One of the most important realizations was how different working with a live backend is compared to static data. Every query had to be efficient and secure, especially since the data was now hosted in the cloud.
One challenge I encountered was properly securing the MongoDB credentials while still keeping the project easy to deploy for other users. I learned to use .env files and the python-dotenv package to isolate sensitive connection strings and prevent hardcoding secrets into the source code. Another challenge was designing aggregation queries that offload data processing to the database instead of the application layer and ensuring the most frequently filtered fields were properly indexed for performance.
Through this process, I became more confident in my ability to design database-integrated web applications and to think critically about performance and security at scale.
