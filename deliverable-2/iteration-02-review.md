![alt_text](./images/image1.png)


## **Review & Retrospect**



*   When: Thursday November 19th 5:00:00 EST
*   Where: Zoom

## Process - Reflection


####  Q1. Decisions that turned out well 

##### Team member roles

Having team members focusing on the different areas of the project was key to balance and complement our team efforts in every direction. We had team members focused on UX/UI design and front-end, as well as a team dedicated to the back-end development and architecture. Furthermore, we had team members focused on project management from different perspectives: end-user product, architecture/engineering, and course deliverables. In such a way, each of us knew our responsibilities and what we should be working on, as well as whom to contact for any questions or collaboration needed. Together, we combined our efforts to develop the first iteration of our traffic data request tool for our partner, developing both our individual and also our teamwork skills.


##### Team communication and workflow

Closely related to the previous point was the communication and workflow aspect of our teamwork. Having clear team member roles and areas of focus, allowed us to have a clear communication process. For example, we created slack channels to discuss specific areas of the project such as back-end and front-end. Furthermore, people were proactive and responsive in these channels, allowing for a smooth communication and collaboration within our team. Part of this was also thanks to the process guidelines we had established earlier for phase 1, where we agreed on checking/replying on slack at least 2 times a day. 

Furthermore, in terms of our team workflow, having a project management board (trello board) was very helpful for our team. Being able to keep track of the tasks we are working on, and visualize the status of each one, helped us to track our individual tasks, the tasks related to ours, and overall see how all of our team’s tasks come together. This board worked as a point of reference for our sprints and we certainly want to continue to use it. However, we do want to improve some ways in which we are using it going forward, to further take advantage of this tool. We discuss this in more detail in the sections below.


##### Having an MVP

At the beginning of our work for deliverable 2, our team focused on scoping out an MVP out of the general set of requirements for our partner’s solution. During our weekly meetings with the partner, we gained insight into what are the key functionalities, in their simplest form, that would provide our partner’s team with the user value they are looking for, as early as possible in our development cycles. This is how we decided to focus on the ability to request traffic data for a single segment and a single period of time, and to build an interactive map interface to do so. Even though it is a realistic use case that a consultant may want to request data for multiple segments or multiple periods of time, we found that it doesn’t necessarily require the application to handle complex requests from the beginning, since the data could be obtained simply by submitting multiple traffic data requests. So, for our MVP we decided it was a good first step to restrict the use to single segments and time periods and iteratively work our way towards more complex requests, which will then provide more convenience to the user.

Having established the focus for our mvp, we created another set of mockups from our starting ones, and adapted it to have the specific components of our mvp, and to make some small changes from the feedback we got from our partner. This allowed for a clear communication with our partner, and allowed them to visualize what the first iteration of our product would look like. Once we had these mockups ready, it helped our team by boosting front-end development to be mostly focused on implementation since we were clear on what the ux/ui design and acceptance criteria was for each component on the interface. Finally, having use cases and acceptance criteria for our MVP, also helped back-end development and overall development integration, by providing clear, realistic guidelines and test cases to build our application on ie. examples of traffic data requests and expected outputs from users when they used the platform.


##### API, back-end design and documents for reference

Finally, another decision that turned out well was having come up with an API and architecture design early on, and having documents for our team members to refer to it. These designs provided a good foundation on which back-end components we would need and how they would interact with each other. They allowed us to know which tools to set up (e.g. databases, django server, and services in AWS, etc) and to know the approach that we would use to connect these. Furthermore, having documents with this information helped with our team communication since it was a good source of reference to understand how the integration between the front-end and the back-end would work, and to have a concrete API (expected requests and responses) for our implementation of the back-end.


####  Q2. Decisions that did not turn out as well as we hoped 


##### Trello

Our team chose to use Trello to implement a ‘Kanban’ workflow to manage tasks across sprint cycles. We used Trello to implement a Kanban workflow, which enabled us to create and delegate tasks and elucidated the project’s progress and maintained accountability within the team. During our sprint, however, the Kanban board was not sufficiently updated to reflect the life cycle of the project. For instance, a few completed tasks and cards were not put in the “completed column” until much later. Additionally, a few unforeseen ad-hoc tasks were not recorded on Trello.


##### The life cycle of a sprint

Our initial assigned user stories were small and modular. We expected team members to plough through them. As a result, we decided to weekly sprints to delegate new user stories. However, because of other academic commitments, assigned user stories could not be tackled immediately. As a result, user stories that would take one to three days were generally completed in seven to nine days. A few sprint meetings felt too rushed because user stories from the last sprint were still under development.


##### Mid sprint check-ins 

We also had mid-week sprint check-ins to maintain further accountability during the sprint cycle and decrease the tendency to complete user stories right before the sprint meeting. However, the check-ins felt too rushed. There was generally not much to update on most team members only made significant progress on a user story after the weekly check-ins. Moreover, not all team members updated their mid-sprint check-ins.


