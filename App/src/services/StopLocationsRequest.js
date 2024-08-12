import Api from './Api';

export async function GetAllStopLocations() {
  try {
    const request = await Api.get('stoplocations/all');
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}

export async function GetStopLocationBy(value, route = 'id') {
  try {
    const request = await Api.get(
      !route | (route === 'id')
        ? 'stoplocations/${value}'
        : 'stoplocations/${route}/${value}',
    );
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}

export async function AddStopLocation(
  pName,
  pStreet,
  pNumber,
  pDistrict,
  pProvince,
  pState,
  pLocation,
  pNextLocation,
) {
  try {
    data = {
      name: pName,
      address: {
        street: pStreet,
        number: pNumber,
        district: pDistrict,
        province: pProvince,
        state: pState,
        location: pLocation,
      },
      next_location: pNextLocation,
    };
    const request = await Api.post('stoplocations/add', data);
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}
