import './App.css';
import { ContentItem, ContentItemImage, ContentItemLinkText, ContentItemText } from './types/ContentItem'
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

  function isText(item: ContentItem): item is ContentItemText {
    return item.type === "text";
  }

  function isLinkText(item: ContentItem): item is ContentItemLinkText {
    return item.type === "link-text";
  }

  function isImage(item: ContentItem): item is ContentItemImage {
    return item.type === "image";
  }

  const authorImage = author.find(item => item.type === "image") as ContentItemImage | undefined;

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
              <div className="authorImageContainer">
              {authorImage ?
                  (<><figure>
                    <img className="authorImage" src={authorImage.src} srcSet={authorImage.srcset || ""} alt={authorImage.alt} />
                    {authorImage.caption && (
                      <figcaption className="authorCaption">{authorImage.caption}</figcaption>
                    )}
                  </figure></>)
                : (<>{/*NZHerald SVG - fall back pic*/}
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 72" fill="#fff">
                    <path d="M25.15.636c-3.694 4.93-6.202 7.046-10.199 7.046-2.97 0-7.187-1.854-10.005-1.854a6.3 6.3 0 0 0-2.457.33 6.2 6.2 0 0 0-2.125 1.25L.008 6.86a11.74 11.74 0 0 1 3.75-4.419A12.1 12.1 0 0 1 9.21.306a70.5 70.5 0 0 1 9.691 1.987A9.3 9.3 0 0 0 24.74.075l.423.558zm-.608 6.697a11.1 11.1 0 0 0-2.597 7.254V39.86c0 7.125-5.009 11.827-11.18 15.263l-1.163-.334a12.7 12.7 0 0 0 2.774-4.19c.632-1.562.94-3.23.909-4.91v-3.356a9.9 9.9 0 0 0-3.85-.79 6.48 6.48 0 0 0-3.53.58 6.3 6.3 0 0 0-2.649 2.356l-.647-.61c.314-5.036 2.838-9.416 7.078-9.416a18 18 0 0 1 3.602.63v-4.93a8.2 8.2 0 0 0-3.683-.789 6.7 6.7 0 0 0-3.608.567 6.5 6.5 0 0 0-2.738 2.368l-.593-.622c.093-5.176 2.714-9.32 7.214-9.32 1.16.05 2.308.255 3.412.61V19.62c0-5.328 3.802-9.86 10.497-12.514l.775.247-.023-.019Z"/>
                    <path d="M37.079 57.023V3.348c-1.939.072-3.536 1.281-3.536 4.398v32.611a15.7 15.7 0 0 1-2.955 7.95 16.2 16.2 0 0 1-6.701 5.348 31.25 31.25 0 0 1 13.18 3.356zm22.41-31.735a5.16 5.16 0 0 0-1.329 1.92 5.06 5.06 0 0 0-.335 2.297v27.12c0 6.965-6.563 12.698-14.09 14.682l-.923-.486a15.6 15.6 0 0 0 4.65-5.451 15.3 15.3 0 0 0 1.688-6.907V28.99l-6.338-4.247-4.602 3.268v29.737l.167.095 3.101-2.87.965.883-9.303 8.604a21.6 21.6 0 0 0-12.944-3.413 20.3 20.3 0 0 0-13.269 3.5l-.492-.963a21.8 21.8 0 0 1 6.332-6.379 22.3 22.3 0 0 1 8.426-3.333 12.94 12.94 0 0 0 3.609-9.362V16.45a12.6 12.6 0 0 1 1.638-7.042 13 13 0 0 1 5.266-5.062A18.73 18.73 0 0 1 41.57.288a16.68 16.68 0 0 1 11.47 3.791l2.714-2.305.915.781-9.102 8.312a14.3 14.3 0 0 0-3.857-4.69 14.7 14.7 0 0 0-5.493-2.716v23.097a113 113 0 0 0 10.513-7.652c.69.38 8.354 4.876 10.765 6.234v.16l-.008-.012Z"/>
                  </svg>
                </>)}
              </div>
                
                <div className="authorTextContainer">
                  {author
                    .filter(isLinkText)
                    .map((item, index) => (
                      <a 
                        className="authorText"
                        href={item.href}
                        key={index}
                        dangerouslySetInnerHTML={{ __html: item.content }}>
                      </a>
                    ))}
                  {author
                    .filter(isText)
                    .map((item, index) => (
                      <p 
                        className="authorText"
                        key={index}
                        dangerouslySetInnerHTML={{ __html: item.content }}>
                      </p>
                    ))}
                </div>
            </div>)
          }
          {content.map((item, index) => {
            if (isText(item)) {
              return <p 
                      className='sentenceStyle'
                      key={index}
                      dangerouslySetInnerHTML={{ __html: item.content }}>
                     </p>;
            } else if (isImage(item)) {
              return (
                <figure key={index}>
                  <img src={item.src} srcSet={item.srcset || ""} alt={item.alt} />
                  {item.caption && (
                    <figcaption>{item.caption}</figcaption>
                  )}
                </figure>
              )
            } else if (isLinkText(item)) {
              return <a 
                  className='sentenceStyle'
                  href={item.href}
                  target="_blank"
                  rel="noreferrer">
                  {item.content}
                  </a>;
            }
            return null; // Fallback for unknown types, nothing will be rendered
          })}
        </div>
        <footer className='footerStyle'>
          <p>This website is an independent project and is not affiliated with, endorsed by, or sponsored by NZ Herald.
            All trademarks, logos, and content are the property of their respective owners.</p>
          <p>Any referenced articles or materials are displayed solely at the direction of the user and for informational purposes.</p>
          <p>Developed by foofoo for educational purposes - don't sue me pls</p>
        </footer>
      </div>
    </>
  );
}

export default App;
