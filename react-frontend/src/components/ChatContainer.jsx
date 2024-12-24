import { Avatar, Button, Card, Col, Input, List, Row, Space, Typography } from 'antd'
import { useEffect, useMemo, useRef, useState } from 'react'
import { useConnectToRoomMutation, useGetMessagesQuery, useSendMessageMutation } from '../store/apiSlice/chatApi'

const SENDER_AVATAR_URL = 'https://public-storage-development.s3.eu-central-1.amazonaws.com/6051da0573c0fe08d75193d4/ZV49Oxa-pokemon.jpg'
const CURRENT_USER = { name: 'Giannis', avatarUrl: 'https://public-storage-development.s3.eu-central-1.amazonaws.com/6051da0573c0fe08d75193d4/ZV49Oxa-pokemon.jpg' }

const ChatContainer = () => {

  const [currentMessage, setCurrentMessage] = useState('');
  const messagesEndRef = useRef(null);
  const [isSendEnabled, setIsSendEnabled] = useState(true);

  const roomName = 'general'; // You can make this dynamic if needed

  const [connectToRoom] = useConnectToRoomMutation();
  const { data: messages } = useGetMessagesQuery(roomName);
  const [sendMessage] = useSendMessageMutation();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    connectToRoom({ roomName });
  }, [connectToRoom, roomName]);

  const handleOnSendMessage = async (e) => {

    if(!isSendEnabled) {
      return;
    }

    if (!currentMessage.trim()) {
      return;
    }

    try {
      await sendMessage({
        message: currentMessage,
        username: CURRENT_USER.name,
        roomName,
        metadata: {
          avatar: CURRENT_USER.avatarUrl,
          timestamp: new Date().toISOString()
        }
      });
      setCurrentMessage('');
      setIsSendEnabled(false);
    } catch (error) {
      console.error('Failed to send message:', error);
      setIsSendEnabled(true);
    }
  };

  // Ensure messages is an array before mapping
  const messagesList = useMemo(() => {
    setIsSendEnabled(true)
    return messages?.entities ? Object.values(messages.entities) : []
  }, [messages?.entities]);

  return (
    <Card
      className="message-container-card"
      bodyStyle={{
        padding: 0
      }}
    >
      <Row
      >
        <Col xs={24}
          style={{
            minHeight: '500px',
            width: '100%',
            maxHeight: '500px',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column-reverse',
            overflow: 'auto'

          }}
        >
          <div ref={messagesEndRef} />

          <List
            className="message-container"
            locale={{
              emptyText: 'Ask a Question'
            }}
            itemLayout="horizontal"
            dataSource={messagesList}
            renderItem={(item) => (
              <List.Item key={item.id} className={item.username !== CURRENT_USER.name ? 'incoming-message' : 'outgoing-message'}>
                <List.Item.Meta
                  avatar={ <Avatar src={SENDER_AVATAR_URL}/> }
                  title={item.message}
                  description={
                    <Space direction="vertical" size={0}>
                      <Space.Compact>
                        <Typography.Text style={{ fontSize: '12px' }}>
                            Sender:
                        </Typography.Text>
                        <Typography.Text style={{ marginLeft: '4px', fontSize: '12px' }}>
                          {item.username}
                        </Typography.Text>
                      </Space.Compact>
                      <Space.Compact>
                        <Typography.Text style={{ fontSize: '12px' }}>
                            Date:
                        </Typography.Text>
                        <Typography.Text style={{ marginLeft: '4px', fontSize: '12px' }}>
                          {item.timestamp}
                        </Typography.Text>
                      </Space.Compact>
                    </Space>
                  }
                />
              </List.Item>
            )}
          />

        </Col>
        <Col xs={24}>
          <Space
            style={{
              width: '100%'
            }}
            size={0}
            direction="vertical"
          >
            <Space.Compact
              style={{
                width: '100%'
              }}
            >
              <Input
                disabled={!isSendEnabled}
                className="sendbox-input"
                value={currentMessage}
                onChange={(e) => {
                  setCurrentMessage(e.target.value)
                }}
                style={{
                  borderRadius: 0
                }}
                placeholder="Please type your text"
                onPressEnter={() => {
                  handleOnSendMessage()
                }}
              />
              <Button
                style={{
                  borderRadius: 0
                }}

                type="primary"
                onClick={() => {
                  handleOnSendMessage()
                }}
                disabled={!isSendEnabled}
              >
                Send
              </Button>
            </Space.Compact>
          </Space>
        </Col>
      </Row>
    </Card>
  )
}

export default ChatContainer
