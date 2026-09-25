# Victor Delgado
# 09/23/2025
# SDEV-245 Secure Coding

# Module 5: Secure Coding

This folder contains my examples for the Module 5 security assignment. Each file has a short explanation and the main code change.

## Broken Access Control

### 1. Profile access

File: [a01_broken_access_control.js](a01_broken_access_control.js)

I added a check before looking up the profile. It returns a 403 error if the signed-in user's ID does not match the requested profile ID.

```javascript
if (req.user.id !== req.params.userId) {
	return res.status(403).json({ error: 'Access denied' });
}
```

### 2. Account access

The Flask account example from the assignment does not currently have a matching implementation file in this folder.

## Cryptographic Failures

### 3. Password hashing in Java

File: [a02_cryptographic_failures.java](a02_cryptographic_failures.java)

I replaced MD5 with BCrypt. BCrypt adds a salt and makes password hashes harder to crack.

```java
return BCrypt.hashpw(password, BCrypt.gensalt(12));
```

### 4. Password hashing in Python

File: [a04_insecure_design.py](a04_insecure_design.py)

I used Werkzeug's PBKDF2-SHA-256 password hashing instead of SHA-1.

```python
return generate_password_hash(password, method='pbkdf2:sha256')
```

## Injection

### 5. SQL query

File: [a05_security_misconfiguration.java](a05_security_misconfiguration.java)

I changed the SQL query to use a placeholder and pass the username separately. This keeps the input from being treated as part of the SQL command.

```java
String query = "SELECT * FROM users WHERE username = ?";
PreparedStatement stmt = connection.prepareStatement(query);
stmt.setString(1, username);
```

### 6. MongoDB query

File: [a06_vulnerable_components.js](a06_vulnerable_components.js)

I convert the username input to a string before using it in the database query.

```javascript
const username = String(req.query.username);
db.collection('users').findOne(
	{ username: username },
	(err, user) => {
		if (err) {
			return res.status(500).json({ error: 'Server error' });
		}

		res.json(user);
	}
);
```

## Insecure Design

### 7. Password reset

File: [a07_authentication_failures.py](a07_authentication_failures.py)

I added a reset-token check before allowing the password to change. The new password is hashed before it is saved.

```python
user = User.verify_reset_token(token)
if not user:
	return "Invalid or expired token", 400

user.password = generate_password_hash(new_password)
```

## Software and Data Integrity Failures

### 8. External script

File: [a08_software_data_integrity.html](a08_software_data_integrity.html)

The prompt did not include a vulnerable version for this example. I added Subresource Integrity (SRI), which lets the browser check the script against its expected hash.

```html
<script
	src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
	integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"
	crossorigin="anonymous">
</script>
```

## Server-Side Request Forgery

### 9. URL request

File: [a09_logging_monitoring_failures.py](a09_logging_monitoring_failures.py)

I added a hostname check so the request is only allowed for the listed domain, and set a request timeout.

```python
ALLOWED_DOMAINS = ["example.com"]
parsed = urlparse(url)
if parsed.hostname not in ALLOWED_DOMAINS:
	raise ValueError("Domain not allowed")

response = requests.get(url, timeout=5, allow_redirects=False)
```

## Identification and Authentication Failures

### 10. Password check

File: [a10_ssrf.java](a10_ssrf.java)

I changed the check to use BCrypt to compare the entered password with the stored password hash.

```java
if (BCrypt.checkpw(inputPassword, user.getPassword())) {
	// Login success
}
```
