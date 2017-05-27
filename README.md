# IWBT: I Went Boating Today
### Rob Hurst and Exley McCormick<br>
#### Summer 2015

I Went Boating Today (IWBT) is a mobile solution to the information problems 
arising in the whitewater community. In the first round of design and 
development, the features we hope to implement are:  

1. Easily accessable realtime flow data
2. Google Maps integration for improved navigation to put ins and take outs.
3. Paddling Logs

I went boating today is designed as a mobile app front-end with web and back-
end support provided for various features. Most of the real work will be done 
back-end and the app itself should just be a gui/wrapper for the back-end 
support.


There are two ways to think about the breakout of the infrastructure design: 
Categorized by feature, and categorized by technology stack. We will first 
break out the project by features / needs, and then break out the 
implementation of those features as databases, back-end support infrastructure,
 web services, and mobile apps.

### Feature / Need Goals for First Version
___
For more information on these topics, see our 
[Features Design Doc](./documentation/features.md), 
and our [Running ToDo List](./documentation/todo.md).  

**Section F.1: Easily Access realtime flow data**  
Flow data is available from the 
[USGS Website]('http://waterservices.usgs.gov/'). 
Their API returns river gauge information in XML format. We have written a 
simple XML parser to pull relevant data from the return string. Parser runs on 
the back-end to keep the database continuously updated, and the front end 
simply references the up-to-date tables.  

**Part 2: Google Maps Layovers**  
Gonna need some professional help on this part. GIS layovers, Google Maps API, 
getting Lat/Long data for access and rapids, mapping it to RiverId and RapidId,
 etc.  
 
**Part 3: Paddling Log**  
So far, we have the basic idea mapped out as a database, but we need to get 
some help here for how to make it easy to customize your own fields in this 
table. Basically, we need to be able to add custom user paddling logs for 
people like 'u/rob' who like to have lots of creative control.  

###Technology Stack and Services
___
For more information on these topics, see our 
[Technology Design Doc](./documentation/technology.md)  

**Section T.1: Hosting**  
Initially starting out, hosting will be localhost on my linux box. As it starts
 to get bigger, I plan to move it to AWS Cloud Servers.  

**Section T.2: Database Infrastructure**  
Unless someone convinces me otherwise, we'll probably be using MySQL for the 
databases, because it's free, open-source, and I already know how to use it. 
If we are trying to build flexible paddling logs, perhaps we'll want to 
incorporate some type of document-database as well, but I know virtually 
nothing about this, and would probably just create some ugly SQL workaround 
in the first version rather than trying to learn NoSQL.   

**Section T.3: Back-End Support Software**  
This segment of the technology stack encompasses the software and shell 
scripting used to keep the databases updated. This will include parsers for 
updating data from USGS or NOAA or whatever, cron scripts to run the updates. 
Probably makes sense to have "always on" type software that manages itself 
rather than integrating tons of shell scripts and python programs.  

**Section T.4: Web Services**  
More on this later.

**Section T.5: Mobile Apps**  
Need to make mobile apps for Android (Java) and iPhone (Objective C) that 
serve as UX/UI for the entire stack. These will need to interact with several 
crucial parts of the phone / OS, including GPS, GoogleMaps, [ANYTHING ELSE?]. 
This is the section where the UX / UI decisions will actually be implemented 
(Nobody sees the database and the back-end infrastructure).

