import { Avatar, Button, Card, Col, Input, List, Row, Space, Typography } from 'antd'
import { useEffect, useMemo, useRef, useState } from 'react'
import { useConnectToRoomMutation, useGetMessagesQuery, useSendMessageMutation } from '../store/apiSlice/chatApi'

const SENDER_AVATAR_URL = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdZ9dExjxM5bzlQbdh_gLIt2cWMOzQmil8TA&s'
const CURRENT_USER = { name: 'User', avatarUrl: 'https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o=' }

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
            height: '70vh',
            width: '100%',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column-reverse',
            padding: '8px'
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
                  avatar={ <Avatar src={item.username !== CURRENT_USER.name ? SENDER_AVATAR_URL : CURRENT_USER.avatarUrl}/> }
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
            <Row gutter={[8, 8]} style={{ padding: '8px' }}>
              <Col xs={18} sm={20}>
                <Input
                  disabled={!isSendEnabled}
                  className="sendbox-input"
                  value={currentMessage}
                  onChange={(e) => {
                    setCurrentMessage(e.target.value)
                  }}
                  style={{
                    borderRadius: '4px'
                  }}
                  placeholder="Please type your text"
                  onPressEnter={() => {
                    handleOnSendMessage()
                  }}
                />
              </Col>
              <Col xs={6} sm={4}>
                <Button
                  style={{
                    width: '100%',
                    borderRadius: '4px'
                  }}
                  type="primary"
                  onClick={() => {
                    handleOnSendMessage()
                  }}
                  disabled={!isSendEnabled}
                >
                  Send
                </Button>
              </Col>
            </Row>
          </Space>
        </Col>
      </Row>
    </Card>
  )
}

export default ChatContainer
