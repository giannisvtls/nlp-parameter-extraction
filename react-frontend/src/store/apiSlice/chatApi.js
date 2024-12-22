// src/features/chat/chatApi.js
import { createApi } from '@reduxjs/toolkit/query/react';
import { createEntityAdapter } from '@reduxjs/toolkit';
import { WS_URL } from '../../constants/env';

const messagesAdapter = createEntityAdapter({
  selectId: (message) => message.id || `${message.username}-${Date.now()}`,
  sortComparer: (a, b) => (a.timestamp || '').localeCompare(b.timestamp || '')
});

const initialState = messagesAdapter.getInitialState({
  connected: false,
  activeRoom: null
});

let activeSocket = null;

export const chatApi = createApi({
  reducerPath: 'chatApi',
  baseQuery: () => ({ data: null }),
  endpoints: (builder) => ({
    connectToRoom: builder.mutation({
      queryFn: ({ roomName }) => ({ data: { roomName } }),
      async onCacheEntryAdded(
        { roomName },
        { cacheDataLoaded, cacheEntryRemoved, dispatch }
      ) {
        try {
          await cacheDataLoaded;

          // Close existing socket if any
          if (activeSocket) {
            activeSocket.close();
          }

          const wsUrl = `${WS_URL}/chat/${roomName}/`;
          activeSocket = new WebSocket(wsUrl);

          activeSocket.onopen = () => {
            dispatch(
              chatApi.util.updateQueryData('getMessages', roomName, (draft) => {
                draft.connected = true;
                draft.activeRoom = roomName;
              })
            );
            console.log('Connected to room:', roomName);
          };

          activeSocket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            dispatch(
              chatApi.util.updateQueryData('getMessages', roomName, (draft) => {
                messagesAdapter.addOne(draft, {
                  ...message,
                  id: `${message.username}-${Date.now()}`,
                  timestamp: new Date().toISOString(),
                  room: roomName
                });
              })
            );
          };

          activeSocket.onclose = () => {
            dispatch(
              chatApi.util.updateQueryData('getMessages', roomName, (draft) => {
                draft.connected = false;
              })
            );
            console.log('Disconnected from room:', roomName);
          };

          activeSocket.onerror = (error) => {
            console.error('WebSocket error:', error);
          };

          // Cleanup on unmount
          await cacheEntryRemoved;
          if (activeSocket) {
            activeSocket.close();
            activeSocket = null;
          }
        } catch (error) {
          console.error('WebSocket connection error:', error);
        }
      }
    }),

    getMessages: builder.query({
      query: (roomName) => ({ roomName }),
      transformResponse: () => messagesAdapter.getInitialState({
        connected: false,
        activeRoom: null
      })
    }),

    sendMessage: builder.mutation({
      queryFn: ({ message, username, roomName }) => {
        if (!activeSocket || activeSocket.readyState !== WebSocket.OPEN) {
          throw new Error('WebSocket is not connected');
        }

        activeSocket.send(JSON.stringify({ message, username }));
        return { data: null };
      }
    })
  })
});

// Selectors
export const selectMessages = (state) => {
  const messages = Object.values(state.chatApi.queries?.getMessages?.data?.entities || {});
  return messages.sort((a, b) => (a.timestamp || '').localeCompare(b.timestamp || ''));
};

export const selectIsConnected = (state) =>
  state.chatApi.queries?.getMessages?.data?.connected || false;

export const {
  useConnectToRoomMutation,
  useGetMessagesQuery,
  useSendMessageMutation
} = chatApi;
