import React from 'react';

export default function Setting(props: any) {
  return (
    <div>
      <h4>Conversational GIS Settings</h4>
      <p>Configure the backend URL and the map widget connection for your Experience Builder app.</p>
      <ul>
        <li>Backend URL: http://localhost:8000/api</li>
        <li>Map widget association: bind to the native Experience Builder map widget</li>
      </ul>
    </div>
  );
}
