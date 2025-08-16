CREATE TABLE nfl.teams(
   id INT PRIMARY KEY() NOT NULL,
   displayName TEXT NOT NULL,
   location TEXT NOT NULL,
   name TEXT NOT NULL,
   shortDisplayName TEXT NOT NULL,
   abbreviation TEXT NOT NULL,
   color TEXT NOT NULL,
   alternateColor TEXT NOT NULL,
   logoURL TEXT NOT NULL
);