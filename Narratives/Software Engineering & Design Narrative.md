# Software Engineering & Design Narrative

## **Briefly describe the artifact. What is it? When was it created?**

The artifact is an animal outcomes dashboard originally developed in CS-340: Client/Server Development. The initial version, created as a Jupyter Notebook, used JupyterDash to render visualizations from a MongoDB dataset, showing information like adoption rates and animal types over time. The project has since been enhanced and fully restructured into a standalone Flask web application, using HTML templates, modular backend code, and improved maintainability. The original was created in a past term during my core coursework, and the enhanced version was developed during the current capstone.

## **Justify the inclusion of the artifact in your ePortfolio. Why did you select this item? What specific components of the artifact showcase your skills and abilities in software development? How was the artifact improved?**

I selected this artifact because it reflects a complete transformation in the way I approach software design and engineering. The original dashboard functioned well but was embedded in a notebook environment that was difficult to maintain, scale, or deploy. It lacked modularity, proper routing, and a clear separation between data access and presentation logic.
The enhanced version, now built in Flask, showcases key software development skills such as modular architecture, template rendering using Jinja2, static asset management, and route control. I reorganized the project into a clean folder structure with app.py managing routing, crud.py handling database logic, and index.html rendering dynamic charts. This separation of concerns improves readability, testability, and makes the dashboard deployable on the web—far beyond what the notebook could support.

## **Did you meet the course outcomes you planned to meet with this enhancement in Module One? Do you have any updates to your outcome-coverage plans?**

Yes, I met the outcomes I initially targeted for this enhancement. Specifically:
-	Outcome 2: I demonstrated the ability to deliver professional-quality, technically sound visual communications through the redesign of the user interface and web structure.
-	Outcome 4: I applied modern development practices using Flask and MongoDB integration, showcasing innovative tools that deliver real-world value.
No changes are needed to the outcome-coverage plan, as this enhancement successfully supports both outcomes through improved application design and deployment readiness.

## **Reflect on the process of enhancing and modifying the artifact. What did you learn as you were creating it and improving it? What challenges did you face?**

Converting the notebook to a Flask application taught me how different a true web application is from an exploratory data project. I had to think in terms of routes, views, and data lifecycles rather than just outputting cells. Learning how to use Jinja2 templating to separate HTML from Python logic was a valuable experience, as was organizing files into static and template directories for long-term maintainability.
One challenge I encountered was adapting Plotly-based charts to render dynamically in a static HTML context instead of an interactive notebook. This required embedding JSON chart data directly into templates and carefully managing how visual components loaded on the page. Another challenge was ensuring the CRUD-based backend remained consistent and functional through the shift to a modular Flask environment.
Ultimately, the project was greatly improved in clarity, usability, and professionalism, and it now represents a real, deployable application that showcases full-stack development practices.
