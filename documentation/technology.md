# Technology Plan for IWBT
> Target State Architecture for this project is detailed in this doc, along
> with what we'll need to do to get there.

This project began as a pipe-dream, cooked up on a long drive in the 
Adirondacks during the Summer of 2015, on our way back from running the 
Back then, Rob and I didn't know shit 
about technology or building a professional project, so this document never 
really got written. Since then, I've built a ton of web-tools, and learned 
front-end and back-end design as well as what works and what doesn't. It's 
finally time to take another stab at this, and (although it is subject to 
massive revision as we go, this is my revised technology plan)
-- Exley McCormick, May 27 2017

# Key Philosophical Tenets
This is just some crap i jotted down. Draft this up into something tighter.
    
    Keep the real goal on the page with the tech goal! This is about providing 
    quality data and information to people who like the outdoors. Everything 
    else is just a means of doing that.
    
    Embrace Flexibility and Modern Architecture  
    Because this is a learning and practice exercise as much as anything else,
    everything about this should be done with the intent of making it flexible, 
    scalable, software that is professional from top to bottom.  
    
    Documentation, Replicability, and Testing are Mandatory  
    Projects have a tendency to grow organically in the design / prototyping 
    phase, which means things get added piecemeal and ad-hoc. This typically 
    leads to a single version of a project that is custom-tailored to a 
    specific system, and moving it around between hosts or changing design 
    decisions is a pain in the ass. Replacing this should be effectively 
    push button.  
    
    Everything should be replaceable. If the front end becomes totally reliant 
    on the API, then the back end can be altered / modernized without 
    affecting the front-end, so long as the API remains fixed, and vice-versa. 

# Technical Inventory
Layout of the stack, and major design decisions that go with it. Where are we 
and where do we want to go?


| Component      | Current State       | Target State           | Timeline        | Skills to Learn  |
| -------------- | ------------------- | ---------------------- | --------------- | ---------------- |
| Deployment     | Flask dev-server    | Docker / AWS           | After the rest  | Docker / AWS     |
| Back-End       | MySQL on Alembic    | Postgres on Alembic    | After schema    | N/A              |
| Web Framework  | Flask / Jinja / API | Flask API + Angular    | After data      | Angular          |
| API            | Flask (just for CRUD) | Flask for everything | In progress     | N/A              |
| Front End      | Jinja + swal + dataTables | Angular | Next | Angular | 

  1. Docker-deployment is the goal, but we're currently deploying with Flask 
  dev server. 
  2. Back-end is currently on MySQL, but 


### Other thoughts and comments
  * `setup.py` doesn't have to be for installing to runtime -- does docker make
  this obsolete?
  * should we focus on dockerizing it, and really commit to that deployment? 
  * seems like that's what we're moving towards at work.