-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2015-07-19 15:25:55.93


-- Set Database
USE Iwbt;


-- tables
-- Table Gauges
CREATE TABLE Gauges (
    GaugeId int    NOT NULL ,
    RiverId int    NULL ,
    TimeStamp datetime    NOT NULL ,
    Flow int    NULL ,
    Level float    NULL ,
    CONSTRAINT Gauges_pk PRIMARY KEY (GaugeId,TimeStamp)
);

-- Table PaddleLog
CREATE TABLE PaddleLog (
    TripId int    NOT NULL ,
    UserId int    NOT NULL ,
    RiverId int    NOT NULL ,
    CreateDate date    NOT NULL ,
    PaddlingDate date    NOT NULL ,
    PutOnTime time    NOT NULL ,
    SwimCount int    NOT NULL ,
    SwimComments varchar(512)    NOT NULL ,
    CONSTRAINT PaddleLog_pk PRIMARY KEY (TripId)
);

-- Table Rapids
CREATE TABLE Rapids (
    RapidId int    NOT NULL ,
    RapidName varchar(64)    NOT NULL ,
    RiverId int    NOT NULL ,
    Grade varchar(8)    NOT NULL ,
    MileMarker float    NULL ,
    Gps varchar(32)    NULL ,
    Rivers_RiverId int    NOT NULL ,
    CONSTRAINT Rapids_pk PRIMARY KEY (RapidId)
);

-- Table Rivers
CREATE TABLE Rivers (
    RiverId int    NOT NULL ,
    RiverName varchar(64)    NOT NULL ,
    Section varchar(64)    NOT NULL ,
    Grade float(8)    NOT NULL ,
    MinFlow int    NULL ,
    MaxFlow int    NULL ,
    GaugeId int    NULL ,
    CONSTRAINT Rivers_pk PRIMARY KEY (RiverId)
);

-- Table TripUserMap
CREATE TABLE TripUserMap (
    TripId int    NOT NULL ,
    UserId int    NOT NULL ,
    CONSTRAINT TripUserMap_pk PRIMARY KEY (TripId)
);

-- Table Users
CREATE TABLE Users (
    UserId int    NOT NULL ,
    UserName varchar(64)    NOT NULL ,
    CreationDate date    NOT NULL ,
    TripUserMap_TripId int    NOT NULL ,
    CONSTRAINT Users_pk PRIMARY KEY (UserId)
);





-- foreign keys
-- Reference:  PaddleLog_TripUserMap (table: TripUserMap)


ALTER TABLE TripUserMap ADD CONSTRAINT PaddleLog_TripUserMap FOREIGN KEY PaddleLog_TripUserMap (TripId)
    REFERENCES PaddleLog (TripId);
-- Reference:  Rapids_Rivers (table: Rapids)


ALTER TABLE Rapids ADD CONSTRAINT Rapids_Rivers FOREIGN KEY Rapids_Rivers (Rivers_RiverId)
    REFERENCES Rivers (RiverId);
-- Reference:  Users_TripUserMap (table: TripUserMap)


ALTER TABLE TripUserMap ADD CONSTRAINT Users_TripUserMap FOREIGN KEY Users_TripUserMap (UserId)
    REFERENCES Users (UserId);



-- End of file.


