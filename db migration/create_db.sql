--
-- Jack Miller
-- Nov 2025
--

CREATE SCHEMA fandom_site;

CREATE TABLE fandom_site.account(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE fandom_site.league(
    id SERIAL PRIMARY KEY,
    espn_league_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL, 
    logo_url VARCHAR(255) NOT NULL,
    current_season VARCHAR(50) NOT NULL,
    current_season_type VARCHAR(50) NOT NULL
);

CREATE TABLE fandom_site.team(
    id SERIAL PRIMARY KEY,
    espn_team_id INTEGER NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    short_display_name VARCHAR(50) NOT NULL,
    abbreviation VARCHAR(50) NOT NULL,
    color VARCHAR(50) NOT NULL,
    alternate_color VARCHAR(50),
    logo_url VARCHAR(255) NOT NULL,
    league_id INTEGER
);

CREATE TABLE fandom_site.account_team(
    id SERIAL PRIMARY KEY,
    account_id INTEGER,
    team_id INTEGER
);

-- FOREIGN KEYS --
ALTER TABLE fandom_site.team
    ADD CONSTRAINT fk_team_league
    FOREIGN KEY (league_id)
    REFERENCES fandom_site.league (id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

ALTER TABLE fandom_site.account_team
    ADD CONSTRAINT fk_account_team_account
    FOREIGN KEY (account_id)
    REFERENCES fandom_site.account (id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

ALTER TABLE fandom_site.account_team
    ADD CONSTRAINT fk_account_team_team
    FOREIGN KEY (team_id)
    REFERENCES fandom_site.team (id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;