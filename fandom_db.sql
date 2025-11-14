PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE account(
   id INTEGER PRIMARY KEY,
   username TEXT NOT NULL,
   password TEXT NOT NULL,
   name TEXT NOT NULL
);
INSERT INTO account VALUES(1,'horse','scrypt:32768:8:1$Qc16mwYfkvjGOstB$7d8298eb2fd73cd749cb2e506bdcb38d4f651df6718ed8010762c7af7be418781464922d9fce90b2c57b57b43621fb35fd736762e8529b0e4db95280ccb407a0','Jim');
INSERT INTO account VALUES(2,'colt123','scrypt:32768:8:1$dagw9aWao0kV23u2$ace1cea344019063403e012c847f00cb9f894c58550c58b6f4a3978adc7a4921fad00b110ad81618b17071641ad18c1a4fa5e47fd99eb376532c6b286559ac6f','Joe');
INSERT INTO account VALUES(3,'ponyboy','scrypt:32768:8:1$YBxgBHvckPfT24ub$0b00da0766648038fc3657a8a900534c621fb45bda2f6f9837296017e5a275cd102e53fb42641f388324e7588f6e238c6c7bb019179e561a530f77703c94b38c','Phil');
INSERT INTO account VALUES(4,'justa.man','pbkdf2:sha256:1000000$dkTWlk18PtN0ABir$07ebb8620c8a9986587a976312f7b49a8b4bae46d4d6500ef6497281da7f5d30','Justa');
INSERT INTO account VALUES(5,'newuser','pbkdf2:sha256:1000000$MZrLasePb1zILrre$716b26a2cb3aa790f7f4bc3b3d06cedeec613a60a9efe9fb0a84ce384d1714f2','Joebob');
INSERT INTO account VALUES(6,'chip.patterson','pbkdf2:sha256:1000000$UA92Oo3JDyJ9JuPb$4debd4fb303dd5a2173107bd9c2dfd0e06c18858f3b685d60ec4f842f7064f33','Chip');

CREATE TABLE league(
   id INTEGER PRIMARY KEY,
   espn_league_id INTEGER NOT NULL,
   name TEXT NOT NULL, 
   logo_url TEXT NOT NULL,
   current_season TEXT NOT NULL,
   current_season_type TEXT NOT NULL
);
INSERT INTO league VALUES(1,28,'NFL','https://a.espncdn.com/i/teamlogos/leagues/500/nfl.png',2025,2);
INSERT INTO league VALUES(2,46,'NBA','https://a.espncdn.com/i/teamlogos/leagues/500/nba.png',2026,2);
INSERT INTO league VALUES(3,23,'CFB','https://a.espncdn.com/redesign/assets/img/icons/ESPN-icon-football-college.png',2025,2);
INSERT INTO league VALUES(4,10,'MLB','https://a.espncdn.com/i/teamlogos/leagues/500/mlb.png',2025,3);
INSERT INTO league VALUES(5,700,'PREM','https://a.espncdn.com/i/leaguelogos/soccer/500/23.png',2025,13481);

