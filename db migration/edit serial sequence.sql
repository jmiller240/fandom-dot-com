select * from fandom_site.account_team;

ALTER SEQUENCE fandom_site.account_team_id_seq RESTART WITH 11;

SELECT pg_get_serial_sequence('fandom_site.account_team', 'id');