import { configureStore } from '@reduxjs/toolkit';
import { ChatsSlice } from './slice/chatsSlice';
import { chatApi } from './apiSlice/chatApi';

const store = configureStore({
  reducer: {
    chats: ChatsSlice.reducer,
    [chatApi.reducerPath]: chatApi.reducer
  },

  middleware: (getDefaultMiddleware) => getDefaultMiddleware({}).concat([chatApi.middleware])
});

export default store;
