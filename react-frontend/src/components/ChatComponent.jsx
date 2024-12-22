import { useEffect, useState } from 'react';
import { Avatar } from 'antd';
import PropTypes from 'prop-types';
import { useConnectToRoomMutation, useGetMessagesQuery, useSendMessageMutation } from '../store/apiSlice/chatApi';

// ChatMessage component remains the same
const ChatMessage = ({ content, isReceiver, avatarUrl, timestamp }) => (
  <div className={`flex items-center gap-3 mb-4 ${isReceiver ? 'justify-end' : 'justify-start'}`}>
    {!isReceiver && (
      <Avatar src={avatarUrl} size={40} className="flex-shrink-0" />
    )}
    <div className="flex flex-col">
      <div
        className={`px-4 py-2 rounded-2xl max-w-md ${
          isReceiver
            ? 'bg-teal-500/20 text-teal-400'
            : 'bg-teal-500/20 text-teal-400'
        }`}
      >
        {content}
      </div>
      {timestamp && (
        <span className="text-xs text-gray-400 mt-1">
          {new Date(timestamp).toLocaleTimeString()}
        </span>
      )}
    </div>
    {isReceiver && (
      <Avatar src={avatarUrl} size={40} className="flex-shrink-0" />
    )}
  </div>
);

ChatMessage.propTypes = {
  content: PropTypes.string.isRequired,
  isReceiver: PropTypes.bool.isRequired,
  avatarUrl: PropTypes.string.isRequired,
  timestamp: PropTypes.string
};

ChatMessage.defaultProps = {
  timestamp: null
};

const ChatComponent = ({ currentUser, defaultAvatar }) => {
  const [messageInput, setMessageInput] = useState('');
  const roomName = 'general'; // You can make this dynamic if needed

  const [connectToRoom] = useConnectToRoomMutation();
  const { data: messages } = useGetMessagesQuery(roomName);
  const [sendMessage] = useSendMessageMutation();

  useEffect(() => {
    connectToRoom({ roomName });
  }, [connectToRoom, roomName]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!messageInput.trim()) {
      return;
    }

    try {
      await sendMessage({
        message: messageInput,
        username: currentUser.name,
        roomName,
        metadata: {
          avatar: currentUser.avatarUrl,
          timestamp: new Date().toISOString()
        }
      });
      setMessageInput('');
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  // Ensure messages is an array before mapping
  const messagesList = messages?.entities ? Object.values(messages.entities) : [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-6">
      <div className="max-w-3xl mx-auto flex flex-col h-[calc(100vh-4rem)]">
        <div className="flex-grow overflow-y-auto p-4">
          {messagesList.map((message) => (
            <ChatMessage
              key={message.id}
              content={message.message}
              isReceiver={message.username !== currentUser.name}
              avatarUrl={message.metadata?.avatar || defaultAvatar}
              timestamp={message.metadata?.timestamp}
            />
          ))}
        </div>
        <form onSubmit={handleSendMessage} className="p-4 bg-gray-800/50 rounded-lg">
          <div className="flex gap-2">
            <input
              type="text"
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              className="flex-grow px-4 py-2 bg-gray-700/50 text-teal-400 rounded-full border-none focus:ring-2 focus:ring-teal-500 focus:outline-none"
              placeholder="Type a message..."
            />
            <button
              type="submit"
              className="px-6 py-2 bg-teal-500/20 text-teal-400 rounded-full hover:bg-teal-500/30 transition-colors"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

ChatComponent.propTypes = {
  currentUser: PropTypes.shape({
    name: PropTypes.string.isRequired,
    avatarUrl: PropTypes.string.isRequired
  }).isRequired,
  defaultAvatar: PropTypes.string
};

ChatComponent.defaultProps = {
  defaultAvatar: '/api/placeholder/40/40'
};

export default ChatComponent;
