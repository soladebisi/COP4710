from flask import Flask, render_template,flash, url_for, session, request, redirect, g
import sqlite3

DATABASE = 'team.db'

app = Flask(__name__)

# Set a secret key for sessions
app.secret_key = 'LebronJames'  # Use a random and secure secret key


# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries for easier access
    return conn

@app.route('/')
def home():
    # If user is logged in, show the base page
    if 'user' in session:
        return render_template('base.html', user=session['user'])
    else:
        # Otherwise, redirect to login
        return redirect(url_for('login'))

@app.route('/fav_teams')
def fav_teams():
    if 'user' in session:
        db = get_db_connection()
        user = session['user']

        # Fetch the allowed teams for this user
        user_data = db.execute("SELECT TeamsAllowed FROM User WHERE Username = ?", (user,)).fetchone()
        allowed_teams = user_data['TeamsAllowed'].split(',')  # Convert comma-separated string into a list

        # Retrieve the teams that are in the allowed list
        query = "SELECT * FROM Team WHERE Name IN ({})".format(",".join("?" * len(allowed_teams)))  # Construct dynamic query
        cursor = db.cursor()
        cursor.execute(query, allowed_teams)
        teams = cursor.fetchall()

        db.close()  # Close the connection
        return render_template("fav_teams.html", teams=teams)
    else:
        flash("You must be logged in to view this page.")
        return redirect(url_for('login'))


@app.route('/games')
def games():
    if 'user' in session:
        db = get_db_connection()
        cursor = db.cursor()

        # Get the current user
        user = session['user']

        # Fetch the allowed teams for this user
        user_data = db.execute("SELECT TeamsAllowed FROM User WHERE Username = ?", (user,)).fetchone()

        if user_data and user_data['TeamsAllowed']:
            allowed_teams = user_data['TeamsAllowed'].split(',')

            # Build the placeholder string with the correct count
            placeholder_string = ",".join("?" * len(allowed_teams))

            # Query to get games involving the allowed teams and their team names
            query = (
                f"SELECT Game.GameID, Game.Date, Game.Time, Game.Venue, "
                f"HomeTeam.Name AS HomeTeamName, AwayTeam.Name AS AwayTeamName, Game.Result "
                f"FROM Game "
                f"INNER JOIN Team AS HomeTeam ON Game.HomeTeamID = HomeTeam.TeamID "
                f"INNER JOIN Team AS AwayTeam ON Game.AwayTeamID = AwayTeam.TeamID "
                f"WHERE HomeTeam.Name IN ({placeholder_string}) OR AwayTeam.Name IN ({placeholder_string})"
            )

            cursor.execute(query, allowed_teams + allowed_teams)  # Doubled to account for both Home and Away teams
            games = cursor.fetchall()
        else:
            games = []

        db.close()

        return render_template("games.html", games=games)
    else:
        flash("You must be logged in to view this page.")
        return redirect(url_for('login'))


@app.route("/search_games", methods=["POST"])
def search_games():
    if request.method == "POST":
        # Get the team name from the form
        team_name = request.form['team_name']

        # Fetch the games where this team is the home or away team
        db = get_db_connection()
        query = """
        SELECT g.*, t1.Name as HomeTeamName, t2.Name as AwayTeamName
        FROM Game g
        JOIN Team t1 ON g.HomeTeamID = t1.TeamID
        JOIN Team t2 ON g.AwayTeamID = t2.TeamID
        WHERE t1.Name = ? OR t2.Name = ?
        """
        cursor = db.cursor()
        cursor.execute(query, (team_name, team_name))
        games = cursor.fetchall()

        db.close()

        # Render a new template for displaying search results
        return render_template("search_games.html", games=games)
    else:
        return "Method not allowed", 405


@app.route('/update_game/<int:game_id>', methods=['GET', 'POST'])
def update_game(game_id):
    db = get_db_connection()

    if request.method == 'POST':
        # Get the new result from the form
        new_result = request.form['result']

        # Update the result in the database
        db.execute("UPDATE Game SET Result = ? WHERE GameID = ?", (new_result, game_id))
        db.commit()  # Commit the changes
        db.close()  # Close the connection

        flash("Game result updated successfully!")
        return redirect(url_for('games'))  # Redirect to games page

    # If GET request, fetch the current game details
    game = db.execute("SELECT * FROM Game WHERE GameID = ?", (game_id,)).fetchone()
    db.close()

    if not game:
        flash("Game not found")
        return redirect(url_for('games'))

    return render_template('update_game.html', game=game)

@app.route('/teams')
def teams():
    db = get_db_connection()  # Connect to the SQLite database
    query = "SELECT * FROM Team"  # Query to retrieve all teams
    cursor = db.cursor()
    cursor.execute(query)
    teams = cursor.fetchall()  # Fetch all teams from the database
    db.close()  # Close the database connection

    # Render the 'teams.html' template with the list of teams
    return render_template("teams.html", teams=teams)

@app.route('/add_team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        # Get data from the form
        team_name = request.form['team_name']
        team_location = request.form['team_location']
        team_owner = request.form['team_owner']

        # Connect to the database and insert a new team
        db = get_db_connection()
        try:
            db.execute(
                "INSERT INTO Team (Name, Location, Owner) VALUES (?, ?, ?)",
                (team_name, team_location, team_owner)
            )
            db.commit()  # Commit the changes to the database
            flash("Team added successfully!")  # Provide feedback to the user
            return redirect(url_for('teams'))  # Redirect to the teams page
        except sqlite3.Error as e:
            flash("Failed to add the team. Please try again.")  # Error handling
            return redirect(url_for('add_team'))
        finally:
            db.close()  # Close the database connection

    # Render the form to add a new team
    return render_template("add_team.html")

@app.route('/delete_team', methods=['GET', 'POST'])
def delete_team():
    db = get_db_connection()

    if request.method == 'POST':
        # Get the team ID from the form
        team_id = request.form['team_id']

        # Attempt to delete the team
        try:
            db.execute("DELETE FROM Team WHERE TeamID = ?", (team_id,))
            db.commit()  # Commit the changes to the database
            flash("Team deleted successfully!")  # Feedback to the user
            return redirect(url_for('teams'))  # Redirect to the teams page
        except sqlite3.Error as e:
            flash("Failed to delete the team. Please try again.")  # Error handling
            return redirect(url_for('delete_team'))

    # Fetch all teams to display for deletion
    teams = db.execute("SELECT TeamID, Name FROM Team").fetchall()
    db.close()

    # Render the template to choose a team to delete
    return render_template("delete_team.html", teams=teams)


@app.route("/players")
def players():
    db = get_db_connection()
    cursor = db.cursor()
    query = "SELECT * FROM Player"
    cursor.execute(query)
    players = cursor.fetchall()
    return render_template("players.html", players=players)



# Route to display the login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']

        # Check user credentials in the database
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM User WHERE Username = ? AND Password = ?", (username, password)).fetchone()
        conn.close()

        if user:
            # Store user in session if valid
            session['user'] = username
            return redirect(url_for('home'))  # Redirect to the home page
        else:
            # Show error message if invalid login
            flash("Invalid username or password. Please try again.")

    # If not POST, render the login page
    return render_template('login.html')

# Route to logout
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove 'user' from the session
    flash("You have been logged out.")  # Provide feedback to the user
    return redirect(url_for('login'))  # Redirect to the login page
if __name__ == "__main__":
    app.run(debug=True)


