<!-- Copy and paste the converted output. -->

<!-----
NEW: Check the "Suppress top comment" option to remove this info from the output.

Conversion time: 3.355 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β29
* Fri Oct 16 2020 13:26:13 GMT-0700 (PDT)
* Source doc: planning.md (final) template
* This document has images: check for >>>>>  gd2md-html alert:  inline image link in generated source and store images to your server. NOTE: Images in exported zip file from Google Docs may not appear in  the same order as they do in your doc. Please check the images!

----->


<p style="color: red; font-weight: bold">>>>>>  gd2md-html alert:  ERRORs: 0; WARNINGs: 0; ALERTS: 8.</p>
<ul style="color: red; font-weight: bold"><li>See top comment block for details on ERRORs and WARNINGs. <li>In the converted Markdown or HTML, search for inline alerts that start with >>>>>  gd2md-html alert:  for specific instances that need correction.</ul>

<p style="color: red; font-weight: bold">Links to alert messages:</p><a href="#gdcalert1">alert1</a>
<a href="#gdcalert2">alert2</a>
<a href="#gdcalert3">alert3</a>
<a href="#gdcalert4">alert4</a>
<a href="#gdcalert5">alert5</a>
<a href="#gdcalert6">alert6</a>
<a href="#gdcalert7">alert7</a>
<a href="#gdcalert8">alert8</a>

<p style="color: red; font-weight: bold">>>>>> PLEASE check and correct alert issues and delete this message and the inline alerts.<hr></p>



# 

<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image1.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image1.png "image_tooltip")


_Note:_ This document is meant to evolve throughout the planning phase of your project. That is, it makes sense for you to commit regularly to this file while working on the project (especially edits/additions/deletions to the _Highlights_ section). Most importantly, it is a reflection of all the planning you work you've done in the first iteration. This document will serve as a master plan between your team, your partner and your TA.


## 
**Product Details**


#### 
**Q1: What are you planning to build? **Shisei

Short (1 - 2 min' read)



*   Start with a single sentence, high-level description of the product.
*   Be clear - Describe the problem you are solving in simple terms.
*   Be concrete. For example:
    *   What are you planning to build? Is it a website, mobile app, browser extension, command-line app, etc.?
    *   When describing the problem/need, give concrete examples of common use cases.
    *   Assume your reader knows nothing about the problem domain and provide the necessary context.
*   Focus on _what_ your product does, and avoid discussing _how_ you're going to implement it. \
For example: This is not the time or the place to talk about which programming language and/or framework you are planning to use.
*   Feel free (and very much encouraged) to include useful diagrams, mock-ups and/or links.

The Toronto Transportation Services project aims to create a simple web interface so that **consultants and traffic analysts **with non-technical backgrounds can easily acquire traffic sensor data from specific areas in Toronto. To aid this, Vulcan Solutions is creating a web interface which allows for inquiries to be created by creating routes on a map, with controls similar to the user interface on the commonly used Google Maps. The query will then automatically be translated and executed on the SQL database to return CSV or GIS formatted datasets which can be used with traffic SAS applications.

Currently, the process for an inquiry requires an engineer to manually transcribe written requests to an SQL query which can then be saved and emailed back to the inquirer. The incumbent system is thus extremely labor intensive and vague requests can create operational overhead. Vulcan Solutions is creating an interface which uses a map so the inquiry is less vague and can be executed directly without distracting engineers from precious coding time. The solution provides the added benefit of tracking queries so insights can be created by the TTS team on what queries might benefit from caching. Our solution also allows queries to be continuously processed instead of waiting for an engineer to get back with the result data set. This will save time and allow for faster Transportation and Safety planning in Toronto.

Our solution is security focused as an important reason for the incumbent strategy is to ensure only authorized personnel have access to the main database. Our interface performs read-only requests to ensure data-integrity of the database is maintained and malicious users cannot use our product to modify the data. The permitted user's input will be sent as API requests, and the returning information will be displayed on UI or be outputted as certain data format, such as CSV or GIS.

UI screen for selecting a route and time range to get traffic data from:



<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image2.png "image_tooltip")
   

