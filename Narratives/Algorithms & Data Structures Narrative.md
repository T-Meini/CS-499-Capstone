# Algorithms & Data Structures Narrative

## **Briefly describe the artifact. What is it? When was it created?**

The artifact is an interactive dashboard application originally created in CS‑340: Client/Server Development. The original version was a Jupyter Notebook that visualized animal shelter data using static filters and hard-coded queries. In its enhanced form, the dashboard has been converted into a Flask web app and now features a real-time search capability that uses a HashMap (Python dictionary) to efficiently filter animals by name.

## **Justify the inclusion of the artifact in your ePortfolio. Why did you select this item? What specific components of the artifact showcase your skills and abilities in software development? How was the artifact improved?**

I chose this artifact because the enhancement clearly demonstrates my ability to apply efficient data structures in a real-world scenario. The original notebook relied on filtering data directly through MongoDB queries, which was functional but not optimized for performance or responsiveness when handling multiple user interactions.
In the enhanced version, I integrated a HashMap to act as a lookup table for animal names and metadata. This change drastically improved the efficiency and responsiveness of the search feature. Instead of querying the database repeatedly, the app now loads animal data into a dictionary on page load and allows for constant-time access while the user types. This demonstrates a practical application of data structure optimization in a user-focused, web-based context.

## **Did you meet the course outcomes you planned to meet with this enhancement in Module One? Do you have any updates to your outcome-coverage plans?**

Yes, this enhancement directly supports:
-	Course Outcome 3: “Design and evaluate computing solutions that solve a given problem using algorithmic principles and computer science practices.”
I applied algorithmic thinking to reduce the complexity of repeated searches and improve the scalability of the dashboard. I do not need to make any updates to the outcome-coverage plan—this enhancement met the objective as originally outlined.

## **Reflect on the process of enhancing and modifying the artifact. What did you learn as you were creating it and improving it? What challenges did you face?**

Through this enhancement, I deepened my understanding of how performance and usability are directly impacted by the choice of data structures. I learned to balance client-side responsiveness with backend efficiency, and how pre-processing data into a searchable structure can make a web application feel faster and more modern.
A major challenge was integrating the search feature without sacrificing scalability. I had to ensure that the initial dictionary build was efficient and didn’t degrade performance with large datasets. Testing this across different browsers also introduced edge cases with how the search input interacted with the dynamically rendered results. Additionally, making this feature feel seamless within a Flask application meant ensuring the search logic ran in sync with the rendering engine and the user’s expectations.
In the end, this enhancement not only improved the functionality of the dashboard but also demonstrated my ability to apply core computer science concepts like hash-based lookups in a practical, user-facing solution.
