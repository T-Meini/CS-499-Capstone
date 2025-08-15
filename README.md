# ePortfolio
**CS-499 Capstone by Tanner Meininger**

## Professional Self-Assessment
My journey through the Computer Science program at Southern New Hampshire University has been an amazing opportunity to shape my skills, professional values, and career goals. This program has given me a strong technical foundation in software engineering, algorithms, databases, and security, while also strengthening my ability to collaborate effectively and communicate clearly in professional settings.

Collaboration has been a consistent part of my academic and professional development. For example, in one class project, I worked with a small team to design a web application where each member was responsible for a separate feature. My role was to integrate the database connection layer with the front-end form submissions, which required close coordination with both the database lead and the UI designer to ensure seamless functionality. This experience taught me the importance of clear communication, version control discipline, and adapting my work to fit the needs of the overall project.

Communicating with stakeholders has also been an essential skill I’ve built over the course of my studies. In one case, I presented a basic data visualization dashboard to a non-technical audience and explained how the charts reflected underlying trends in plain language rather than technical jargon. This helped ensure that decision-makers understood the meaning of the data without needing to know the technical details of how it was processed. Experiences like this reinforced my ability to translate technical concepts into actionable insights.

In the area of data structures and algorithms, I have developed a strong understanding of how to approach problem-solving methodically, choose optimal data structures, and implement efficient solutions. For example, in a coding exercise, I replaced a brute-force search through a large dataset with a hash map lookup, reducing the search time from several seconds to nearly instantaneous. This taught me how algorithmic thinking can lead to tangible performance improvements in an application.

Software engineering principles have been central to my development as a programmer. I have worked on projects that required breaking a large, monolithic script into smaller, reusable modules. In one case, I reorganized a Python application into separate files for database operations, routing logic, and user interface rendering, which made the project easier to maintain and debug. This modular approach also prepared the project for deployment, something that was not possible in its original form.

My database experience spans from designing schemas and implementing CRUD operations to optimizing queries and integrating secure, cloud-hosted solutions. For instance, I built a database-driven app that allowed users to filter and sort data in real time. I implemented indexing on frequently searched fields, which significantly improved query performance. This reinforced the idea that small backend changes can lead to large gains in usability and efficiency.

Security awareness has been integrated into my approach to all aspects of computing. For example, when working with a login form, I made sure to store passwords as hashed values instead of plain text and used environment variables to store sensitive API keys. These steps prevented exposing confidential information in the source code and reduced the risk of security breaches.

Taken together, these skills form the foundation of my professional identity as a computer scientist. The ePortfolio serves as a representation of my technical expertise, problem-solving abilities, and readiness to deliver high-quality, professional software solutions. It reflects my ability to bridge the gap between technical implementation and real-world application, allowing me to show how I can contribute effectively in the ever-evolving technology field.

## Code Review

