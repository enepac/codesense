import React, { useEffect, useState } from "react";
import axios from "axios";

const App: React.FC = () => {
  const [backendData, setBackendData] = useState<string>("");

  useEffect(() => {
    axios.get("http://localhost:8000/api/test")
      .then((response) => {
        setBackendData(response.data.data);
      })
      .catch((error) => {
        console.error("Error connecting to the backend:", error);
      });
  }, []);

  return (
    <div className="App">
      <header>
        <h1>Welcome to CodeSense Frontend</h1>
        <p>{backendData ? `Backend says: ${backendData}` : "Loading..."}</p>
      </header>
    </div>
  );
};

export default App;
