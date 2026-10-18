from backend.app.websocket.protocol import validate_message


def test_websocket_message_validates_request_id():
    message = {"type": "chat", "request_id": "abc-123", "message": "Find hospitals near the city center"}
    validated = validate_message(message)
    assert validated["type"] == "chat"
    assert validated["request_id"] == "abc-123"
