// Core Imports
import { useRoutes } from 'react-router-dom';

// Component Imports
import MessagesScreen from './MessagesScreen';
import MessagesLayout from '../layouts/MessagesLayout';

const RootScreen = () => {
  let routes = useRoutes([
    { path: '*', element: <MessagesLayout><MessagesScreen /></MessagesLayout> }
  ]);
  return routes;
}

export default RootScreen;
