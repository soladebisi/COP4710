import sqlite3

# Database file name
DATABASE = 'team.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(DATABASE)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# drop User table from database
try:
    conn.execute('''Drop table User''')
    # save changes
    conn.commit()
    print('User table dropped.')
except:
    print('User table did not exist')

# Create the User table
cursor.execute('''
CREATE TABLE User (
    UserID INTEGER PRIMARY KEY,
    Username TEXT,
    Password TEXT,
    Email TEXT,
    TeamsAllowed TEXT
)
''')

# drop Team table from database
try:
    conn.execute('''Drop table Team''')
    # save changes
    conn.commit()
    print('Team table dropped.')
except:
    print('Team table did not exist')

# Create the Team table
cursor.execute('''
CREATE TABLE Team (
    TeamID INTEGER PRIMARY KEY,
    Name TEXT,
    Location TEXT,
    Owner TEXT
)
''')

# drop Player table from database
try:
    conn.execute('''Drop table Player''')
    # save changes
    conn.commit()
    print('Player table dropped.')
except:
    print('Player table did not exist')

# Create the Player table
cursor.execute('''
CREATE TABLE Player (
    PlayerID INTEGER PRIMARY KEY,
    Name TEXT,
    Position TEXT,
    TeamID INTEGER,
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID)
)
''')

# drop Game table from database
try:
    conn.execute('''Drop table Game''')
    # save changes
    conn.commit()
    print('Game table dropped.')
except:
    print('Game table did not exist')

# Create the Game table
cursor.execute('''
CREATE TABLE Game (
    GameID INTEGER PRIMARY KEY,
    Date TEXT,
    Time TEXT,
    Venue TEXT,
    HomeTeamID INTEGER,
    AwayTeamID INTEGER,
    Result TEXT,
    FOREIGN KEY (HomeTeamID) REFERENCES Team(TeamID),
    FOREIGN KEY (AwayTeamID) REFERENCES Team(TeamID)
)
''')

# drop TeamStatistics table from database
try:
    conn.execute('''Drop table TeamStatistics''')
    # save changes
    conn.commit()
    print('TeamStatistics table dropped.')
except:
    print('TeamStatistics table did not exist')

# Create the TeamStatistics table
cursor.execute('''
CREATE TABLE TeamStatistics (
    TeamID INTEGER,
    PointsScoredPerGame REAL,
    PointsAllowedPerGame REAL,
    FieldGoalPercentage REAL,
    ThreePointPercentage REAL,
    FreeThrowPercentage REAL,
    TurnoversPerGame REAL,
    ReboundsPerGame REAL,
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID)
)
''')

# drop TeamStatistics table from database
try:
    conn.execute('''Drop table PlayerStatistics''')
    # save changes
    conn.commit()
    print('PlayerStatistics table dropped.')
except:
    print('PlayerStatistics table did not exist')

# Create the PlayerStatistics table
cursor.execute('''
CREATE TABLE PlayerStatistics (
    PlayerID INTEGER,
    PointsPerGame REAL,
    AssistsPerGame REAL,
    StealsPerGame REAL,
    BlocksPerGame REAL,
    ReboundsPerGame REAL,
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
)
''')

conn.commit()


# Insert data into the User table
cursor.execute("INSERT INTO User (Username, Password, Email, TeamsAllowed) VALUES ('sola', 'adebisi', 'sola@gmail.com', 'Lakers,Hawks')")
cursor.execute("INSERT INTO User (Username, Password, Email, TeamsAllowed) VALUES ('kayode', 'adebisi', 'kayode@gmail.com', 'Knicks,Nets')")
cursor.execute("INSERT INTO User (Username, Password, Email, TeamsAllowed) VALUES ('toluwani', 'adebisi', 'toluwani@gmail.com', 'Warriors,Mavericks')")

