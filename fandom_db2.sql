PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE account(
   id INTEGER PRIMARY KEY,
   username TEXT  NOT NULL,
   password TEXT NOT NULL,
   name TEXT NOT NULL
);
INSERT INTO account VALUES(1,'horse','scrypt:32768:8:1$Qc16mwYfkvjGOstB$7d8298eb2fd73cd749cb2e506bdcb38d4f651df6718ed8010762c7af7be418781464922d9fce90b2c57b57b43621fb35fd736762e8529b0e4db95280ccb407a0','Horsey');
INSERT INTO account VALUES(2,'colt123','scrypt:32768:8:1$dagw9aWao0kV23u2$ace1cea344019063403e012c847f00cb9f894c58550c58b6f4a3978adc7a4921fad00b110ad81618b17071641ad18c1a4fa5e47fd99eb376532c6b286559ac6f','Joe');
INSERT INTO account VALUES(3,'ponyboy','scrypt:32768:8:1$YBxgBHvckPfT24ub$0b00da0766648038fc3657a8a900534c621fb45bda2f6f9837296017e5a275cd102e53fb42641f388324e7588f6e238c6c7bb019179e561a530f77703c94b38c','Phil');

CREATE TABLE account_teams(
   id INTEGER PRIMARY KEY,
   account_id INTEGER,
   team_id INTEGER,
   FOREIGN KEY (account_id) REFERENCES account(id),
   FOREIGN KEY (team_id) REFERENCES team(appID)
);
-- INSERT INTO account_teams VALUES(1,1,10);
-- INSERT INTO account_teams VALUES(2,1,58);
-- INSERT INTO account_teams VALUES(3,2,7);
-- INSERT INTO account_teams VALUES(4,2,67);
-- INSERT INTO account_teams VALUES(5,3,57);
-- INSERT INTO account_teams VALUES(6,3,213);

CREATE TABLE team(
   id INTEGER NOT NULL,
   displayName TEXT NOT NULL,
   location TEXT NOT NULL,
   name TEXT NOT NULL,
   shortDisplayName TEXT NOT NULL,
   abbreviation TEXT NOT NULL,
   color TEXT NOT NULL,
   alternateColor TEXT NOT NULL,
   logoURL TEXT NOT NULL,
   league TEXT NOT NULL,
   appID INTEGER PRIMARY KEY
);

COMMIT;
