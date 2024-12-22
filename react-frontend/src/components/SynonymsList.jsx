// Core Imports
import { useMemo } from 'react';
import PropTypes from 'prop-types';

// Component Imports
import { List } from 'antd'

const SynonymsList = ({ synonyms }) => {
  const memoizedSynonyms = useMemo(() => synonyms, [synonyms]);

  const renderSynonym = (synonym) => (
    <List.Item style={{ textAlign: 'left' }} key={synonym.id || synonym.label}>
      {synonym.label}
    </List.Item>
  );

  return (
    <div style={{ maxHeight: 200, overflowY: 'auto' }}>
      <List
        size="large"
        rowKey={'id'}
        dataSource={memoizedSynonyms}
        renderItem={renderSynonym}
      />
    </div>
  )
}

SynonymsList.propTypes = {
  synonyms: PropTypes.array
};

export default SynonymsList