📺 **[Watch my Full Code Review Video](https://youtu.be/XOeZaSNp0Yw)**

In this video, I walk through the original CS-340 dashboard, review the code for each enhancement category, and explain the reasoning and process behind my modifications.

## Enhancement One - Software Design & Engineering

**[Link to Original File](https://github.com/T-Meini/ePortfolio/tree/main/Original%20Project)**

**[Link to Enhanced File](https://github.com/T-Meini/ePortfolio/tree/main/Software%20Engineering%20%26%20Design%20Enhancement)**

The artifact that was selected was an animal outcomes dashboard originally developed in CS-340: Client/Server Development. The initial version, created as a Jupyter Notebook, used JupyterDash to render visualizations from a MongoDB dataset, showing information like adoption rates and animal types over time. The project has since been enhanced and fully restructured into a standalone Flask web application, using HTML templates, modular backend code, and improved maintainability. The original was created in a past term during my core coursework, and the enhanced version was developed during the current capstone.

![Figure 1: Look of the Original Dashboard](https://raw.githubusercontent.com/T-Meini/ePortfolio/refs/heads/main/Images/Original%20Dashboard.png)
>_Figure 1: Look of the original dashboard_
 ---
![Figure 2: Remade and Enhanced Flask Dashboard](https://raw.githubusercontent.com/T-Meini/ePortfolio/refs/heads/main/Images/Enhancement%201.png)
>_Figure 2: Remade and Enhanced Flask Dashboard_

I selected this artifact because it reflects a complete transformation in the way I approach software design and engineering. The original dashboard functioned well but was embedded in a notebook environment that was difficult to maintain, scale, or deploy. It lacked modularity, proper routing, and a clear separation between data access and presentation logic. The enhanced version, now built in Flask, showcases key software development skills such as modular architecture, template rendering using Jinja2, static asset management, and route control. I reorganized the project into a clean folder structure with app.py managing routing, crud.py handling database logic, and index.html rendering dynamic charts. This separation of concerns improves readability, testability, and makes the dashboard deployable on the web—far beyond what the notebook could support.

For this enhancement, I met the outcomes I initially targeted. Specifically:

- Outcome 1: I showed that there is room for building collaborative environments that enable diverse audiences to support organizational decision making in the field of computer science through maintainability and organization of files
- Outcome 2: I demonstrated the ability to deliver professional-quality, technically sound visual communications through the redesign of the user interface and web structure.
- Outcome 4: I applied modern development practices using Flask and MongoDB integration, showcasing innovative tools that deliver real-world value. No changes are needed to the outcome-coverage plan, as this enhancement successfully supports both outcomes through improved application design and deployment readiness.

When reflecting on this project, converting the notebook to a Flask application taught me how different a true web application is from an exploratory data project. I had to think in terms of routes, views, and data lifecycles rather than just outputting cells. Learning how to use Jinja2 templating to separate HTML from Python logic was a valuable experience, as was organizing files into static and template directories for long-term maintainability. One challenge I encountered was adapting Plotly-based charts to render dynamically in a static HTML context instead of an interactive notebook. This required embedding JSON chart data directly into templates and carefully managing how visual components loaded on the page. Another challenge was ensuring the CRUD-based backend remained consistent and functional through the shift to a modular Flask environment. Ultimately, the project was greatly improved in clarity, usability, and professionalism, and it now represents a real, deployable application that showcases full-stack development practices.

## Enhancement Two – Algorithms & Data Structures

**[Link to Original File](https://github.com/T-Meini/ePortfolio/tree/main/Original%20Project)**

**[Link to Enhanced File](https://github.com/T-Meini/ePortfolio/tree/main/Algorithms%20%26%20Data%20Structures%20Enhancement)**

Like the previous enhancement, this uses the same artifact which is an interactive dashboard application originally created in CS‑340: Client/Server Development. The original version was a Jupyter Notebook that visualized animal shelter data using static filters and hard-coded queries. In its enhanced form, the dashboard has been converted into a Flask web app and now features a real-time search capability that uses a HashMap (Python dictionary) to efficiently filter animals by name.

![Figure 3: Addition of Hash Search Function to Dashboard with Example Search](https://raw.githubusercontent.com/T-Meini/ePortfolio/24c7e29e0e7bb09c196a9b4ce221f06e2885ca7a/Images/Enhancement%202.png)
>_Figure 3: Addition of Hash Search Function to Dashboard with Example Search_

I chose this artifact because the enhancement clearly demonstrates my ability to apply efficient data structures in a real-world scenario. The original notebook relied on filtering data directly through MongoDB queries, which was functional but not optimized for performance or responsiveness when handling multiple user interactions. In the enhanced version, I integrated a HashMap to act as a lookup table for animal names and metadata. This change drastically improved the efficiency and responsiveness of the search feature. Instead of querying the database repeatedly, the app now loads animal data into a dictionary on page load and allows for constant-time access while the user types. This demonstrates a practical application of data structure optimization in a user-focused, web-based context.

When looking at the course outcomes, this enhancement directly supports:

- Course Outcome 3: “Design and evaluate computing solutions that solve a given problem using algorithmic principles and computer science practices.” I applied algorithmic thinking to reduce the complexity of repeated searches and improve the scalability of the dashboard. I do not need to make any updates to the outcome-coverage plan—this enhancement met the objective as originally outlined.

Through this enhancement, I deepened my understanding of how performance and usability are directly impacted by the choice of data structures. I learned to balance client-side responsiveness with backend efficiency, and how pre-processing data into a searchable structure can make a web application feel faster and more modern. A major challenge was integrating the search feature without sacrificing scalability. I had to ensure that the initial dictionary build was efficient and didn’t degrade performance with large datasets. Testing this across different browsers also introduced edge cases with how the search input interacted with the dynamically rendered results. Additionally, making this feature feel seamless within a Flask application meant ensuring the search logic ran in sync with the rendering engine and the user’s expectations. In the end, this enhancement not only improved the functionality of the dashboard but also demonstrated my ability to apply core computer science concepts like hash-based lookups in a practical, user-facing solution.

## Enhancement Three – Databases

**[Link to Original File](https://github.com/T-Meini/ePortfolio/tree/main/Original%20Project)**

**[Link to Enhanced File](https://github.com/T-Meini/ePortfolio/tree/main/Databases%20Enhancement)**

Similarily to the last two, this enhancement also uses the same artifact which is the animal outcomes dashboard project initially created in CS‑340: Client/Server Development. The original version was a Jupyter Notebook that used a local CSV file (aac_shelter_outcomes.csv) and basic data filtering through pandas to display visualizations and perform data analysis. In contrast, the enhanced version, in addition to the conversion to flask and implmentation of the hash map search function, transitions the data layer to a cloud-hosted MongoDB Atlas database, supports dynamic queries via Flask, and incorporates more advanced database features like aggregation pipelines, compound indexing, and search filtering. The enhanced version was developed as part of this capstone to demonstrate improved backend architecture and data operations.

![Figure 4: Addition of Button to Analytics Page and Ability to Export the Data to a CSV](https://raw.githubusercontent.com/T-Meini/ePortfolio/refs/heads/main/Images/Enhancement%203%20Part%201.png)
>_Figure 4: Addition of Button to Analytics Page and Ability to Export the Data to a CSV_
 ---
![Figure 5: New Analytics Page to Display More Advanced Features](https://raw.githubusercontent.com/T-Meini/ePortfolio/refs/heads/main/Images/Enhancement%203%20Part%202.png)
>_Figure 5: New Analytics Page to Display More Advanced Features_

I selected this artifact because it highlights a significant leap in my ability to work with databases in a professional and scalable way. The original dashboard was limited to reading static CSV data with no backend database. All logic for filtering, sorting, and analyzing had to be re-executed every time the notebook ran, and there was no concept of user-specific or real-time interactivity. In the enhanced version, I moved the dataset to MongoDB Atlas, allowing for real-time remote access to structured animal records. I wrote modular code in crud.py to perform robust CRUD operations and implemented advanced MongoDB features like: • Aggregation pipelines to group and analyze data server-side • Compound indexes to improve query efficiency on commonly filtered fields • Environment-based connection configuration for secure cloud access This upgrade transformed the dashboard into a fully functioning database-driven web application, and it showcases my skills in backend integration, NoSQL data modeling, and secure database management.

For this enhancement, I met the expected outcomes, which directly supports: 

- Course Outcome 4: Demonstrate innovative techniques, skills, and tools in computing practices that deliver value and accomplish industry-specific goals. 
- Course Outcome 5: Develop a security mindset that anticipates exploits in software architecture, ensuring privacy and security of data. 

There are no changes needed to my outcome-coverage plan for this category. The secure integration of MongoDB Atlas and indexing strategies demonstrates both technical skill and data-handling foresight.

In the end, enhancing the dashboard to use a remote MongoDB database taught me valuable lessons about database connectivity, security, and query design in modern web applications. One of the most important realizations was how different working with a live backend is compared to static data. Every query had to be efficient and secure, especially since the data was now hosted in the cloud. One challenge I encountered was properly securing the MongoDB credentials while still keeping the project easy to deploy for other users. I learned to use .env files and the python-dotenv package to isolate sensitive connection strings and prevent hardcoding secrets into the source code. Another challenge was designing aggregation queries that offload data processing to the database instead of the application layer and ensuring the most frequently filtered fields were properly indexed for performance. Through this process, I became more confident in my ability to design database-integrated web applications and to think critically about performance and security at scale.
