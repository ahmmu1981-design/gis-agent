from backend.app.result_capture import ResultCapture


def test_result_capture_tracks_request_context():
    capture = ResultCapture()
    request_id = capture.begin_request("request-1")
    capture.set_answer(request_id, "Found 2 facilities.")
    capture.add_tool_result(request_id, {"geojson": {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [24.7, 39.9]}, "properties": {"name": "Alpha"}}]}})

    stored = capture.get_request(request_id)
    assert stored is not None
    assert stored["answer"] == "Found 2 facilities."
    assert len(stored["geojson"]["features"]) == 1
