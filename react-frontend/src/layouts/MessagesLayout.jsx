import { Layout, Menu } from 'antd';
import { Content, Footer, Header } from 'antd/es/layout/layout';
import PropTypes from 'prop-types';

const MessagesLayout = ({ children }) => {
  return (
    <Layout style={{ width: '100%' }}>
      <Header >
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['messagesPage']}
          items={[
            {
              key: 'messagesPage',
              label: 'Messages'
            }
          ]}
        />
      </Header>
      <Content >
        {children}
      </Content>
      <Footer
        style={{
          textAlign: 'center'
        }}
      >
        Intelligencia FE Assessment ©{new Date().getFullYear()} Created by Yannis Vitalis
      </Footer>
    </Layout>
  )
}

MessagesLayout.propTypes = {
  children: PropTypes.element
};

export default MessagesLayout;
