# Conversational GIS widget

This widget is a placeholder scaffold for ArcGIS Experience Builder Developer Edition. It is designed to be placed into the correct custom widget directory for the target Experience Builder version and configured to connect to the FastAPI backend.

## Required installation

1. Copy this folder into the Developer Edition custom widget directory.
2. Register the widget in the Experience Builder project.
3. Bind the widget to the map widget using the configured mapWidgetId.
4. Provide the backendUrl via widget settings.
5. Preview or publish the Experience Builder app.

## Map handling

The widget expects the standard Experience Builder map widget API and should use the ArcGIS Maps SDK for JavaScript to add a dedicated result layer. The map integration is intentionally structured to avoid deleting unrelated layers from the user's map.
