import React, {useEffect, useState, useContext} from 'react';

//-- contexts
import StackRoutes from './src/contexts/app/Routes'
import {AppAuthContext} from './src/contexts/app/AuthProvider';

//-- screens
import Login from './src/screens/Login'

const App = () => {
  const [splashLoading, setSplashLoading] = useState(true);
  useEffect(() => {
    setTimeout(() => {
      setSplashLoading(false);
    }, 2000);
  }, []);

  const [AppAuthState, setAppAuthState] = useContext(AppAuthContext);
  return (
    AppAuthState.isLoggedIn ? <StackRoutes/> : <Login/>
  );
};

export default App;
