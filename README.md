# cloaked-spice

This is a Flask app that listens for Github's hook and verifies it. It does the
deployment and returns 'OK'. In case of validation failing, it returns 404.

Before you run the app, you need to create an `application.cfg` file inside the
instance directory with `GITHUB_SECRET` key to store your github secret.
