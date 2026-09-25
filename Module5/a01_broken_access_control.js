//A01: Broken Access Control.

//Original problem: the requested user/account ID was trusted without checking
//whether the logged-in user was allowed to view it.

//Change made: I added a check to make sure the signed-in user can only view
// their own profile. If the IDs do not match, access is denied.

app.get('/profile/:userId', (req, res) => {
if (req.user.id !== req.params.userId) {
return res.status(403).json({ error: 'Access denied' });
}
 
User.findById(req.params.userId, (err, user) => {
if (err) return res.status(500).send(err);
res.json(user);
});
});
