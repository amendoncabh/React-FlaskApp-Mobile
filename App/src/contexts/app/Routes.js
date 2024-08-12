import React from 'react';
import {createStackNavigator} from '@react-navigation/stack';

import Map from '../../screens/Map';
import BusStop from '../screens/BusStop';
// import Favoritos from '../screens/Favoritos/index';
// import Feedback from '../screens/Feedback/Feedback';
// import ProfileScreen from '../screens/Perfil/Perfil';

export function StackRoutes() {
  const AppStack = createStackNavigator();
  return (
    <AppStack.Navigator initialRouteName="Mapa">
      <AppStack.Screen name="Mapa" component={Map} />
      <AppStack.Screen name="Paradas" component={BusStop} />
      {/* <AppStack.Screen name="Perfil" component={ProfileScreen} />
      <AppStack.Screen name="Favoritos" component={Favoritos} />
      <AppStack.Screen name="Feedback" component={Feedback} /> */}
    </AppStack.Navigator>
  );
}
