PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE account(
   id INTEGER PRIMARY KEY,
   username TEXT  NOT NULL,
   password TEXT NOT NULL,
   name TEXT NOT NULL
);
INSERT INTO account VALUES(1,'horse','horseman1','Horsey');
INSERT INTO account VALUES(2,'colt123','neighneigh','Joe');
INSERT INTO account VALUES(3,'ponyboy','clickclack','Phil');
COMMIT;
