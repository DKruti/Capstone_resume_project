import React from 'react';

function Message({ sender, content }) {
  return (
    <div className={`message ${sender}`}>
      <p>{content}</p>
    </div>
  );
}

export default Message;