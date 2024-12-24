// Core Imports
import { useCallback, useState } from 'react';

// Component Imports
import { Col, Row, Typography, Card, Grid } from 'antd';
import SearchForm from '../components/SearchForm';
import ChatComponent from '../components/ChatComponent';
import ChatContainer from '../components/ChatContainer';

// Constant Declarations
const { Title } = Typography
const { useBreakpoint } = Grid

const MessagesScreen = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const screens = useBreakpoint();
  const isMobileSize = (screens.xs || screens.sm || screens.md) && !screens.lg;

  const handleSearchChange = useCallback((query) => {
    setSearchQuery(query);
  }, []);

  return(
    <Card style={{ marginLeft: isMobileSize ? '0' : '100px', marginRight: isMobileSize ? '0' : '100px' }}>
      <Row align="middle" justify="space-between">
        <Col >
          <SearchForm setSearchQuery={handleSearchChange}></SearchForm>
        </Col>
        <Col >
          <Title>EFO Term Table with search</Title>
        </Col>
      </Row>
      <Row justify="center" align="middle">
        <Col xs={24} style={{
          display: 'flex',
          justifyContent: 'center'
        }}>
          <ChatContainer />
        </Col>
      </Row>
      {/* <ChatComponent
        currentUser={{ name: 'Giannis', avatarUrl: 'https://public-storage-development.s3.eu-central-1.amazonaws.com/6051da0573c0fe08d75193d4/ZV49Oxa-pokemon.jpg' }}
        defaultAvatar="/default-avatar.png"
      /> */}
    </Card>

  )
}

export default MessagesScreen;
