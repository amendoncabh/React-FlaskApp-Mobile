import React, {useEffect, useState} from 'react';
import {StyleSheet, View, ScrollView} from 'react-native';
import {useNavigation} from '@react-navigation/native';

//-- components
import LocateOnMap from '../components/location/LocateOnMap';
import ProfileButton from '../components/location/PerfilButton';
import SchoolBus from '../components/location/SchoolBus';
import BusStop from '../components/location/BusStop';

export default function ParadaView() {
  const navigation = useNavigation();

  return (
    <View style={{flex: 1, height: '100%'}}>
      <LocateOnMap />
      <ProfileButton />

      <View style={styles.blocoParadas}>
        <View>
          <BusStop
            title={'Parada favorita'}
            subtitle={'Rua dos Amores, 195'}></BusStop>
        </View>

        <ScrollView>
          <SchoolBus
            title={'Bela Vista  '}
            subtitle={'Ida'}
            tempo={'5 min'}></SchoolBus>

          <SchoolBus
            title={'Várzea Fria'}
            subtitle={'Volta'}
            tempo={'10 min'}></SchoolBus>
        </ScrollView>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 50,
  },
  map: {
    flex: 1,
    height: '50%',
  },
  input: {
    width: '90%',
    height: 40,
    borderColor: '#069AC9',
    borderWidth: 1.3,
    borderRadius: 8,
    padding: 10,
    marginBottom: 10,
    alignSelf: 'center',
    flexDirection: 'row',
  },
  view: {},
  blocoParadas: {
    flex: 1,
    height: '35%',
    paddingTop: 10,
    backgroundColor: 'white',
    borderRadius: 20,
    margin: 10,
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0, // Define a largura do bloco igual à largura do contêiner pai
    justifyContent: 'center', // Centraliza verticalmente
    alignItems: 'center', // Centraliza horizontalmente
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
});
