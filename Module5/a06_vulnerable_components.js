//A03: Injection.

//Original problem: the query used the raw request value, which could contain
//MongoDB operators instead of a username.
//Change made: I convert the username input to a string before using it in the
//MongoDB query.


app.get('/user', (req, res) => {
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
});