#### Q3. Planned changes


##### Sprint cycle

We want to make two important changes to our sprint cycles going forward. 

First, we want these cycles to be biweekly instead of weekly. Our sprint cycles are currently composed of: 



*   Sprint grooming
*   Sprint planning
*   Midweek sprint check in

We want to change the duration of the sprint cycles to be two weeks instead of one week, but we would keep the same components/events throughout our sprint. We think this would allow for more time to make significant progress on our development and a more efficient planning for it as a team.

During our sprint groomings, our project managers and product manager will get together to plan what our team will work on, break this down into user stories/tasks, and prioritize these based on our partner’s input and any dependencies between tasks.

During our spring planning, our entire team will get together and share updates, go through the list of tasks that we’ll be working on during the upcoming sprint and clarify any doubts, as well as delegate these tasks. The idea for this meeting is to get a high level understanding of what our entire team will work on, and then we will complement this meeting with more in-depth technical discussions about how we’ll do it - this is part of our second change which is further described below in this section.

Finally, even though our sprint cycles will last two weeks, we want to maintain weekly slack check ins to encourage communication and accountability within our team. It won’t be expected that  there are major updates every time, but just that there are updates by all team members, so that we know that we are making progress, spot any blockers, and encourage teamwork throughout our sprint.

The second change we want to make to our sprint cycle is the addition of weekly technical discussions between the front-end team and the back-end team, respectively.

Often, the front-end/back-end tasks are related to each other or fall under a larger user story. This requires that there is communication between people working on the tasks in order to come up with a general approach, consider any important details for these tasks, make any architecture decisions, and to better coordinate on who’ll work on what.

This is hard to do in the same meeting as our weekly sprint planning, yet it is quite essential to our development process. Therefore, we have decided to have separate calls for these technical discussions that will explore exactly how the tasks are going to be done and to improve our collaboration while working on these related tasks. 


##### Task management

The other process-related changes we want to make are in the area of task management. We certainly feel that using a project management board helped us to keep track of tasks and their progress, but we found some limitations while trying to take full advantage of this tool in the past sprint cycles. Based on this, we have decided to make a few improvements. First, we will focus on creating separate trello tasks / cards whenever we want to break down stories instead of creating nested checklists within a task for this.

This is particularly helpful to more easily  keep track  of each subtask and to see who is working on what. Currently, with the free version of trello, one of the limitations we had is that we couldn’t assign items in checklists to different people, which made it hard to coordinate within our team members. 

Another improvement we want to make is to more accurately capture our work on our trello board. It is possible that when someone starts working on a task, other things are needed that weren’t initially contemplated. For this, we want to ensure that we capture our work on our project board by creating trello tasks if they come up, especially if they are of significant scope and if it would be helpful for our team to have visibility on them.

Finally, another improvement we want to focus on is to update the progress of our tasks on trello. Mainly, when we’ve started working on a task, we would make sure we move it to “in progress” and when we’ve finished working on a task, we would move it to “completed”. This would allow our trello board to be an accurate reflection of our work and to enhance our team’s coordination of tasks and overall communication.


## Product - Review


#### Q4. How was your product Demo

We had our product demo with our partner on Thursday November 19th at 1 PM EST. 

In order to prepare for the demo we ensured that we would be able to visually demonstrate the features we implemented for this deliverable. This involved creating temporary solutions for some things such as deleting a node. Since we did not implement a delete button into the markers on the map we showed the partner that nodes could be deleted by hardcoding the node that needed to be deleted and showing how the application reacts to such a change. We further showed requests implemented on Postman since the front and backend integration was not complete. Our preparation for the demo also involved assigning roles for who would demo the different features and who would answer questions regarding specific details if the partner had any. 

We managed to demo everything we wanted and more for this deliverable. As mentioned the frontend and backend weren’t completely integrated so we were able to show the backend functionality through Postman. The partner was able to see the map, the side menu for query specifics, the module to specify desired return values, creation/deletion/modification of routes, and a returned csv of their desired data. We were able to demonstrate almost all of our backend functionality for the application as a whole, which was more than we expected for this deliverable.

The partner was delighted by the interface and progress we made for the application. He was pleasantly surprised by the design of the interface and all the route related functionality was as he was expecting it to be. The only change request was made when we demonstrated a sample return csv. He wanted us to use a different method of data aggregation for the final output, more specifically, he wanted the output mean speed values to be a harmonic mean as opposed to just averaging over the selected route.

On the whole, the demo was quite successful. If there was something we needed to improve upon and learn for the next time it would be to better plan the order in which we demonstrate functionality to the partner. Due to the nature of our relationship with the partner, we were quite casual about presenting and therefore the presentation might have lacked a bit of cohesion. Next time we intend to have a clear order and an exhaustive list of features we want to demo so there is better clarity. 
