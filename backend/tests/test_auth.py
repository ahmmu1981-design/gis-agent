from backend.app.auth.sessions import SessionStore


def test_session_expiration():
    store = SessionStore(expiration_seconds=0)
    token = store.create_session("user@example.com")
    assert token is not None
    assert store.get_session(token) is None
