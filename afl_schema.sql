CREATE TABLE game (
    round INTEGER,
    agoals INTEGER,
    game_id INTEGER PRIMARY KEY,
    unixtime INTEGER,
    date TEXT,
    hteamid INTEGER,
    ateam TEXT,
    tz TEXT,
    venue TEXT,
    localtime TEXT,
    winner TEXT, -- draw if winner is null
    complete INTEGER,
    hbehinds INTEGER,
    ascore INTEGER,
    roundname TEXT,
    year INTEGER,
    is_final INTEGER,
    hscore INTEGER,
    abehinds INTEGER,
    is_grand_final INTEGER,
    updated TEXT,
    hgoals INTEGER,
    timestr TEXT,
    hteam TEXT,
    winnerteamid REAL,
    ateamid INTEGER
);
CREATE TABLE player_stats (
    round INT,
    year INT,
    player_id INT,
    player_name VARCHAR(255),
    team VARCHAR(50),
    opponent VARCHAR(50),
    kicks INT,
    marks INT,
    hand_balls INT,
    disp INT, -- should be kicks + hand_balls
    goals INT, -- goals are worth 6 points
    behinds INT, -- behinds are worth 1 point
    hit_outs INT, -- ruckmen mostly only get hit outs
    tackles INT,
    rebounds INT,
    inside_50 INT,
    clearances INT,
    clangers INT,
    frees_for INT,
    frees_against INT,
    brownlow INT, -- most brownlow votes in a season without suspension wins the brownlow medal
    contested_possessions INT,
    uncontested_possessions INT,
    contested_marks INT,
    marks_inside_50 INT,
    one_percenters INT,
    bounces INT,
    goal_assists INT,
    percent_time_played INT,
    game_id INT,
    PRIMARY KEY (round, year, player_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id)
);