CREATE TABLE team(
   espn_team_id INTEGER NOT NULL,
   display_name TEXT NOT NULL,
   location TEXT NOT NULL,
   name TEXT NOT NULL,
   short_display_name TEXT NOT NULL,
   abbreviation TEXT NOT NULL,
   color TEXT NOT NULL,
   alternate_color TEXT NOT NULL,
   logo_url TEXT NOT NULL,
   league_id INTEGER,
   id INTEGER PRIMARY KEY,
   FOREIGN KEY (league_id) REFERENCES league(id)
);
INSERT INTO team VALUES(1,'Atlanta Falcons','Atlanta','Falcons','Falcons','ATL','a71930','000000','https://a.espncdn.com/i/teamlogos/nfl/500/atl.png',1,0);
INSERT INTO team VALUES(2,'Buffalo Bills','Buffalo','Bills','Bills','BUF','00338d','d50a0a','https://a.espncdn.com/i/teamlogos/nfl/500/buf.png',1,1);
INSERT INTO team VALUES(3,'Chicago Bears','Chicago','Bears','Bears','CHI','0b1c3a','e64100','https://a.espncdn.com/i/teamlogos/nfl/500/chi.png',1,2);
INSERT INTO team VALUES(4,'Cincinnati Bengals','Cincinnati','Bengals','Bengals','CIN','fb4f14','000000','https://a.espncdn.com/i/teamlogos/nfl/500/cin.png',1,3);
INSERT INTO team VALUES(5,'Cleveland Browns','Cleveland','Browns','Browns','CLE','472a08','ff3c00','https://a.espncdn.com/i/teamlogos/nfl/500/cle.png',1,4);
INSERT INTO team VALUES(6,'Dallas Cowboys','Dallas','Cowboys','Cowboys','DAL','002a5c','b0b7bc','https://a.espncdn.com/i/teamlogos/nfl/500/dal.png',1,5);
INSERT INTO team VALUES(7,'Denver Broncos','Denver','Broncos','Broncos','DEN','0a2343','fc4c02','https://a.espncdn.com/i/teamlogos/nfl/500/den.png',1,6);
INSERT INTO team VALUES(8,'Detroit Lions','Detroit','Lions','Lions','DET','0076b6','bbbbbb','https://a.espncdn.com/i/teamlogos/nfl/500/det.png',1,7);
INSERT INTO team VALUES(9,'Green Bay Packers','Green Bay','Packers','Packers','GB','204e32','ffb612','https://a.espncdn.com/i/teamlogos/nfl/500/gb.png',1,8);
INSERT INTO team VALUES(10,'Tennessee Titans','Tennessee','Titans','Titans','TEN','4b92db','002a5c','https://a.espncdn.com/i/teamlogos/nfl/500/ten.png',1,9);
INSERT INTO team VALUES(11,'Indianapolis Colts','Indianapolis','Colts','Colts','IND','003b75','ffffff','https://a.espncdn.com/i/teamlogos/nfl/500/ind.png',1,10);
INSERT INTO team VALUES(12,'Kansas City Chiefs','Kansas City','Chiefs','Chiefs','KC','e31837','ffb612','https://a.espncdn.com/i/teamlogos/nfl/500/kc.png',1,11);
INSERT INTO team VALUES(13,'Las Vegas Raiders','Las Vegas','Raiders','Raiders','LV','000000','a5acaf','https://a.espncdn.com/i/teamlogos/nfl/500/lv.png',1,12);
INSERT INTO team VALUES(14,'Los Angeles Rams','Los Angeles','Rams','Rams','LAR','003594','ffd100','https://a.espncdn.com/i/teamlogos/nfl/500/lar.png',1,13);
INSERT INTO team VALUES(15,'Miami Dolphins','Miami','Dolphins','Dolphins','MIA','008e97','fc4c02','https://a.espncdn.com/i/teamlogos/nfl/500/mia.png',1,14);
INSERT INTO team VALUES(16,'Minnesota Vikings','Minnesota','Vikings','Vikings','MIN','4f2683','ffc62f','https://a.espncdn.com/i/teamlogos/nfl/500/min.png',1,15);
INSERT INTO team VALUES(17,'New England Patriots','New England','Patriots','Patriots','NE','002a5c','c60c30','https://a.espncdn.com/i/teamlogos/nfl/500/ne.png',1,16);
INSERT INTO team VALUES(18,'New Orleans Saints','New Orleans','Saints','Saints','NO','d3bc8d','000000','https://a.espncdn.com/i/teamlogos/nfl/500/no.png',1,17);
INSERT INTO team VALUES(19,'New York Giants','New York','Giants','Giants','NYG','003c7f','c9243f','https://a.espncdn.com/i/teamlogos/nfl/500/nyg.png',1,18);
INSERT INTO team VALUES(20,'New York Jets','New York','Jets','Jets','NYJ','115740','ffffff','https://a.espncdn.com/i/teamlogos/nfl/500/nyj.png',1,19);
INSERT INTO team VALUES(21,'Philadelphia Eagles','Philadelphia','Eagles','Eagles','PHI','06424d','000000','https://a.espncdn.com/i/teamlogos/nfl/500/phi.png',1,20);
INSERT INTO team VALUES(22,'Arizona Cardinals','Arizona','Cardinals','Cardinals','ARI','a40227','ffffff','https://a.espncdn.com/i/teamlogos/nfl/500/ari.png',1,21);
INSERT INTO team VALUES(23,'Pittsburgh Steelers','Pittsburgh','Steelers','Steelers','PIT','000000','ffb612','https://a.espncdn.com/i/teamlogos/nfl/500/pit.png',1,22);
INSERT INTO team VALUES(24,'Los Angeles Chargers','Los Angeles','Chargers','Chargers','LAC','0080c6','ffc20e','https://a.espncdn.com/i/teamlogos/nfl/500/lac.png',1,23);
INSERT INTO team VALUES(25,'San Francisco 49ers','San Francisco','49ers','49ers','SF','aa0000','b3995d','https://a.espncdn.com/i/teamlogos/nfl/500/sf.png',1,24);
INSERT INTO team VALUES(26,'Seattle Seahawks','Seattle','Seahawks','Seahawks','SEA','002a5c','69be28','https://a.espncdn.com/i/teamlogos/nfl/500/sea.png',1,25);
INSERT INTO team VALUES(27,'Tampa Bay Buccaneers','Tampa Bay','Buccaneers','Buccaneers','TB','bd1c36','3e3a35','https://a.espncdn.com/i/teamlogos/nfl/500/tb.png',1,26);
INSERT INTO team VALUES(28,'Washington Commanders','Washington','Commanders','Commanders','WSH','5a1414','ffb612','https://a.espncdn.com/i/teamlogos/nfl/500/wsh.png',1,27);
INSERT INTO team VALUES(29,'Carolina Panthers','Carolina','Panthers','Panthers','CAR','0085ca','000000','https://a.espncdn.com/i/teamlogos/nfl/500/car.png',1,28);
INSERT INTO team VALUES(30,'Jacksonville Jaguars','Jacksonville','Jaguars','Jaguars','JAX','007487','d7a22a','https://a.espncdn.com/i/teamlogos/nfl/500/jax.png',1,29);
INSERT INTO team VALUES(33,'Baltimore Ravens','Baltimore','Ravens','Ravens','BAL','29126f','000000','https://a.espncdn.com/i/teamlogos/nfl/500/bal.png',1,30);
INSERT INTO team VALUES(34,'Houston Texans','Houston','Texans','Texans','HOU','00143f','c41230','https://a.espncdn.com/i/teamlogos/nfl/500/hou.png',1,31);
INSERT INTO team VALUES(2,'Auburn Tigers','Auburn','Tigers','Auburn','AUB','002b5c','f26522','https://a.espncdn.com/i/teamlogos/ncaa/500/2.png',3,32);
INSERT INTO team VALUES(5,'UAB Blazers','UAB','Blazers','UAB','UAB','003b28','ffc845','https://a.espncdn.com/i/teamlogos/ncaa/500/5.png',3,33);
INSERT INTO team VALUES(6,'South Alabama Jaguars','South Alabama','Jaguars','South Alabama','USA','003E7E','','https://a.espncdn.com/i/teamlogos/ncaa/500/6.png',3,34);
INSERT INTO team VALUES(8,'Arkansas Razorbacks','Arkansas','Razorbacks','Arkansas','ARK','a41f35','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/8.png',3,35);
INSERT INTO team VALUES(9,'Arizona State Sun Devils','Arizona State','Sun Devils','Arizona St','ASU','8e0c3a','ffc72c','https://a.espncdn.com/i/teamlogos/ncaa/500/9.png',3,36);
INSERT INTO team VALUES(12,'Arizona Wildcats','Arizona','Wildcats','Arizona','ARIZ','0c234b','ab0520','https://a.espncdn.com/i/teamlogos/ncaa/500/12.png',3,37);
INSERT INTO team VALUES(21,'San Diego State Aztecs','San Diego State','Aztecs','San Diego St','SDSU','c41230','000000','https://a.espncdn.com/i/teamlogos/ncaa/500/21.png',3,38);
INSERT INTO team VALUES(23,'San José State Spartans','San José State','Spartans','San José St','SJSU','005893','fdba31','https://a.espncdn.com/i/teamlogos/ncaa/500/23.png',3,39);
INSERT INTO team VALUES(24,'Stanford Cardinal','Stanford','Cardinal','Stanford','STAN','8c1515','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/24.png',3,40);
INSERT INTO team VALUES(25,'California Golden Bears','California','Golden Bears','California','CAL','031522','ffc423','https://a.espncdn.com/i/teamlogos/ncaa/500/25.png',3,41);
INSERT INTO team VALUES(26,'UCLA Bruins','UCLA','Bruins','UCLA','UCLA','2774ae','f2a900','https://a.espncdn.com/i/teamlogos/ncaa/500/26.png',3,42);
INSERT INTO team VALUES(30,'USC Trojans','USC','Trojans','USC','USC','9e2237','ffcc00','https://a.espncdn.com/i/teamlogos/ncaa/500/30.png',3,43);
INSERT INTO team VALUES(36,'Colorado State Rams','Colorado State','Rams','Colorado St','CSU','1e4d2b','c8c372','https://a.espncdn.com/i/teamlogos/ncaa/500/36.png',3,44);
INSERT INTO team VALUES(38,'Colorado Buffaloes','Colorado','Buffaloes','Colorado','COLO','000000','cfb87c','https://a.espncdn.com/i/teamlogos/ncaa/500/38.png',3,45);
INSERT INTO team VALUES(41,'UConn Huskies','UConn','Huskies','UConn','CONN','0c2340','f1f2f3','https://a.espncdn.com/i/teamlogos/ncaa/500/41.png',3,46);
INSERT INTO team VALUES(48,'Delaware Blue Hens','Delaware','Blue Hens','Delaware','DEL','033594','e8ce31','https://a.espncdn.com/i/teamlogos/ncaa/500/48.png',3,47);
INSERT INTO team VALUES(52,'Florida State Seminoles','Florida State','Seminoles','Florida St','FSU','782f40','ceb888','https://a.espncdn.com/i/teamlogos/ncaa/500/52.png',3,48);
INSERT INTO team VALUES(55,'Jacksonville State Gamecocks','Jacksonville State','Gamecocks','Jax State','JVST','b50500','b5b7ba','https://a.espncdn.com/i/teamlogos/ncaa/500/55.png',3,49);
INSERT INTO team VALUES(57,'Florida Gators','Florida','Gators','Florida','FLA','0021a5','fa4616','https://a.espncdn.com/i/teamlogos/ncaa/500/57.png',3,50);
INSERT INTO team VALUES(58,'South Florida Bulls','South Florida','Bulls','South Florida','USF','004A36','231f20','https://a.espncdn.com/i/teamlogos/ncaa/500/58.png',3,51);
INSERT INTO team VALUES(59,'Georgia Tech Yellow Jackets','Georgia Tech','Yellow Jackets','Georgia Tech','GT','003057','b3a369','https://a.espncdn.com/i/teamlogos/ncaa/500/59.png',3,52);
INSERT INTO team VALUES(61,'Georgia Bulldogs','Georgia','Bulldogs','Georgia','UGA','ba0c2f','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/61.png',3,53);
INSERT INTO team VALUES(62,'Hawai''i Rainbow Warriors','Hawai''i','Rainbow Warriors','Hawai''i','HAW','003420','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/62.png',3,54);
INSERT INTO team VALUES(66,'Iowa State Cyclones','Iowa State','Cyclones','Iowa State','ISU','822433','fdca2f','https://a.espncdn.com/i/teamlogos/ncaa/500/66.png',3,55);
INSERT INTO team VALUES(68,'Boise State Broncos','Boise State','Broncos','Boise St','BOIS','0033a0','fa4616','https://a.espncdn.com/i/teamlogos/ncaa/500/68.png',3,56);
INSERT INTO team VALUES(77,'Northwestern Wildcats','Northwestern','Wildcats','Northwestern','NU','582c83','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/77.png',3,57);
INSERT INTO team VALUES(84,'Indiana Hoosiers','Indiana','Hoosiers','Indiana','IU','990000','edebeb','https://a.espncdn.com/i/teamlogos/ncaa/500/84.png',3,58);
INSERT INTO team VALUES(87,'Notre Dame Fighting Irish','Notre Dame','Fighting Irish','Notre Dame','ND','0c2340','c99700','https://a.espncdn.com/i/teamlogos/ncaa/500/87.png',3,59);
INSERT INTO team VALUES(96,'Kentucky Wildcats','Kentucky','Wildcats','Kentucky','UK','0033a0','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/96.png',3,60);
INSERT INTO team VALUES(97,'Louisville Cardinals','Louisville','Cardinals','Louisville','LOU','c9001f','000000','https://a.espncdn.com/i/teamlogos/ncaa/500/97.png',3,61);
INSERT INTO team VALUES(98,'Western Kentucky Hilltoppers','Western Kentucky','Hilltoppers','Western KY','WKU','F32026','b3b5b8','https://a.espncdn.com/i/teamlogos/ncaa/500/98.png',3,62);
INSERT INTO team VALUES(99,'LSU Tigers','LSU','Tigers','LSU','LSU','461d7c','fdd023','https://a.espncdn.com/i/teamlogos/ncaa/500/99.png',3,63);
INSERT INTO team VALUES(103,'Boston College Eagles','Boston College','Eagles','Boston College','BC','8c2232','dbcca6','https://a.espncdn.com/i/teamlogos/ncaa/500/103.png',3,64);
INSERT INTO team VALUES(113,'Massachusetts Minutemen','Massachusetts','Minutemen','UMass','MASS','880007','','https://a.espncdn.com/i/teamlogos/ncaa/500/113.png',3,65);
INSERT INTO team VALUES(120,'Maryland Terrapins','Maryland','Terrapins','Maryland','MD','D5002B','ffcd00','https://a.espncdn.com/i/teamlogos/ncaa/500/120.png',3,66);
INSERT INTO team VALUES(127,'Michigan State Spartans','Michigan State','Spartans','Michigan St','MSU','18453b','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/127.png',3,67);
INSERT INTO team VALUES(130,'Michigan Wolverines','Michigan','Wolverines','Michigan','MICH','00274c','ffcb05','https://a.espncdn.com/i/teamlogos/ncaa/500/130.png',3,68);
INSERT INTO team VALUES(135,'Minnesota Golden Gophers','Minnesota','Golden Gophers','Minnesota','MINN','5e0a2f','fab41c','https://a.espncdn.com/i/teamlogos/ncaa/500/135.png',3,69);
INSERT INTO team VALUES(142,'Missouri Tigers','Missouri','Tigers','Missouri','MIZ','f1b82d','000000','https://a.espncdn.com/i/teamlogos/ncaa/500/142.png',3,70);
INSERT INTO team VALUES(145,'Ole Miss Rebels','Ole Miss','Rebels','Ole Miss','MISS','13294b','c8102e','https://a.espncdn.com/i/teamlogos/ncaa/500/145.png',3,71);
INSERT INTO team VALUES(150,'Duke Blue Devils','Duke','Blue Devils','Duke','DUKE','013088','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/150.png',3,72);
INSERT INTO team VALUES(151,'East Carolina Pirates','East Carolina','Pirates','East Carolina','ECU','4b1869','f0907b','https://a.espncdn.com/i/teamlogos/ncaa/500/151.png',3,73);
INSERT INTO team VALUES(152,'NC State Wolfpack','NC State','Wolfpack','NC State','NCSU','cc0000','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/152.png',3,74);
INSERT INTO team VALUES(153,'North Carolina Tar Heels','North Carolina','Tar Heels','North Carolina','UNC','7bafd4','13294b','https://a.espncdn.com/i/teamlogos/ncaa/500/153.png',3,75);
INSERT INTO team VALUES(154,'Wake Forest Demon Deacons','Wake Forest','Demon Deacons','Wake Forest','WAKE','000000','ceb888','https://a.espncdn.com/i/teamlogos/ncaa/500/154.png',3,76);
INSERT INTO team VALUES(158,'Nebraska Cornhuskers','Nebraska','Cornhuskers','Nebraska','NEB','d00000','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/158.png',3,77);
INSERT INTO team VALUES(164,'Rutgers Scarlet Knights','Rutgers','Scarlet Knights','Rutgers','RUTG','d21034','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/164.png',3,78);
INSERT INTO team VALUES(166,'New Mexico State Aggies','New Mexico State','Aggies','New Mexico St','NMSU','891216','000000','https://a.espncdn.com/i/teamlogos/ncaa/500/166.png',3,79);
INSERT INTO team VALUES(167,'New Mexico Lobos','New Mexico','Lobos','New Mexico','UNM','000000','231f20','https://a.espncdn.com/i/teamlogos/ncaa/500/167.png',3,80);
INSERT INTO team VALUES(183,'Syracuse Orange','Syracuse','Orange','Syracuse','SYR','ff6500','000e54','https://a.espncdn.com/i/teamlogos/ncaa/500/183.png',3,81);
INSERT INTO team VALUES(189,'Bowling Green Falcons','Bowling Green','Falcons','Bowling Green','BGSU','2b1000','492000','https://a.espncdn.com/i/teamlogos/ncaa/500/189.png',3,82);
INSERT INTO team VALUES(193,'Miami (OH) RedHawks','Miami (OH)','RedHawks','Miami OH','M-OH','a4000c','f0f0f0','https://a.espncdn.com/i/teamlogos/ncaa/500/193.png',3,83);
INSERT INTO team VALUES(194,'Ohio State Buckeyes','Ohio State','Buckeyes','Ohio State','OSU','ce1141','505056','https://a.espncdn.com/i/teamlogos/ncaa/500/194.png',3,84);
INSERT INTO team VALUES(195,'Ohio Bobcats','Ohio','Bobcats','Ohio','OHIO','295A29','e4bb85','https://a.espncdn.com/i/teamlogos/ncaa/500/195.png',3,85);
INSERT INTO team VALUES(197,'Oklahoma State Cowboys','Oklahoma State','Cowboys','Oklahoma St','OKST','000000','dddddd','https://a.espncdn.com/i/teamlogos/ncaa/500/197.png',3,86);
INSERT INTO team VALUES(201,'Oklahoma Sooners','Oklahoma','Sooners','Oklahoma','OU','a32036','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/201.png',3,87);
INSERT INTO team VALUES(202,'Tulsa Golden Hurricane','Tulsa','Golden Hurricane','Tulsa','TLSA','003595','d0b787','https://a.espncdn.com/i/teamlogos/ncaa/500/202.png',3,88);
INSERT INTO team VALUES(204,'Oregon State Beavers','Oregon State','Beavers','Oregon St','ORST','231f20','d73f09','https://a.espncdn.com/i/teamlogos/ncaa/500/204.png',3,89);
INSERT INTO team VALUES(213,'Penn State Nittany Lions','Penn State','Nittany Lions','Penn State','PSU','00265D','002e5c','https://a.espncdn.com/i/teamlogos/ncaa/500/213.png',3,90);
INSERT INTO team VALUES(218,'Temple Owls','Temple','Owls','Temple','TEM','A80532','a7a9ac','https://a.espncdn.com/i/teamlogos/ncaa/500/218.png',3,91);
INSERT INTO team VALUES(221,'Pittsburgh Panthers','Pittsburgh','Panthers','Pitt','PITT','003263','231f20','https://a.espncdn.com/i/teamlogos/ncaa/500/221.png',3,92);
INSERT INTO team VALUES(228,'Clemson Tigers','Clemson','Tigers','Clemson','CLEM','f56600','522d80','https://a.espncdn.com/i/teamlogos/ncaa/500/228.png',3,93);
INSERT INTO team VALUES(235,'Memphis Tigers','Memphis','Tigers','Memphis','MEM','004991','8e908f','https://a.espncdn.com/i/teamlogos/ncaa/500/235.png',3,94);
INSERT INTO team VALUES(238,'Vanderbilt Commodores','Vanderbilt','Commodores','Vanderbilt','VAN','000000','231f20','https://a.espncdn.com/i/teamlogos/ncaa/500/238.png',3,95);
INSERT INTO team VALUES(239,'Baylor Bears','Baylor','Bears','Baylor','BAY','154734','ffb81c','https://a.espncdn.com/i/teamlogos/ncaa/500/239.png',3,96);
INSERT INTO team VALUES(242,'Rice Owls','Rice','Owls','Rice','RICE','d1d5d8','003d7d','https://a.espncdn.com/i/teamlogos/ncaa/500/242.png',3,97);
INSERT INTO team VALUES(245,'Texas A&M Aggies','Texas A&M','Aggies','Texas A&M','TA&M','500000','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/245.png',3,98);
INSERT INTO team VALUES(248,'Houston Cougars','Houston','Cougars','Houston','HOU','c92a39','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/248.png',3,99);
INSERT INTO team VALUES(249,'North Texas Mean Green','North Texas','Mean Green','North Texas','UNT','ffffff','000000','https://a.espncdn.com/i/teamlogos/ncaa/500/249.png',3,100);
INSERT INTO team VALUES(251,'Texas Longhorns','Texas','Longhorns','Texas','TEX','c15d26','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/251.png',3,101);
INSERT INTO team VALUES(252,'BYU Cougars','BYU','Cougars','BYU','BYU','003da5','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/252.png',3,102);
INSERT INTO team VALUES(254,'Utah Utes','Utah','Utes','Utah','UTAH','ea002a','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/254.png',3,103);
INSERT INTO team VALUES(256,'James Madison Dukes','James Madison','Dukes','James Madison','JMU','450084','b5a068','https://a.espncdn.com/i/teamlogos/ncaa/500/256.png',3,104);
INSERT INTO team VALUES(258,'Virginia Cavaliers','Virginia','Cavaliers','Virginia','UVA','232d4b','f84c1e','https://a.espncdn.com/i/teamlogos/ncaa/500/258.png',3,105);
INSERT INTO team VALUES(259,'Virginia Tech Hokies','Virginia Tech','Hokies','Virginia Tech','VT','630031','cf4520','https://a.espncdn.com/i/teamlogos/ncaa/500/259.png',3,106);
INSERT INTO team VALUES(264,'Washington Huskies','Washington','Huskies','Washington','WASH','33006f','e8d3a2','https://a.espncdn.com/i/teamlogos/ncaa/500/264.png',3,107);
INSERT INTO team VALUES(265,'Washington State Cougars','Washington State','Cougars','Washington St','WSU','981e32','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/265.png',3,108);
INSERT INTO team VALUES(275,'Wisconsin Badgers','Wisconsin','Badgers','Wisconsin','WIS','c4012f','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/275.png',3,109);
INSERT INTO team VALUES(276,'Marshall Thundering Herd','Marshall','Thundering Herd','Marshall','MRSH','00ae42','be854c','https://a.espncdn.com/i/teamlogos/ncaa/500/276.png',3,110);
INSERT INTO team VALUES(277,'West Virginia Mountaineers','West Virginia','Mountaineers','West Virginia','WVU','002855','eaaa00','https://a.espncdn.com/i/teamlogos/ncaa/500/277.png',3,111);
INSERT INTO team VALUES(278,'Fresno State Bulldogs','Fresno State','Bulldogs','Fresno St','FRES','c41230','13284c','https://a.espncdn.com/i/teamlogos/ncaa/500/278.png',3,112);
INSERT INTO team VALUES(290,'Georgia Southern Eagles','Georgia Southern','Eagles','GA Southern','GASO','003775','f0f0f0','https://a.espncdn.com/i/teamlogos/ncaa/500/290.png',3,113);
INSERT INTO team VALUES(295,'Old Dominion Monarchs','Old Dominion','Monarchs','Old Dominion','ODU','00507d','a1d2f1','https://a.espncdn.com/i/teamlogos/ncaa/500/295.png',3,114);
INSERT INTO team VALUES(309,'Louisiana Ragin'' Cajuns','Louisiana','Ragin'' Cajuns','Louisiana','UL','ce181e','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/309.png',3,115);
INSERT INTO team VALUES(324,'Coastal Carolina Chanticleers','Coastal Carolina','Chanticleers','Coastal','CCU','007073','876447','https://a.espncdn.com/i/teamlogos/ncaa/500/324.png',3,116);
INSERT INTO team VALUES(326,'Texas State Bobcats','Texas State','Bobcats','Texas St','TXST','4e1719','b4975a','https://a.espncdn.com/i/teamlogos/ncaa/500/326.png',3,117);
INSERT INTO team VALUES(328,'Utah State Aggies','Utah State','Aggies','Utah State','USU','00263a','949ca1','https://a.espncdn.com/i/teamlogos/ncaa/500/328.png',3,118);
INSERT INTO team VALUES(333,'Alabama Crimson Tide','Alabama','Crimson Tide','Alabama','ALA','9e1632','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/333.png',3,119);
INSERT INTO team VALUES(338,'Kennesaw State Owls','Kennesaw State','Owls','Kennesaw St','KENN','fdbb30','000000','https://a.espncdn.com/i/teamlogos/ncaa/500/338.png',3,120);
INSERT INTO team VALUES(344,'Mississippi State Bulldogs','Mississippi State','Bulldogs','Mississippi St','MSST','5d1725','c1c6c8','https://a.espncdn.com/i/teamlogos/ncaa/500/344.png',3,121);
INSERT INTO team VALUES(349,'Army Black Knights','Army','Black Knights','Army','ARMY','ce9c00','231f20','https://a.espncdn.com/i/teamlogos/ncaa/500/349.png',3,122);
INSERT INTO team VALUES(356,'Illinois Fighting Illini','Illinois','Fighting Illini','Illinois','ILL','ff5f05','13294b','https://a.espncdn.com/i/teamlogos/ncaa/500/356.png',3,123);
INSERT INTO team VALUES(2005,'Air Force Falcons','Air Force','Falcons','Air Force','AFA','003594','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/2005.png',3,124);
INSERT INTO team VALUES(2006,'Akron Zips','Akron','Zips','Akron','AKR','00285e','84754e','https://a.espncdn.com/i/teamlogos/ncaa/500/2006.png',3,125);
INSERT INTO team VALUES(2026,'App State Mountaineers','App State','Mountaineers','App State','APP','000000','ffcd00','https://a.espncdn.com/i/teamlogos/ncaa/500/2026.png',3,126);
INSERT INTO team VALUES(2032,'Arkansas State Red Wolves','Arkansas State','Red Wolves','Arkansas St','ARST','e81018','000000','https://a.espncdn.com/i/teamlogos/ncaa/500/2032.png',3,127);
INSERT INTO team VALUES(2050,'Ball State Cardinals','Ball State','Cardinals','Ball State','BALL','DA0000','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/2050.png',3,128);
INSERT INTO team VALUES(2084,'Buffalo Bulls','Buffalo','Bulls','Buffalo','BUFF','041A9B','ebebeb','https://a.espncdn.com/i/teamlogos/ncaa/500/2084.png',3,129);
INSERT INTO team VALUES(2116,'UCF Knights','UCF','Knights','UCF','UCF','000000','b4a269','https://a.espncdn.com/i/teamlogos/ncaa/500/2116.png',3,130);
INSERT INTO team VALUES(2117,'Central Michigan Chippewas','Central Michigan','Chippewas','C Michigan','CMU','6a0032','ffc82e','https://a.espncdn.com/i/teamlogos/ncaa/500/2117.png',3,131);
INSERT INTO team VALUES(2132,'Cincinnati Bearcats','Cincinnati','Bearcats','Cincinnati','CIN','000000','717073','https://a.espncdn.com/i/teamlogos/ncaa/500/2132.png',3,132);
INSERT INTO team VALUES(2199,'Eastern Michigan Eagles','Eastern Michigan','Eagles','E Michigan','EMU','00331b','f0f0f0','https://a.espncdn.com/i/teamlogos/ncaa/500/2199.png',3,133);
INSERT INTO team VALUES(2226,'Florida Atlantic Owls','Florida Atlantic','Owls','FAU','FAU','00447c','d31245','https://a.espncdn.com/i/teamlogos/ncaa/500/2226.png',3,134);
INSERT INTO team VALUES(2229,'Florida International Panthers','Florida International','Panthers','FIU','FIU','001538','c5960c','https://a.espncdn.com/i/teamlogos/ncaa/500/2229.png',3,135);
INSERT INTO team VALUES(2247,'Georgia State Panthers','Georgia State','Panthers','Georgia St','GAST','1e539a','ebebeb','https://a.espncdn.com/i/teamlogos/ncaa/500/2247.png',3,136);
INSERT INTO team VALUES(2294,'Iowa Hawkeyes','Iowa','Hawkeyes','Iowa','IOWA','000000','fcd116','https://a.espncdn.com/i/teamlogos/ncaa/500/2294.png',3,137);
INSERT INTO team VALUES(2305,'Kansas Jayhawks','Kansas','Jayhawks','Kansas','KU','0051ba','e8000d','https://a.espncdn.com/i/teamlogos/ncaa/500/2305.png',3,138);
INSERT INTO team VALUES(2306,'Kansas State Wildcats','Kansas State','Wildcats','Kansas St','KSU','3c0969','e2e3e4','https://a.espncdn.com/i/teamlogos/ncaa/500/2306.png',3,139);
INSERT INTO team VALUES(2309,'Kent State Golden Flashes','Kent State','Golden Flashes','Kent State','KENT','003976','efab00','https://a.espncdn.com/i/teamlogos/ncaa/500/2309.png',3,140);
INSERT INTO team VALUES(2335,'Liberty Flames','Liberty','Flames','Liberty','LIB','071740','a61f21','https://a.espncdn.com/i/teamlogos/ncaa/500/2335.png',3,141);
INSERT INTO team VALUES(2348,'Louisiana Tech Bulldogs','Louisiana Tech','Bulldogs','Louisiana Tech','LT','002d65','d3313a','https://a.espncdn.com/i/teamlogos/ncaa/500/2348.png',3,142);
INSERT INTO team VALUES(2390,'Miami Hurricanes','Miami','Hurricanes','Miami','MIA','005030','f47321','https://a.espncdn.com/i/teamlogos/ncaa/500/2390.png',3,143);
INSERT INTO team VALUES(2393,'Middle Tennessee Blue Raiders','Middle Tennessee','Blue Raiders','MTSU','MTSU','006db6','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/2393.png',3,144);
INSERT INTO team VALUES(2426,'Navy Midshipmen','Navy','Midshipmen','Navy','NAVY','00225b','b5a67c','https://a.espncdn.com/i/teamlogos/ncaa/500/2426.png',3,145);
INSERT INTO team VALUES(2429,'Charlotte 49ers','Charlotte','49ers','Charlotte','CLT','ffffff','cfab7a','https://a.espncdn.com/i/teamlogos/ncaa/500/2429.png',3,146);
INSERT INTO team VALUES(2433,'UL Monroe Warhawks','UL Monroe','Warhawks','UL Monroe','ULM','231F20','b18445','https://a.espncdn.com/i/teamlogos/ncaa/500/2433.png',3,147);
INSERT INTO team VALUES(2439,'UNLV Rebels','UNLV','Rebels','UNLV','UNLV','b10202','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/2439.png',3,148);
INSERT INTO team VALUES(2440,'Nevada Wolf Pack','Nevada','Wolf Pack','Nevada','NEV','002d62','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/2440.png',3,149);
INSERT INTO team VALUES(2459,'Northern Illinois Huskies','Northern Illinois','Huskies','N Illinois','NIU','F1122C','cc0000','https://a.espncdn.com/i/teamlogos/ncaa/500/2459.png',3,150);
INSERT INTO team VALUES(2483,'Oregon Ducks','Oregon','Ducks','Oregon','ORE','007030','fee11a','https://a.espncdn.com/i/teamlogos/ncaa/500/2483.png',3,151);
INSERT INTO team VALUES(2509,'Purdue Boilermakers','Purdue','Boilermakers','Purdue','PUR','000000','cfb991','https://a.espncdn.com/i/teamlogos/ncaa/500/2509.png',3,152);
INSERT INTO team VALUES(2534,'Sam Houston Bearkats','Sam Houston','Bearkats','Sam Houston','SHSU','fe5000','000000','https://a.espncdn.com/i/teamlogos/ncaa/500/2534.png',3,153);
INSERT INTO team VALUES(2567,'SMU Mustangs','SMU','Mustangs','SMU','SMU','354ca1','cc0035','https://a.espncdn.com/i/teamlogos/ncaa/500/2567.png',3,154);
INSERT INTO team VALUES(2572,'Southern Miss Golden Eagles','Southern Miss','Golden Eagles','Southern Miss','USM','FFAA3C','ffc423','https://a.espncdn.com/i/teamlogos/ncaa/500/2572.png',3,155);
INSERT INTO team VALUES(2579,'South Carolina Gamecocks','South Carolina','Gamecocks','South Carolina','SC','73000a','ffffff','https://a.espncdn.com/i/teamlogos/ncaa/500/2579.png',3,156);
INSERT INTO team VALUES(2623,'Missouri State Bears','Missouri State','Bears','Missouri St','MOST','5F0000','e8e8e8','https://a.espncdn.com/i/teamlogos/ncaa/500/2623.png',3,157);
INSERT INTO team VALUES(2628,'TCU Horned Frogs','TCU','Horned Frogs','TCU','TCU','4d1979','f1f2f3','https://a.espncdn.com/i/teamlogos/ncaa/500/2628.png',3,158);
INSERT INTO team VALUES(2633,'Tennessee Volunteers','Tennessee','Volunteers','Tennessee','TENN','ff8200','58595b','https://a.espncdn.com/i/teamlogos/ncaa/500/2633.png',3,159);
INSERT INTO team VALUES(2636,'UTSA Roadrunners','UTSA','Roadrunners','UTSA','UTSA','002A5C','f47321','https://a.espncdn.com/i/teamlogos/ncaa/500/2636.png',3,160);
INSERT INTO team VALUES(2638,'UTEP Miners','UTEP','Miners','UTEP','UTEP','ff8200','041e42','https://a.espncdn.com/i/teamlogos/ncaa/500/2638.png',3,161);
INSERT INTO team VALUES(2641,'Texas Tech Red Raiders','Texas Tech','Red Raiders','Texas Tech','TTU','000000','da291c','https://a.espncdn.com/i/teamlogos/ncaa/500/2641.png',3,162);
INSERT INTO team VALUES(2649,'Toledo Rockets','Toledo','Rockets','Toledo','TOL','0a2240','ffcd00','https://a.espncdn.com/i/teamlogos/ncaa/500/2649.png',3,163);
INSERT INTO team VALUES(2653,'Troy Trojans','Troy','Trojans','Troy','TROY','AE0210','88898c','https://a.espncdn.com/i/teamlogos/ncaa/500/2653.png',3,164);
INSERT INTO team VALUES(2655,'Tulane Green Wave','Tulane','Green Wave','Tulane','TULN','006547','468ac9','https://a.espncdn.com/i/teamlogos/ncaa/500/2655.png',3,165);
INSERT INTO team VALUES(2711,'Western Michigan Broncos','Western Michigan','Broncos','W Michigan','WMU','532e1f','8b7f79','https://a.espncdn.com/i/teamlogos/ncaa/500/2711.png',3,166);
INSERT INTO team VALUES(2751,'Wyoming Cowboys','Wyoming','Cowboys','Wyoming','WYO','492f24','ffc425','https://a.espncdn.com/i/teamlogos/ncaa/500/2751.png',3,167);
INSERT INTO team VALUES(1,'Atlanta Hawks','Atlanta','Hawks','Hawks','ATL','c8102e','fdb927','https://a.espncdn.com/i/teamlogos/nba/500/atl.png',2,168);
INSERT INTO team VALUES(2,'Boston Celtics','Boston','Celtics','Celtics','BOS','008348','ffffff','https://a.espncdn.com/i/teamlogos/nba/500/bos.png',2,169);
INSERT INTO team VALUES(3,'New Orleans Pelicans','New Orleans','Pelicans','Pelicans','NO','0a2240','b4975a','https://a.espncdn.com/i/teamlogos/nba/500/no.png',2,170);
INSERT INTO team VALUES(4,'Chicago Bulls','Chicago','Bulls','Bulls','CHI','ce1141','000000','https://a.espncdn.com/i/teamlogos/nba/500/chi.png',2,171);
INSERT INTO team VALUES(5,'Cleveland Cavaliers','Cleveland','Cavaliers','Cavaliers','CLE','860038','bc945c','https://a.espncdn.com/i/teamlogos/nba/500/cle.png',2,172);
INSERT INTO team VALUES(6,'Dallas Mavericks','Dallas','Mavericks','Mavericks','DAL','0064b1','bbc4ca','https://a.espncdn.com/i/teamlogos/nba/500/dal.png',2,173);
INSERT INTO team VALUES(7,'Denver Nuggets','Denver','Nuggets','Nuggets','DEN','0e2240','fec524','https://a.espncdn.com/i/teamlogos/nba/500/den.png',2,174);
INSERT INTO team VALUES(8,'Detroit Pistons','Detroit','Pistons','Pistons','DET','1d428a','c8102e','https://a.espncdn.com/i/teamlogos/nba/500/det.png',2,175);
INSERT INTO team VALUES(9,'Golden State Warriors','Golden State','Warriors','Warriors','GS','fdb927','1d428a','https://a.espncdn.com/i/teamlogos/nba/500/gs.png',2,176);
INSERT INTO team VALUES(10,'Houston Rockets','Houston','Rockets','Rockets','HOU','ce1141','000000','https://a.espncdn.com/i/teamlogos/nba/500/hou.png',2,177);
INSERT INTO team VALUES(11,'Indiana Pacers','Indiana','Pacers','Pacers','IND','0c2340','ffd520','https://a.espncdn.com/i/teamlogos/nba/500/ind.png',2,178);
INSERT INTO team VALUES(12,'LA Clippers','LA','Clippers','Clippers','LAC','12173f','c8102e','https://a.espncdn.com/i/teamlogos/nba/500/lac.png',2,179);
INSERT INTO team VALUES(13,'Los Angeles Lakers','Los Angeles','Lakers','Lakers','LAL','552583','fdb927','https://a.espncdn.com/i/teamlogos/nba/500/lal.png',2,180);
INSERT INTO team VALUES(14,'Miami Heat','Miami','Heat','Heat','MIA','98002e','000000','https://a.espncdn.com/i/teamlogos/nba/500/mia.png',2,181);
INSERT INTO team VALUES(15,'Milwaukee Bucks','Milwaukee','Bucks','Bucks','MIL','00471b','eee1c6','https://a.espncdn.com/i/teamlogos/nba/500/mil.png',2,182);
INSERT INTO team VALUES(16,'Minnesota Timberwolves','Minnesota','Timberwolves','Timberwolves','MIN','266092','79bc43','https://a.espncdn.com/i/teamlogos/nba/500/min.png',2,183);
INSERT INTO team VALUES(17,'Brooklyn Nets','Brooklyn','Nets','Nets','BKN','000000','ffffff','https://a.espncdn.com/i/teamlogos/nba/500/bkn.png',2,184);
INSERT INTO team VALUES(18,'New York Knicks','New York','Knicks','Knicks','NY','1d428a','f58426','https://a.espncdn.com/i/teamlogos/nba/500/ny.png',2,185);
INSERT INTO team VALUES(19,'Orlando Magic','Orlando','Magic','Magic','ORL','0150b5','9ca0a3','https://a.espncdn.com/i/teamlogos/nba/500/orl.png',2,186);
INSERT INTO team VALUES(20,'Philadelphia 76ers','Philadelphia','76ers','76ers','PHI','1d428a','e01234','https://a.espncdn.com/i/teamlogos/nba/500/phi.png',2,187);
INSERT INTO team VALUES(21,'Phoenix Suns','Phoenix','Suns','Suns','PHX','29127a','e56020','https://a.espncdn.com/i/teamlogos/nba/500/phx.png',2,188);
INSERT INTO team VALUES(22,'Portland Trail Blazers','Portland','Trail Blazers','Trail Blazers','POR','e03a3e','000000','https://a.espncdn.com/i/teamlogos/nba/500/por.png',2,189);
INSERT INTO team VALUES(23,'Sacramento Kings','Sacramento','Kings','Kings','SAC','5a2d81','6a7a82','https://a.espncdn.com/i/teamlogos/nba/500/sac.png',2,190);
INSERT INTO team VALUES(24,'San Antonio Spurs','San Antonio','Spurs','Spurs','SA','000000','c4ced4','https://a.espncdn.com/i/teamlogos/nba/500/sa.png',2,191);
INSERT INTO team VALUES(25,'Oklahoma City Thunder','Oklahoma City','Thunder','Thunder','OKC','007ac1','ef3b24','https://a.espncdn.com/i/teamlogos/nba/500/okc.png',2,192);
INSERT INTO team VALUES(26,'Utah Jazz','Utah','Jazz','Jazz','UTAH','4e008e','79a3dc','https://a.espncdn.com/i/teamlogos/nba/500/utah.png',2,193);
INSERT INTO team VALUES(27,'Washington Wizards','Washington','Wizards','Wizards','WSH','e31837','002b5c','https://a.espncdn.com/i/teamlogos/nba/500/wsh.png',2,194);
INSERT INTO team VALUES(28,'Toronto Raptors','Toronto','Raptors','Raptors','TOR','d91244','000000','https://a.espncdn.com/i/teamlogos/nba/500/tor.png',2,195);
INSERT INTO team VALUES(29,'Memphis Grizzlies','Memphis','Grizzlies','Grizzlies','MEM','5d76a9','12173f','https://a.espncdn.com/i/teamlogos/nba/500/mem.png',2,196);
INSERT INTO team VALUES(30,'Charlotte Hornets','Charlotte','Hornets','Hornets','CHA','008ca8','1d1060','https://a.espncdn.com/i/teamlogos/nba/500/cha.png',2,197);
INSERT INTO team VALUES(1,'Baltimore Orioles','Baltimore','Orioles','Orioles','BAL','df4601','000000','https://a.espncdn.com/i/teamlogos/mlb/500/bal.png',4,198);
INSERT INTO team VALUES(2,'Boston Red Sox','Boston','Red Sox','Red Sox','BOS','0d2b56','bd3039','https://a.espncdn.com/i/teamlogos/mlb/500/bos.png',4,199);
INSERT INTO team VALUES(3,'Los Angeles Angels','Los Angeles','Angels','Angels','LAA','ba0021','c4ced4','https://a.espncdn.com/i/teamlogos/mlb/500/laa.png',4,200);
INSERT INTO team VALUES(4,'Chicago White Sox','Chicago','White Sox','White Sox','CHW','000000','c4ced4','https://a.espncdn.com/i/teamlogos/mlb/500/chw.png',4,201);
INSERT INTO team VALUES(5,'Cleveland Guardians','Cleveland','Guardians','Guardians','CLE','002b5c','e31937','https://a.espncdn.com/i/teamlogos/mlb/500/cle.png',4,202);
INSERT INTO team VALUES(6,'Detroit Tigers','Detroit','Tigers','Tigers','DET','0a2240','ff4713','https://a.espncdn.com/i/teamlogos/mlb/500/det.png',4,203);
INSERT INTO team VALUES(7,'Kansas City Royals','Kansas City','Royals','Royals','KC','004687','7ab2dd','https://a.espncdn.com/i/teamlogos/mlb/500/kc.png',4,204);
INSERT INTO team VALUES(8,'Milwaukee Brewers','Milwaukee','Brewers','Brewers','MIL','13294b','ffc72c','https://a.espncdn.com/i/teamlogos/mlb/500/mil.png',4,205);
INSERT INTO team VALUES(9,'Minnesota Twins','Minnesota','Twins','Twins','MIN','031f40','e20e32','https://a.espncdn.com/i/teamlogos/mlb/500/min.png',4,206);
INSERT INTO team VALUES(10,'New York Yankees','New York','Yankees','Yankees','NYY','132448','c4ced4','https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png',4,207);
INSERT INTO team VALUES(11,'Athletics','Athletics','Athletics','Athletics','ATH','003831','efb21e','https://a.espncdn.com/i/teamlogos/mlb/500/ath.png',4,208);
INSERT INTO team VALUES(12,'Seattle Mariners','Seattle','Mariners','Mariners','SEA','005c5c','0c2c56','https://a.espncdn.com/i/teamlogos/mlb/500/sea.png',4,209);
INSERT INTO team VALUES(13,'Texas Rangers','Texas','Rangers','Rangers','TEX','003278','c0111f','https://a.espncdn.com/i/teamlogos/mlb/500/tex.png',4,210);
INSERT INTO team VALUES(14,'Toronto Blue Jays','Toronto','Blue Jays','Blue Jays','TOR','134a8e','6cace5','https://a.espncdn.com/i/teamlogos/mlb/500/tor.png',4,211);
INSERT INTO team VALUES(15,'Atlanta Braves','Atlanta','Braves','Braves','ATL','0c2340','ba0c2f','https://a.espncdn.com/i/teamlogos/mlb/500/atl.png',4,212);
INSERT INTO team VALUES(16,'Chicago Cubs','Chicago','Cubs','Cubs','CHC','0e3386','cc3433','https://a.espncdn.com/i/teamlogos/mlb/500/chc.png',4,213);
INSERT INTO team VALUES(17,'Cincinnati Reds','Cincinnati','Reds','Reds','CIN','c6011f','ffffff','https://a.espncdn.com/i/teamlogos/mlb/500/cin.png',4,214);
INSERT INTO team VALUES(18,'Houston Astros','Houston','Astros','Astros','HOU','002d62','eb6e1f','https://a.espncdn.com/i/teamlogos/mlb/500/hou.png',4,215);
INSERT INTO team VALUES(19,'Los Angeles Dodgers','Los Angeles','Dodgers','Dodgers','LAD','005a9c','ffffff','https://a.espncdn.com/i/teamlogos/mlb/500/lad.png',4,216);
INSERT INTO team VALUES(20,'Washington Nationals','Washington','Nationals','Nationals','WSH','ab0003','11225b','https://a.espncdn.com/i/teamlogos/mlb/500/wsh.png',4,217);
INSERT INTO team VALUES(21,'New York Mets','New York','Mets','Mets','NYM','002d72','ff5910','https://a.espncdn.com/i/teamlogos/mlb/500/nym.png',4,218);
INSERT INTO team VALUES(22,'Philadelphia Phillies','Philadelphia','Phillies','Phillies','PHI','e81828','003278','https://a.espncdn.com/i/teamlogos/mlb/500/phi.png',4,219);
INSERT INTO team VALUES(23,'Pittsburgh Pirates','Pittsburgh','Pirates','Pirates','PIT','000000','fdb827','https://a.espncdn.com/i/teamlogos/mlb/500/pit.png',4,220);
INSERT INTO team VALUES(24,'St. Louis Cardinals','St. Louis','Cardinals','Cardinals','STL','be0a14','001541','https://a.espncdn.com/i/teamlogos/mlb/500/stl.png',4,221);
INSERT INTO team VALUES(25,'San Diego Padres','San Diego','Padres','Padres','SD','2f241d','ffc425','https://a.espncdn.com/i/teamlogos/mlb/500/sd.png',4,222);
INSERT INTO team VALUES(26,'San Francisco Giants','San Francisco','Giants','Giants','SF','000000','fd5a1e','https://a.espncdn.com/i/teamlogos/mlb/500/sf.png',4,223);
INSERT INTO team VALUES(27,'Colorado Rockies','Colorado','Rockies','Rockies','COL','33006f','000000','https://a.espncdn.com/i/teamlogos/mlb/500/col.png',4,224);
INSERT INTO team VALUES(28,'Miami Marlins','Miami','Marlins','Marlins','MIA','00a3e0','000000','https://a.espncdn.com/i/teamlogos/mlb/500/mia.png',4,225);
INSERT INTO team VALUES(29,'Arizona Diamondbacks','Arizona','Diamondbacks','Diamondbacks','ARI','aa182c','000000','https://a.espncdn.com/i/teamlogos/mlb/500/ari.png',4,226);
INSERT INTO team VALUES(30,'Tampa Bay Rays','Tampa Bay','Rays','Rays','TB','092c5c','8fbce6','https://a.espncdn.com/i/teamlogos/mlb/500/tb.png',4,227);
INSERT INTO team VALUES(331,'Brighton & Hove Albion','Brighton & Hove Albion','Brighton & Hove Albion','Brighton','BHA','0606fa','ffdd00','https://a.espncdn.com/i/teamlogos/soccer/500/331.png',5,228);
INSERT INTO team VALUES(337,'Brentford','Brentford','Brentford','Brentford','BRE','f42727','f8ced9','https://a.espncdn.com/i/teamlogos/soccer/500/337.png',5,229);
INSERT INTO team VALUES(349,'AFC Bournemouth','AFC Bournemouth','AFC Bournemouth','Bournemouth','BOU','f42727','ffffff','https://a.espncdn.com/i/teamlogos/soccer/500/349.png',5,230);
INSERT INTO team VALUES(357,'Leeds United','Leeds United','Leeds United','Leeds','LEE','ffffff','ffff00','https://a.espncdn.com/i/teamlogos/soccer/500/357.png',5,231);
INSERT INTO team VALUES(359,'Arsenal','Arsenal','Arsenal','Arsenal','ARS','e20520','132257','https://a.espncdn.com/i/teamlogos/soccer/500/359.png',5,232);
INSERT INTO team VALUES(360,'Manchester United','Manchester United','Manchester United','Man United','MAN','da020e','144992','https://a.espncdn.com/i/teamlogos/soccer/500/360.png',5,233);
INSERT INTO team VALUES(361,'Newcastle United','Newcastle United','Newcastle United','Newcastle','NEW','000000','cd1937','https://a.espncdn.com/i/teamlogos/soccer/500/361.png',5,234);
INSERT INTO team VALUES(362,'Aston Villa','Aston Villa','Aston Villa','Aston Villa','AVL','660e36','ffffff','https://a.espncdn.com/i/teamlogos/soccer/500/362.png',5,235);
INSERT INTO team VALUES(363,'Chelsea','Chelsea','Chelsea','Chelsea','CHE','144992','ffeeee','https://a.espncdn.com/i/teamlogos/soccer/500/363.png',5,236);
INSERT INTO team VALUES(364,'Liverpool','Liverpool','Liverpool','Liverpool','LIV','d11317','132257','https://a.espncdn.com/i/teamlogos/soccer/500/364.png',5,237);
INSERT INTO team VALUES(366,'Sunderland','Sunderland','Sunderland','Sunderland','SUN','EB172B','87cced','https://a.espncdn.com/i/teamlogos/soccer/500/366.png',5,238);
INSERT INTO team VALUES(367,'Tottenham Hotspur','Tottenham Hotspur','Tottenham Hotspur','Spurs','TOT','ffffff','9bafd8','https://a.espncdn.com/i/teamlogos/soccer/500/367.png',5,239);
INSERT INTO team VALUES(368,'Everton','Everton','Everton','Everton','EVE','0606fa','132257','https://a.espncdn.com/i/teamlogos/soccer/500/368.png',5,240);
INSERT INTO team VALUES(370,'Fulham','Fulham','Fulham','Fulham','FUL','ffffff','d11317','https://a.espncdn.com/i/teamlogos/soccer/500/370.png',5,241);
INSERT INTO team VALUES(371,'West Ham United','West Ham United','West Ham United','West Ham','WHU','7c2c3b','000000','https://a.espncdn.com/i/teamlogos/soccer/500/371.png',5,242);
INSERT INTO team VALUES(379,'Burnley','Burnley','Burnley','Burnley','BUR','6C1D45','1a1a1a','https://a.espncdn.com/i/teamlogos/soccer/500/379.png',5,243);
INSERT INTO team VALUES(380,'Wolverhampton Wanderers','Wolverhampton Wanderers','Wolverhampton Wanderers','Wolves','WOL','fdb913','cd1937','https://a.espncdn.com/i/teamlogos/soccer/500/380.png',5,244);
INSERT INTO team VALUES(382,'Manchester City','Manchester City','Manchester City','Man City','MNC','99c5ea','e6ff00','https://a.espncdn.com/i/teamlogos/soccer/500/382.png',5,245);
INSERT INTO team VALUES(384,'Crystal Palace','Crystal Palace','Crystal Palace','C Palace','CRY','0202fb','ffdd00','https://a.espncdn.com/i/teamlogos/soccer/500/384.png',5,246);
INSERT INTO team VALUES(393,'Nottingham Forest','Nottingham Forest','Nottingham Forest','Nottm Forest','NFO','c8102e','132257','https://a.espncdn.com/i/teamlogos/soccer/500/393.png',5,247);

CREATE TABLE account_teams(
   id INTEGER PRIMARY KEY,
   account_id INTEGER,
   team_id INTEGER,
   FOREIGN KEY (account_id) REFERENCES account(id),
   FOREIGN KEY (team_id) REFERENCES team(id)
);
INSERT INTO account_teams VALUES(1,1,10);
INSERT INTO account_teams VALUES(2,1,58);
INSERT INTO account_teams VALUES(3,2,7);
INSERT INTO account_teams VALUES(4,2,67);
INSERT INTO account_teams VALUES(5,3,57);
INSERT INTO account_teams VALUES(6,3,213);
INSERT INTO account_teams VALUES(10,4,33);

COMMIT;
