import React, { useState } from 'react';

function InputArea() {
  const [input, setInput] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Handle the message submission
    const url = "http://127.0.0.1:8000/query"
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type' : 'application/json',
        },
        body: JSON.stringify({message: input}),
      });

      if (response.ok) {
        console.log('Message sent successfuly');
        setInput(''); // Clear the input after successful submission
        const data = await response.json();
        setInput(data.response)
      } else {
        console.log("Error sending message inside try:", response.status);
      }
    
    } catch (error) {
      console.error('Error sending message inside catch: ', error);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      // submit the form
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="input-area">
        <textarea type="text" value={input}  onChange={(e) => setInput(e.target.value)} onKeyDown={handleKeyDown} />
        <button type="submit">
            <span className='icon-container'>
                <img src="./send_icon.svg" alt="Send Icon" width="16" height="16" />
            </span>
        </button>
    </form>
  );
}

export default InputArea;
