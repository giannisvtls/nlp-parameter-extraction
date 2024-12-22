// Core Imports
import { lazy, memo, Suspense, useCallback, useEffect, useMemo, useState } from 'react';
import { useGetMessagesQuery } from '../store/apiSlice/chatApi';
import PropTypes from 'prop-types';

// Component Imports
import { Button, Row, Typography, Popover, Grid, Table, message, Skeleton } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

// Lazy loaded components
const SynonymsList = memo(lazy(() => import('./SynonymsList')))

// Constant Declarations
const { Column } = Table
const { Text } = Typography
const { useBreakpoint } = Grid

const MessagesTable = ({ searchQuery }) => {
  const [currentPage, setCurrentPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)
  const screens = useBreakpoint();
  const isMobileSize = (screens.xs || screens.sm || screens.md) && !screens.lg;

  const { data: messages, isLoading: isLoadingMessages, error: fetchMessagesError } = useGetMessagesQuery({
    page: currentPage,
    page_size: pageSize,
    search: searchQuery
  });

  const errorMessage = fetchMessagesError?.error;

  useEffect(() => {
    if (errorMessage) {
      message.error(errorMessage);
    }
  }, [errorMessage])

  useEffect(() => {
    setCurrentPage(1)
  }, [searchQuery])

  const totalMessages = useMemo(() => {
    return Math.ceil(messages?.count / pageSize)
  }, [messages, pageSize])

  const synonymsColumn = useMemo(() => (
    <Column
      title="Synonyms"
      dataIndex="synonyms"
      hidden={isMobileSize}
      ellipsis={true}
      render={(_text, record) => {
        const allSynonyms = record.synonyms.map(synonym => synonym.label).join(', ');

        return allSynonyms ? (
          <Row align="middle" style={{ display: 'flex', width: '100%' }}>
            <Text style={{ flex: 1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {allSynonyms}
            </Text>
            {record.synonyms.length > 0 && (
              <Popover
                placement="top"
                overlayStyle={{ maxWidth: 300 }}
                title="All Synonyms"
                trigger="click"
                content={
                  <Suspense fallback={<Skeleton />}>
                    <SynonymsList synonyms={record.synonyms} />
                  </Suspense>
                }
              >
                <Button size="small" type="text" style={{ marginLeft: 8 }} icon={<PlusOutlined />}/>
              </Popover>
            )}
          </Row>
        ) : (
          <Text type="secondary" italic>
            No synonyms found
          </Text>
        );
      }}
    />
  ), [isMobileSize, messages])

  const expandedRowRender = useCallback(
    (record) => (
      <Suspense fallback={<Skeleton />}>
        <SynonymsList synonyms={record.synonyms} />
      </Suspense>
    ), []
  );

  return (
    <Table
      loading={isLoadingMessages}
      pagination={{
        total: totalMessages || 0,
        defaultCurrent: 1,
        current: currentPage,
        pageSize: messages?.results.length || 0,
        size: 'default',
        onChange: (page, pageSize) => {
          setCurrentPage(page)
          setPageSize(pageSize)
        }
      }}
      expandable={{
        columnTitle: isMobileSize ? 'Synonyms': '',
        expandedRowRender: expandedRowRender,
        rowExpandable: () => isMobileSize
      }}
      rowKey={(row) => row.id}
      dataSource={messages?.results}
    >
      <Column
        title="Term"
        dataIndex="term"
        width={isMobileSize ? '80%' : '40%'}
      />

      {synonymsColumn}
    </Table>
  )
}

MessagesTable.propTypes = {
  searchQuery: PropTypes.string
};

export default MessagesTable