# Insert data into the Team table
cursor.execute("INSERT INTO Team (Name, Location, Owner) VALUES ('Lakers', 'Los Angeles', 'Jeanie Buss')")
cursor.execute("INSERT INTO Team (Name, Location, Owner) VALUES ('Hawks', 'Atlanta', 'Tony Ressler')")
cursor.execute("INSERT INTO Team (Name, Location, Owner) VALUES ('Knicks', 'New York', 'James Dolan')")
cursor.execute("INSERT INTO Team (Name, Location, Owner) VALUES ('Mavericks', 'Dallas', 'Mark Cuban')")
cursor.execute("INSERT INTO Team (Name, Location, Owner) VALUES ('Nets', 'Brooklyn', 'Joe Tsai')")
cursor.execute("INSERT INTO Team (Name, Location, Owner) VALUES ('Warriors', 'Golden State', 'Joe Lacob')")

# Insert data into the Player table
cursor.execute("INSERT INTO Player (Name, Position, TeamID) VALUES ('LeBron James', 'Forward', 1)")
cursor.execute("INSERT INTO Player (Name, Position, TeamID) VALUES ('Stephen Curry', 'Guard', 2)")

# Insert data into the Game table
cursor.execute("INSERT INTO Game (Date, Time, Venue, HomeTeamID, AwayTeamID, Result) VALUES ('2023-11-10', '7:00 PM', 'Staples Center', 1, 2, '102-99')")
cursor.execute("INSERT INTO Game (Date, Time, Venue, HomeTeamID, AwayTeamID, Result) VALUES ('2023-12-15', '8:00 PM', 'State Farm Arena', 2, 1, '110-108')")
cursor.execute("INSERT INTO Game (Date, Time, Venue, HomeTeamID, AwayTeamID, Result) VALUES ('2023-12-15', '8:00 PM', 'Madison Square Garden', 3, 1, '110-108')")
cursor.execute("INSERT INTO Game (Date, Time, Venue, HomeTeamID, AwayTeamID, Result) VALUES ('2023-12-15', '8:00 PM', 'Chase Center', 6, 3, '110-108')")
cursor.execute("INSERT INTO Game (Date, Time, Venue, HomeTeamID, AwayTeamID, Result) VALUES ('2023-12-15', '8:00 PM', 'Barclays Center', 5, 4, '110-108')")
cursor.execute("INSERT INTO Game (Date, Time, Venue, HomeTeamID, AwayTeamID, Result) VALUES ('2023-12-15', '8:00 PM', 'American Airline Arena', 4, 6, '110-108')")



# Insert data into the TeamStatistics table
cursor.execute("INSERT INTO TeamStatistics (TeamID, PointsScoredPerGame, PointsAllowedPerGame, FieldGoalPercentage, ThreePointPercentage, FreeThrowPercentage, TurnoversPerGame, ReboundsPerGame) VALUES (1, 102.5, 100.3, 48.2, 36.7, 78.4, 14.2, 42.5)")
cursor.execute("INSERT INTO TeamStatistics (TeamID, PointsScoredPerGame, PointsAllowedPerGame, FieldGoalPercentage, ThreePointPercentage, FreeThrowPercentage, TurnoversPerGame, ReboundsPerGame) VALUES (2, 110.3, 106.5, 50.0, 40.5, 80.0, 12.5, 45.0)")

# Insert data into the PlayerStatistics table
cursor.execute("INSERT INTO PlayerStatistics (PlayerID, PointsPerGame, AssistsPerGame, StealsPerGame, BlocksPerGame, ReboundsPerGame) VALUES (1, 27.3, 7.1, 1.2, 0.6, 7.8)")
cursor.execute("INSERT INTO PlayerStatistics (PlayerID, PointsPerGame, AssistsPerGame, StealsPerGame, BlocksPerGame, ReboundsPerGame) VALUES (2, 31.2, 6.3, 1.7, 0.4, 5.5)")

# Commit the changes and close the connection
conn.commit()
conn.close()