Full mock-ups can be found at: [https://www.figma.com/file/f83Wa2hfirGbhqqFviZTni/Toronto-Big-data?node-id=0%3A1](https://www.figma.com/file/f83Wa2hfirGbhqqFviZTni/Toronto-Big-data?node-id=0%3A1) 


#### 
**Q2: Who are your target users? **Shisei and Fernanda

Short (1 - 2 min' read max)



*   Be specific (e.g. a 'a third-year university student studying Computer Science' and not 'a student')
*   Feel free (but not obligated) to use personas. \
You can create your personas as part of this Markdown file, or add a link to an external site (for example, [Xtensio](https://xtensio.com/user-persona/)).

There are two groups of target users. Firstly, internal data requesters, both from the Toronto Big Data Innovation Team at the City of Toronto, as well from other teams at the same organization. Secondly, external consultants who use traffic data from the city for their own projects. Neither of these groups of users should be assumed to have a technical background. Therefore, there shouldn’t be technical terms such as SQL terminology, and the application should be self-service, which means that a user should be able to perform data requests on their own, without assistance from someone who has worked more closely with this data or the platform. Furthermore, an important characteristic of the users is they submit these traffic data requests in order to use the data for their consulting projects, which revolve around areas such as transportation in the city, policy intervention, monitoring of security infrastructure, collision prevention, among others. In such a way, the users’ goals are mainly to easily obtain the traffic data they need, as well specific metrics for it such as average travel time, min/max values, etc. This would allow users to gain insight into the data through an intuitive, self-service tool.



<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image3.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image3.png "image_tooltip")



#### 
**Q3: Why would your users choose your product? What are they using today to solve their problem/need? **Sajjad

Short (1 - 2 min' read max)



*   We want you to "connect the dots" for us - Why does your product (as described in your answer to Q1) fits the needs of your users (as described in your answer to Q2)?
*   Explain the benefits of your product explicitly & clearly. For example:
    *   Save users time (how much?)
    *   Allow users to discover new information (which information? And, why couldn't they discover it before?)
    *   Provide users with more accurate and/or informative data (what kind of data? Why is it useful to them?)
    *   Does this application exist in another form? If so, how does your differ and provide value to the users?
    *   How does this align with your partner's organization's values/mission/mandate?

Toronto Transportation Services plans, constructs, and manages the transportation infrastructure of the city of Toronto, and to make the most well informed decisions with those interests in mind quantitative data is imperative. However, oftentimes obtaining or presenting this data can be quite unintuitive (especially to those without a technical background), to a point where it can deter or hinder the ability to make key decisions that have an impact on the whole city. Our team’s primary goal is to provide a straightforward solution for this data acquisition problem, and consequently ensure that the users can easily access the specific data they require and allow them to focus on using the data to make decisions. More specifically in this project we will enable staff at Toronto Transportation Services and consultants to be able to self-serve their requests for existing traffic speed data and as a consequence of this data they may make the following decisions: speed limit reductions and installation of speed bumps/pedestrian crossovers. 

The application will save the time of users in multiple ways: Firstly, since there is no existing implementation (in terms of an application that automates the data fetching procedure using a UI), a **significant **amount of time and energy will be saved by removing the need for an engineer to manually transcribe SQL queries, or having to find a particular query in a massive history log of them. Secondly, as the intention is for self-serving, this eradicates the need for consultants to submit requests and wait for data, along with reducing the time spent by TSS employees in processing the requests for data. Furthermore, this application provides consistency and precision in providing the data, as it is easier for users to articulate their own needs on the given map and form UI as opposed to writing queries (can lead to problems with data types for example) or as requests (as these can sometimes be too vague). Ultimately a successful deployment of this product will allow the users to expend their focus on the implication of the data and not on it’s acquisition. 


#### 
**Q4: How will you build it? **Kavan and Sarthak

Short (1-2 min' read max)



*   What is the technology stack? Specify any and all languages, frameworks, libraries, PaaS products or tools.
*   How will you deploy the application?
*   Describe the architecture - what are the high level components or patterns you will use? Diagrams are useful here.
*   Will you be using third party applications or APIs? If so, what are they?
*   What is your testing strategy?

We plan on making use of AWS as our primary cloud service provider for both building and deploying our application. We will be using Elastic Beanstalk along with CodeBuild/CodeDeploy/CodePipeline for our CI/CD. We will mock our partner’s database with RDS for read-only data and manage our own DynamoDB for application logic. We also plan to host static content from S3 (Webpack) with Cloudfront, although we will probably temporarily serve directly from Elastic Beanstalk during early development.

Our frontend tech stack consists of React/Redux with Material UI components. Mapping components will be built atop of MapBox, with either an inhouse date selection component or react-calendar. Our backend will use Django, with boto3 (AWS python SDK) and postgres (with PostGIS and pgRouting) with the psycopg2 driver.



<p id="gdcalert4" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image4.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert5">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image4.png "image_tooltip")


On the server side, we have a basic request driven architecture. At a high level, we use read-only data from our RDS database to create Nodes and construct routes which persist in our DynamoDB. IDs pertaining to these routes are passed with additional metadata (time-windows, file format, etc) to form traffic data requests which return data in a format specified by the user. Requests that update the route in the backend or create a new route also update the view using data from the response body. Pathfinding related logic will mostly be handled by pgRouting. We also have a [Figma mockup](https://www.figma.com/file/f83Wa2hfirGbhqqFviZTni/Toronto-Big-data?node-id=0%3A1) available for the frontend.

In terms of testing, we will incorporate automated unit tests and integration tests as part of our pipeline. Our CI workflow will incorporate line and branch coverage requirements. 

A full architectural design document with in-depth details can be found [here](https://docs.google.com/document/d/1bxzayjc6_qowtGDHgSKSe90dKoDKqm1jKn1VxApd74E/edit?usp=sharing ).


#### 
**Q5: What are the user stories that make up the MVP? - **Fernanda



*   At least 5 user stories concerning the main features of the application - note that this can broken down further
*   You must follow proper user story format (as taught in lecture) As a &lt;user of the app>, I want to &lt;do something in the app> in order to &lt;accomplish some goal>
*   If you have a partner, these must be reviewed and accepted by them
*   The user stories should be written in Github and each one must have clear acceptance criteria.
1. As a consultant for the Toronto Transportation Services, I want to be able to select routes to obtain their traffic data so that I can analyze information from these routes for my consulting projects.

	Acceptance Criteria:



*   A user can select the nodes and paths between them on a map interface
*   A user can see a list of the nodes that were selected
*   A user can see the route direction (e.g. if it’s bidirectional) for the path that was selected
2. As a data requester, I want to be able to select the time range that the data should be applied to so that I only get the data I am interested in.

Acceptance Criteria:



*   A user can select the time range that the data should be applied to, especifically:
    *   Date range: the calendar range of dates from start date to end date
    *   Day(s) of week: an array of days of the week
    *   Time of Day: a time range from start hour (inclusive) to end hour (exclusive, this should be explicit)
    *   Include holidays: specify the ability to exclude holiday dates. (Optionally we may want to exclude long weekend Fridays)
3. As a traffic analyst, I want to be able to specify data values that I am interested in such as average travel time, min/max, among others, so that I don’t have unnecessary data or have to compute values separately in order to gain insight from the data I receive.

    Acceptance Criteria:

*   A user should be able to specify return values to be included with the data from the following options:
    *   Average Travel Time
    *   Standard deviation
    *   Min/Max travel time
    *   Average & Median Speed
    *   Sample count
    *   Complete coverage sample count
4. As a data requester, I want to be able to download the data results so that I can access this data at any time and use it for conducting further analysis.

Acceptance Criteria:



*   A user should be able to download the data in csv or xlsx (optional: shapefile), which would have a header and the following columns:
    *   segment name
    *   direction
    *   time period
    *   return values
5. As a data requester, I want  to save a query with a particular route and time period so that I can resubmit a request for the data in the future or modify it to make slight changes to the request (in case I need to follow up about certain details in the data).

	Acceptance Criteria:



*   When submitting a data request for a specific route, a user should be prompted to input a name to save the route
*   A user can view all the saved routes
*   A user can create a data request from a saved route and edit the route and time range for it



---



## 
**Process Details**


#### 
**Q6: What are the roles & responsibilities on the team? **

Describe the different roles on the team and the responsibilities associated with each role.



*   Roles should reflect the structure of your team and be appropriate for your project. Not necessarily one role to one team member.

List each team member and:



*   A description of their role(s) and responsibilities including the components they'll work on and non-software related work
*   3 technical strengths and weaknesses each (e.g. languages, frameworks, libraries, development methodologies, etc.)

A successful team needs to have a diverse array of talents and strengths lending to different roles and responsibilities. We agreed before defining and assigning particular roles that the role must be necessary and beneficial for the structure of the team, that it should elevate our combined and individual strengths, and also allow us to hold each other accountable. Therefore, for the purposes of this project we chose to have the following roles: Project Manager, Architecture Manager, Pipeline Engineer, Document Specialist, and Developer positions. Below is an overview of each position and the software/non-software related work for the positions.

<span style="text-decoration:underline;">Roles Overview:</span>

Project Manager: The project manager is responsible for planning, organizing, and directing the completion of the project, this position is needed to provide our group with a direction and ensure everyone knows what’s expected of them. 

Individual(s): Fernanda

Architecture Manager: The Architecture manager is responsible for designing the general architecture of the project and making executive decisions on frameworks and libraries we use for different parts of our product. They must research all possible solutions and pitch the ones that they find are most suitable for our product.

Individual(s): Kavan

Pipeline Manager: The pipelines engineer is responsible for the communication layer between all the different components of the application. They must design the API and understand the integration of all different frameworks. Since there are a lot of different frameworks and subgroups in the development phase, this individual will oversee the process for putting everything together into a polished product and answering questions about any component of the application.

Individual(s): Sarthak

Document Specialist: The document specialist is responsible for ensuring high quality of documentation (whether it’s code or written reports), and also documenting key details and insights that arise in partner meetings. This individual can make suggestions to different managers based on details from partner meetings and class requirements. . 

Individual(s): Sajjad

UI/UX Designer: The UI/UX Designers are responsible for creating mockups and wireframes for the application that clearly illustrate how sites function and look like for mobile and desktop versions. These individuals ensure the application is visually pleasing and can call for adjustments to the frontend in the development phase. The designs made have been linked in Q1.

Individual(s): Sherman, Shisei

Full Stack Developer & QA Testing: As students of CSC301, we are all expected to write quality code and tests for the frontend and backend of the application. Thereby, we are all Full Stack Developers that are expected to test our code, however individuals with strengths in particular areas will prioritize tasks in their area of expertise. Individuals with a focus in frontend will mainly work on languages/frameworks such as: React, Redux, and Mapbox. Individuals with focus in the backend will mainly work on languages/frameworks such as Python: Django, Javascript: Node, AWS, and PostgreSQL. For more information about particular work involved in each component see Q4.

Individual(s): Everyone

<span style="text-decoration:underline;">Team Skill Set & Roles Breakdown:</span>

Here is a breakdown of the strengths and weaknesses of the individuals that comprise the Vulcan Solutions group. This should clarify the rationale behind assigning certain roles.


#### **Sajjad:**


#### Strengths



*   Experienced with backend development, specifically using languages such as Python, JavaScript, and PostgreSQL.
*   Exposure and understanding of industry grade software design and practices.
*   Clear, detail oriented methodical approach to problem solving.
    *   Motivated to ensure that all required details are met appropriately.
    *   Can clearly communicate ideas and intricacies.


#### Weaknesses:** **



*   Limited Experience working in an AGILE environment.
*   Limited Exposure to frontend technologies (React/Redux).
*   Unfamiliar with testing infrastructures/frameworks and CI/CD. 

Roles: Document Specialist, Full Stack Engineer: focus in backend.


#### **Sarthak**:

Strengths



*   Strong Understanding of Databases and architectural concerns
*   Composing Case studies and Market Analysis documents, and Pitch Decks
*   Experience with Parallel programming using python libraries

Weaknesses



*   Limited Front-End Experience
*   Limited Experience with React/Redux which is a core technology of product
*   Limited Experience with QA/testing suites


#### Roles: Pipeline Manager, Full Stack Developer: focus in backend, business perspective. 


#### **Fernanda**

Strengths

	



*   Getting at the bottom of a problem to really address people’s needs through design thinking and human-centered design.
*   Breaking down problems. This can be in coding or for breaking down product requirements.
*   Prioritization of tasks, creating a product roadmap

Weaknesses



*   Limited knowledge on general software architecture and the different systems needed for a software application
*   Need to learn more about systems design from the software component perspective i.e. uml, class diagrams
*   Limited exposure to prototyping and graphic design 

Roles: Project manager, Full Stack Developer: General.


#### **Kavan**

Strengths



*   Pipelines, Systems, and Software Design
*   Extensive backend experience designing, prototyping, and building large scalable solutions with native AWS
*   Rapid onboarding/development

Weaknesses



*   Limited front end experience
*   Often overshoot goals when planning
*   Tendency to overengineer projects

Roles: Architecture Manager, Full Stack Developer: focus in backend.


#### **Sherman**

Strengths



1. React 
    1. Material UI 
    2. Grommet
    3.  Styled components 
2. Wireframes and Mockups : Adobe XD, Figma
3. Familiarity with Tailwind css 

Weaknesses



1. Backend Development 
2. Limited exposure to setting up backend architecture 
3. Limited experience with CI/CD set up.


#### Roles: UI/UX Designer, Full Stack Developer: focus in frontend.


#### **Shisei **

Strengths



*   Familiarity with Rect, Redux, Redux-Saga, and React Native for Web.
*   Ability to solve problems from both an engineering and business perspective.
*   Familiarity with infrastructure engineering with AWS and GCP. 

Weaknesses



*   Limited experience with backend development.
*   Understand how to use Figma, but limited experience with designing UI/UX
*   Limited experience with API development. 

Roles: UI/UX Designer, Full Stack developer: focus in frontend. 


#### 
**Q7: What operational events will you have as a team? **Sarthak

Our team is planning on having weekly or bi-weekly sprints (depending on workload of current sprint). Sprints will be constructed by segmenting MVP tasks and will be modified to be in line with deliverable expectations. We will be developing in an AGILE environment using Trello boards to assign tasks. Currently our task board is set up to have the following lists: Todo, In Progress, Completed, Backlog. The first 3 categories are straightforward, the Backlog board is used to highlight any tickets which are stopping other dev teams from completing their assignments. This board is thus critical to stopping bottlenecks. The ticketing system is explained below:



1. Tickets are assigned by the Project Manager who will fill in basic descriptions (overarching and open-ended) and assign an importance score representing the precedence of this task relative to other tasks assigned to the team/developer.
2. The Ticket will then go to the developer who will fill in specifics and assign a difficulty score to represent the expected amount of coding-hours.
3. The ticket will be evaluated by Pipeline Engineer to ensure the interface integrates to other teams and Architecture Engineer for compliance with current tech/hardware stack. The importance and coding-hour scores will also be evaluated here. If the task is hardware and API independent, then this step will be skipped and scores will be evaluated by Project Manager.

Weekly meetings at the start of every week have been set-up to discuss the previous week’s accomplishments, backlogs etc. and understand expectations for this week’s work. We have set-up recurring meetings via Zoom for Thursdays at 5pm which is managed via Google Calendars to remind everyone of the ongoing commitment. In addition, on Wednesdays we have a slack channel check-in which will update everyone about each team’s progress. This will ensure responsibility and clear communication about expectations. We will have retros at the end of every sprint cycle to reorient any critical errors in our operations.

During our meeting with our project partner, we discussed the current solution used by TTS (which is essentially manually structuring queries and sending log files). We also discussed preferences in tech stack and authentication/availability of service requirements. During this meeting we got a clear understanding of what our product needs to include and we were added to a group github the partner created for us. This process helped us assign tasks for the second meeting (namely architectural diagram, creation of prototype v1, creation of user stories)

Our second meeting included pitching our prototyped app to the partner and gaining feedback on the UI/UX experience. To show our prototype, we ran through user stories to ensure all functionalities were based on concrete use cases and the partner could easily explain if any feature was extraneous or if a critical feature was missing. From here we took notes on improvements to make for our application (namely our options for map path generation were too limited). We also instructed the partner to send us a comprehensive list of queries made by partners so that we could create a more specific UI experience. During this meeting, we also pitched our Tech/Hardware architecture to ensure the framework was compliant with any TTS needs. We convinced the partner to switch from a Flask native network to Django to add stability, security, and scalability to our application.

We will be meeting our partner before and after every sprint cycle to update the partner on our progress and let him know about next steps. Meeting minutes are maintained in the below document and the document also contains minutes for the first 2 meetings.

Link to Meeting Minutes Document: 

[https://docs.google.com/document/d/1fhNuVtA0MuVoDgApVCfUXQJ54Ei72pB9AU3sGjZPtao/edit?usp=sharing](https://docs.google.com/document/d/1fhNuVtA0MuVoDgApVCfUXQJ54Ei72pB9AU3sGjZPtao/edit?usp=sharing) 


#### 
**Q8: What artifacts will you use to self-organize? **Sarthak

List/describe the artifacts you will produce in order to organize your team.



*   Artifacts can be To-Do lists, Task boards, schedule(s), meeting minutes, etc.
*   We want to understand:
    *   How do you keep track of what needs to get done?
    *   How do you prioritize tasks?
    *   How do tasks get assigned to team members?
    *   How do you determine the status of work from inception to completion?

We will be using Slack as the main form of communication and have exchanged phone numbers for “critical” emergencies. We have established members are required to check Slack at least twice a day once in the morning, once in the evening). This allows us to maintain a maximum of 12 hours “to-response” time.

Tasks are designated via Trello by the Project Manager and assigned to developers by skill-set and our internal segmentation of teams. A more complete explanation of the use of Trello is available under Q7 as the tasking system is directly implemented into our AGILE operational environment. The ticketing system consists of 2 scores: the precedence score allows developers to understand which ticket to focus on first, while the coding hours score allows the PM to have a clear understanding of when to expect the ticket to be completed. To understand the status of tasks, we have 4 lists created on our board tracking to-dos, in progress tickets, completed tickets, and tickets causing backlogs/development bottlenecks. In addition, we have meetly check-ins to ensure developers work on the correct tasks during the week and a middle-of-the-week check-in implements responsibility and allows for a syncing of expectations. Meetings take place at the start of every week and take place over Zoom. The link is distributed via Google Calendar and the shared calendar ensures all developer’s are notified of company meetings/events. Meeting-minutes duty is assigned on a rotating schedule for both partner meetings and weekly Sprint meetings.

Slack Channels Setup:



<p id="gdcalert5" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image5.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert6">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image5.png "image_tooltip")


Trello Board Setup:



<p id="gdcalert6" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image6.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert7">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image6.png "image_tooltip")



#### 
**Q9: What are the rules regarding how your team works?**

Describe your team's working culture.

Communications: Sajjad



*   What is the expected frequency? What methods/channels are appropriate?
*   If you have a partner project, what is your process (in detail) for communicating with your partner?

We believe that communication is the cornerstone to success in this group project. Productive communication enables our team to tackle issues with ease, understand our roles/responsibilities, and most importantly allows us all to be on the same page. As such, it’s important with so many different roles and groups of skills, that there is a clear path of communication and it is both effective and efficient. This is why we chose our primary mode of communication to be Slack. Slack’s channels allow us to compartmentalize the development process, this ensures that people working together on subprocesses can stay updated with each other, while others don’t have to be active on channels that don’t necessarily involve them. Furthermore, Slack’s integration with other applications we are using as part of our process (Google Calendar, Trello, Zoom, etc.) make it an obvious choice at the base of our communications. 

The protocol on our communications is as follows: Everyone is expected to check Slack at least twice a day, notifications should be turned on for mentions, Zoom meetings at the beginning/end of sprint cycles, and every Wednesday we will have a Slack stand up to discuss progress and issues. These rules ensure that everybody is aware of the status/progress of the project at all times, if we are needed individually or collectively we are available within a reasonable timeframe and allows us to stay on top of our work by holding each other accountable. We have also shared our phone numbers as an insurance policy, so if there is an urgent matter we can communicate with the individual more directly. 

In a partner project such as ours, communication with the partner is vital to a successful delivery of their envisioned product. The process of communication with the partner is as follows: Adding the partner to our Slack channel, meeting with the partner at least once every two week (using the partners chosen platform: Cisco’s Webex), a singular point of reference for emails/questions/concerns (the project manager). This procedure ensures that the partner is constantly involved in the project, allows them to give input or suggest improvements as per their requirements, and there is a consistent/clear path of communication with them.

Meetings: Sajjad



*   How are people held accountable for attending meetings, completing action items? Is there a moderator or process?

Our meeting schedule and timings are governed by common availability throughout the week. We use [www.when2meet.com](www.when2meet.com) (see image below) as a tool to determine individual availabilities, and then choose the most accommodating time for our Zoom meetings. This way, prior to the meetings people have knowingly committed their chosen times and are accountable for showing up. However, in the event that someone does miss a meeting or cannot find availability with the rest of the group members, they must inform the Project Manager (who plays a moderator role) at least 24 hours prior to the meeting (meetings are set at least 48 hours ahead of time - sprint cycle meetings have an agreed upon fixed time in the week) so there are no surprise absentees. As upper year computer science students we all understand the stress and workload (especially in the current climate) that everyone is subjected to, and are therefore considerate when individuals cannot make meetings. We expect the individual who has missed the meeting to show initiative in getting caught up and are all willing to help them do so; however by default this responsibility falls upon the project manager. Similarly, the project manager organizes the meetings, guides the agenda of the meeting and keeps track of who’s missing or has fallen behind. In general, the meetings will be goal and result oriented, where we discuss our progress and strategies to maximise our performance. 

<span style="text-decoration:underline;">Example when2meet: </span>



<p id="gdcalert7" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image7.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert8">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image7.png "image_tooltip")


Conflict Resolution: Kavan



*   List at least three team scenarios/conflicts you discussed in lecture and how you decided you will resolve them. Indecisions? Non-responsive team members? Any other scenarios you can think of?
1. Scenario: Not everyone is on the same page.
    1. A consensus is good assuming that everyone understands the risks of going forward with a decision and has put in their two cents. If a situation arises where this becomes an issue, we will conduct round table discussions at critical project junctions where everyone has a chance to speak their mind.
1. Scenario: Someone is not meeting their deadlines.
    2. We will discuss performance during our sprint retros and what in particular went wrong, and correct it for the next sprint. In most scenarios we expect to just reweight/reassign tasks and move on. For example, if we underestimated the difficulty of a particular story, we would just assign more points or get another team member more familiar with the domain to assist. If the issue comes down to individual contribution, we will have a sit down discussion to raise concerns and or discuss solutions.
2. Scenario: One person makes decisions on behalf of everyone without much consultation
    3. If this occurs, we will create a review process for these decisions moving forward, where individuals need to consult at least one other member on the team. This other member will also be accountable in the event that other members are blindsided at the next sprint/partner meeting.



---



### 
**Highlights - **Sajjad

Specify 3 - 5 key decisions and/or insights that came up during your meetings and/or collaborative process.



*   Short (5 min' read max)
*   Decisions can be related to the product and/or the team process.
    *   Mention which alternatives you were considering.
    *   Present the arguments for each alternative.
    *   Explain why the option you decided on makes the most sense for your team/product/users.
*   Essentially, we want to understand how (and why) you ended up with your current product and process plan.
*   This section is useful for important information regarding your decision making process that may not necessarily fit in other sections.

Through the planning phase of this project, there were a few interesting insights and decisions that came up to lead to our current product and plan. The most notable highlights were: the team’s eagerness to build an impactful product, how we utilized our previous experiences to build up our technical/communication stack, and finally the diverse array of analytics we used to make the best technological/design decisions and how we used them to convince the partner of certain features. 

The Vulcan group members chose the TSS partner project as an almost unanimous number one option for this group assignment (See selections in image below). Upon our group discussion on the topic it was revealed that we all had similar motives for choosing this project as such a preferential choice; the impact the project would have. We all understand the potential public safety implication of this application, and we would all love to see The City of Toronto benefit from us aiding decision makers by providing them easier and faster access to data. This is why we have all invested a significant amount of time in the planning phases of this project and why we’ve been so thorough in our mockups and technical considerations. We believe ultimately this will allow our product to provide a high quality of performance, since our utmost priority when making choices has been with the needs of the users. 

Although we are all relatively young professionals in the software industry, we were able to apply our experiences in choosing helpful infrastructures for our tech stack and communication with confidence. With every member of the team having prior experience, in groups and companies of all sizes we were able to apply our combined experience to build a system that worked well for everybody. For example, we chose to use Slack as our communication channel since we all understand it utility for group projects, we chose React for our frontend since our most experienced frontend developers were most accustom to the framework, and we chose AWS as part of our backend many of us are comfortable with its features (with one of our members even interning at AWS). Our experiences with these frameworks means we understand how to use them and can apply them in this project with little difficulty. 

Furthermore when facing contentious decisions we took many different factors into account. At times we even managed to convince the partner to change their mind on some specific structural decisions due to the reasons we provided. For example, when faced with the choice of using Flask or Django as our main backend framework, we understood the suitability of Flask for small scale applications, but due to the scalability of Django and the larger variety of support with other frameworks we chose Django, and in explaining these benefits to the partner they were also happy with Django. Similarly, we convinced the partner to have user authentication in the application by explaining the security, concurrency, and caching benefits it can provide. 

<span style="text-decoration:underline;">Team Selections for Toronto Transportation Services Partner Project</span>

1 Indicates that the project is the number 1 choice. 



<p id="gdcalert8" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image8.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert9">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image8.png "image_tooltip")


**<span style="text-decoration:underline;"> \
</span>**
