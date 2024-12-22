import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  chats: [],
  loading: false,
  error: null
};

export const ChatsSlice = createSlice({
  name: 'chat_slice',
  initialState,
  reducers: { }
});

export default ChatsSlice.reducer;
