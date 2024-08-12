import React, {useEffect, useState} from 'react';
import {StyleSheet, View, TextInput, ScrollView} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import Icon from 'react-native-vector-icons/Ionicons';

//-- components
import LocateOnMap from './LocateOnMap';
import ProfileButton from './ProfileButton';
import BusStop from './BusStop';


export default function Map() {
  const [pesquisa, setPesquisa] = useState(null);
  const navigation = useNavigation();

  return (
    <View style={{flex: 1, height: '100%'}}>
      <LocateOnMap />
      <ProfileButton />

      <View style={styles.blocoParadas}>
        <View style={styles.input}>
          <Icon name="search" size={18} color="#888" paddingRight={10} />
          <TextInput
            onChangeText={pesquisa => setPesquisa(pesquisa)}
            keyboardType="default"
            placeholder="Procurar no mapa"
          />
        </View>

        <ScrollView>
          <BusStop
            imagem={require('../../../assets/iconCasa.png')}
            imageStyle={styles.image}
            title={'Casa'}
            subtitle={'Rua da sua Casa, 52'}></BusStop>

          <BusStop
            imagem={require('../../../assets/iconEscola.png')}
            imageStyle={styles.image}
            title={'Escola'}
            subtitle={'Rua das Escolas, 281'}></BusStop>

          <BusStop
            title={'Parada favorita'}
            subtitle={'Rua dos Amores, 195'}
            onPress={() => navigation.navigate('Parada')}></BusStop>

          <BusStop
            title={'Parada favorita'}
            subtitle={'Rua das Canções, 26'}></BusStop>
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
  buttonContainer: {
    position: 'absolute',
    top: 10,
    left: 10,
  },
  image: {
    width: 35,
    height: 35,
    marginHorizontal: 5,
  },
  blocoParadas: {
    flex: 1,
    height: '45%',
    paddingTop: 15,
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
