// Core Imports

// Component Imports
import { Col, Row, Card, Grid } from 'antd';
import ChatContainer from '../components/ChatContainer';

// Constant Declarations
const { useBreakpoint } = Grid

const MessagesScreen = () => {
  const screens = useBreakpoint();
  const isMobileSize = (screens.xs || screens.sm || screens.md) && !screens.lg;

  return(
    <Card style={{ marginLeft: isMobileSize ? '0' : '100px', marginRight: isMobileSize ? '0' : '100px' }}>
      <Row justify="center" align="middle">
        <Col xs={24} style={{
          display: 'flex',
          justifyContent: 'center'
        }}>
          <ChatContainer />
        </Col>
      </Row>
    </Card>

  )
}

export default MessagesScreen;
