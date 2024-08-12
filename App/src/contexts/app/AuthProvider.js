import React, {createContext, useState} from 'react';

//-- services
import LoginUser from '../../services/UsersRequest';

export const AppAuthContext = createContext();

export const AuthProvider = ap => {
    async function authenticate(username, password) {
      try {
        const response = await LoginUser(username, password);
        if (response) {
          setUser(response);
          console.log(response);
        } else {
          console.log('errado');
          console.log(response);
        }
      } catch (erro) {
        console.log('errado');
      }
    }

  const [AppAuthState, setAppAuthState] = useState({
    isLoading: true,
    isLoggedIn: false,
    authToken: '',
    primaryMobile: '',
    isFirstTime: true,
    authenticate,
  });

  return (
    <AppAuthContext.Provider value={[AppAuthState, setAppAuthState]}>
      {ap.children}
    </AppAuthContext.Provider>
  );
};
