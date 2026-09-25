"""A04: Insecure Design.

Original problem: the reset route changed a password without checking that the
user owned the account.
Change made: I made the user provide a valid reset token before changing a
password. The new password is hashed before it is saved.
"""

@app.route('/reset-password', methods=['POST'])
def reset_password():
    token = request.form['token']
    new_password = request.form['new_password']

    user = User.verify_reset_token(token)

    if not user:
        return "Invalid or expired token", 400

    user.password = generate_password_hash(new_password)
    db.session.commit()

    return "Password reset successful"
