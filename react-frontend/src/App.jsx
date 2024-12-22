// Core Imports
import { Provider } from 'react-redux';
import { BrowserRouter as Router } from 'react-router-dom';
import store from './store/store';

// Component Imports
import RootScreen from './screens/RootScreen';

// Misc Imports
import './styles/app.css'

function App() {
  return (
    <Provider store={store}>
      <Router>
        <RootScreen />
      </Router>
    </Provider>
  )
}

export default App
