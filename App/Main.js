import {NavigationContainer} from '@react-navigation/native';
import App from './App';

//-- contexts
import {AuthProvider} from './src/contexts/app/AuthProvider';

const Main = () => {
  return (
    <NavigationContainer>
      <AuthProvider>
        <App />
      </AuthProvider>
    </NavigationContainer>
  );
};

export default Main;
