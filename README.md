# Project Experience: Automated Discount Data Collection and Analysis

## Python
Utilizing the Python programming language, I employed HTTP requests to access the Spark website's Ajax-powered interface. Extracting data from the responses, I gathered information about various phone models. Subsequently, I used the Selenium module to simulate user interactions, accessing detailed information pages for each phone. This allowed me to retrieve discount information, which I recorded in both an Excel sheet and a MySQL database simultaneously.

## My SQL
Building upon various models and specific information available on the Spark website, I populated the "phones" table in the "oppo" database. This included daily promotional activities for each model, encompassing discounts and giveaways, stored in the "sparksale" table. A one-to-many relationship was established between these tables to efficiently manage the data.
[![mysql1.png](https://i.postimg.cc/RZQL3Cmk/mysql1.png)](https://postimg.cc/TK1DF6p0)

## Jenkins
To achieve continuous integration, I connected my Python program, GitHub, and Jenkins. I scheduled daily executions and sent newly generated discount information Excel sheets via email. The process involves setting up a GitHub repository, installing Jenkins, configuring a Jenkins job, scheduling builds, enabling email notifications, and optionally using GitHub webhooks for automation.
[![jenkins2.png](https://i.postimg.cc/2jVGHfdW/jenkins2.png)](https://postimg.cc/QVZctwyN)
[![jenkins1.png](https://i.postimg.cc/jjM5nPmp/jenkins1.png)](https://postimg.cc/LqZRrYHD)

## Power BI
Given variations in discounts over time, I harnessed Power BI's capabilities to visualize the data sourced from MySQL. This enabled direct analysis of discount changes and trends through filtered and grouped data. Daily refreshing from MySQL facilitated up-to-date insights.
[![powerbi1.png](https://i.postimg.cc/13ZK5nk0/powerbi1.png)](https://postimg.cc/1fJFvt54)
[![powerbi2.png](https://i.postimg.cc/1zmcDx5f/powerbi2.png)](https://postimg.cc/cvznNb3S)
[![powerbi3.png](https://i.postimg.cc/DyGgTdMy/powerbi3.png)](https://postimg.cc/7fx7174p)

## Todo
- **Data Visualization and Reporting:** Creating diverse charts and dashboards to visually represent discount trends for quick insights and decision-making.
- **Multi-channel Data Collection:** Ensuring automated processes can accommodate data from new channels for consistent and accurate analysis.
- **Data Analysis and Modeling:** Exploring advanced techniques like predictive models and clustering for deeper insights.
- **User Experience Optimization:** Enhancing user interface for seamless data access and interaction.

## Conclusion
Through the Automated Discount Data Collection and Analysis project, I showcased my proficiency in Python programming, web automation using Selenium, MySQL database management, and Power BI visualization. This comprehensive project not only reinforced my technical skills but also highlighted my commitment to innovation, efficiency, and data-driven decision-making.
