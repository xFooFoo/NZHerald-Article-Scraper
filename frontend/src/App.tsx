import './App.css';
import React, { useState, ChangeEvent, FormEvent } from 'react';

function App() {
  const API_BASE_URL = 'https://nzherald.vercel.app' // 'http://localhost:5000';
  const [url, setUrl] = useState<string>('');
  const [fetchStatus, setFetchStatus] = useState<string>('');
  const [title, setTitle] = useState<string>('');
  const [content, setContent] = useState<string[]>([]);

  // Handle input changes
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    setUrl(event.target.value);
  };

  // Handle form submission
  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); // Prevent the default form submission (page reload)

    // Send data to Flask using fetch
    try {
      const response = await fetch(`${API_BASE_URL}/api/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url.trim(), // The value you want to send to Flask
        }),
      })

      const data = await response.json() // Get the response data
      setContent(data.content) // Store the received value in state
      setTitle(data.title)
      setFetchStatus(data.fetchStatus)
      setUrl('') // Clear the input after submission
    } catch (error) {
      console.error('Error:', error);
    }
  };


  return (
    <>
      <div className='mainContainer'>
        <h1>NZ Herald Article Scraper</h1>
        <form className='formContainer' onSubmit={handleSubmit}>
          <label>
            Enter the URL of the NZ Herald Article:
          </label>
          <input
            type="text"
            value={url}
            onChange={handleChange}
            placeholder="nzherald.co.nz/business/companies/tourism/mt-dobson-ski-area-for-sale-after-50-years-one-owner/LPUS2BT56FGK5MZ6ZPPHQ4N2XU/"
          />
          <button type="submit">Submit</button>
        </form>
        <h3>{fetchStatus}</h3>
        <div className='contentContainer'>
          <h1 className='titleStyle'>{title}</h1>
          {Array.isArray(content) && content.map((sentence, index) => (
            <p className='sentenceStyle' key={index}>{sentence}</p>
          ))}
        </div>
        <footer className='footerStyle'>
          <p>developed by foofoo for educational purposes - don't sue me pls</p>
        </footer>
      </div>
    </>
  );
}

export default App;
