# Pipeline function for social-auth to mark newly created social users in session.

def mark_new_social_user(strategy, backend, user=None, is_new=False, *args, **kwargs):
    """
    If this login resulted in creating a new user, set session flags so that
    the post-login view can redirect the client to a registration page.
    """
    if is_new:
        # strategy.session_set stores data into the session for later retrieval
        strategy.session_set("social_is_new", True)
        # backend.name gives provider name like 'google-oauth2' or 'github'
        strategy.session_set("social_provider", getattr(backend, "name", None))
