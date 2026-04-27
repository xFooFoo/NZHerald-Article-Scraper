import './App.css';
import { ContentItem, ContentItemImage, ContentItemText } from './types/ContentItem'
import { APIResponse } from './types/APIResponse'

import React, { useState, useEffect, ChangeEvent, FormEvent } from 'react';

function App() {
  // Dynamically set API_BASE_URL based on environment
  const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000' 
    : 'https://nzherald-server.vercel.app';
  const [url, setUrl] = useState<string>('');
  const [fetchStatus, setFetchStatus] = useState<string>('');
  const [title, setTitle] = useState<string>('');
  const [author, setAuthor] = useState<ContentItem[]>([]);
  const [content, setContent] = useState<ContentItem[]>([]);

  // Handle input changes
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    setUrl(event.target.value);
  };

  // Handle form submission
  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); // Prevent the default form submission (page reload)

    // Send data to Flask using fetch
    try {
      const response = await fetch(`${API_BASE_URL}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url.trim(), // The value you want to send to Flask
        }),
      })

      const data: APIResponse = await response.json() // Get the response data
      if (response.ok) {
        setContent(data.content || [])
        setAuthor(data.author?.filter((elem): elem is ContentItem => elem != null) ?? []
      )
        setTitle(data.title || '')
        setFetchStatus(data.fetchStatus)
        setUrl('') // Clear the input after submission
      } else {
        setFetchStatus(data.fetchStatus || 'An error occurred')
        setContent([])
        setAuthor([])
        setTitle('')
      }
    } catch (error) {
        console.error('Error:', error);
    }
  };

  useEffect(() => {
    document.title = "NZ Herald Article Scraper";
  }, []);

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
          {author.length > 0 &&
            (<div className='authorContainer'>
              {author
                .filter(item => item.type === 'image')
                .map((item, index) => (
                  <div key={index} className="authorImageContainer">
                    <figure>
                      <img className="authorImage" src={(item as ContentItemImage).src} srcSet={(item as ContentItemImage).srcset || ""} alt={(item as ContentItemImage).alt} />
                      {(item as ContentItemImage).caption && (
                        <figcaption className="authorCaption">{(item as ContentItemImage).caption}</figcaption>
                      )}
                    </figure>
                  </div>
                ))}
                <div className="authorTextContainer">
                  {author
                    .filter(item => item.type === 'text')
                    .map((item, index) => (
                      <p 
                        className="authorText"
                        key={index}
                        dangerouslySetInnerHTML={{ __html: (item as ContentItemText).content }}>
                      </p>
                    ))}
                </div>
            </div>)
          }
          {content.map((item, index) => {
            if (item.type === 'text') {
              return <p 
                      className='sentenceStyle'
                      key={index}
                      dangerouslySetInnerHTML={{ __html: item.content }}>
                     </p>;
            } 
            return null; // Fallback for unknown types, nothing will be rendered
          })}
        </div>
        <footer className='footerStyle'>
          <p>developed by foofoo for educational purposes - don't sue me pls</p>
        </footer>
      </div>
    </>
  );
}

export default App;
