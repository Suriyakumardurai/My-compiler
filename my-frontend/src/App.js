import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');

  const handleCompile = async () => {
    try {
      const response = await axios.post('http://localhost:5000/compile', { code });
      setOutput(response.data.stdout || response.data.stderr);
    } catch (error) {
      setOutput('Error: ' + error.message);
    }
  };

  return (
    <div className="App">
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Write your Python code here"
      ></textarea>
      <button onClick={handleCompile}>Compile</button>
      <pre>{output}</pre>
    </div>
  );
}

export default App;
