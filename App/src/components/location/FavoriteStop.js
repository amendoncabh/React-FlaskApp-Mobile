import React, {useState} from 'react';
import {View, TouchableOpacity} from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';

const FavoriteStop = ({favorite, onPress}) => {
  const [isFavorite, setFavoriteState] = useState(favorite);

  const toggleFavorito = () => {
    setFavoriteState(!isFavorite);
    onPress(!isFavorite); // Passa o novo estado como argumento para a função onPress
  };

  return (
    <TouchableOpacity onPress={toggleFavorito}>
      <View style={{padding: 10}}>
        <Icon
          name={isFavorite ? 'star' : 'star-o'}
          size={34}
          color={isFavorite ? 'gold' : 'gray'}
        />
      </View>
    </TouchableOpacity>
  );
};

export default FavoriteStop;
