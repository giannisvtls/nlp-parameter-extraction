// Component Imports
import { Form, Input } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import PropTypes from 'prop-types';

// Misc Imports
import useDebouncedCallback from '../hooks/useDebouncedCallback';

const SearchForm = ({ setSearchQuery }) => {
  const [form] = Form.useForm();
  const debouncedOnChange = useDebouncedCallback((value) => setSearchQuery(value));

  return (
    <Form
      name="searchForm"
      initialValues={{ search: '' }}
      form={form}
      onValuesChange={(changedValues) => {
        debouncedOnChange(changedValues.search);
      }}
    >
      <Form.Item
        name="search"
        style={{ marginBottom: 0, marginTop: 12 }}
      >
        <Input
          size="large"
          placeholder="Search"
          allowClear
          prefix={<SearchOutlined />}
        />
      </Form.Item>
    </Form>
  );
};

SearchForm.propTypes = {
  setSearchQuery: PropTypes.func
};

export default SearchForm;
