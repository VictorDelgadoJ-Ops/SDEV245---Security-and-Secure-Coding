//A03: Injection.

//Original problem: adding the username directly to SQL lets input change the
//query.
//Change made: I used a prepared statement so the username is handled as data
//instead of being added directly to the SQL command.


String username = request.getParameter("username");

String query = "SELECT * FROM users WHERE username = ?";
PreparedStatement stmt = connection.prepareStatement(query);
stmt.setString(1, username);

ResultSet rs = stmt.executeQuery();