import Api from './Api';

export async function GetAllRouteLocations() {
  try {
    const request = await Api.get('routelocations/all');
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}

export async function GetRouteLocationBy(value, route = 'id') {
  try {
    const request = await Api.get(
      !route | (route === 'id')
        ? 'routelocations/${value}'
        : 'routelocations/${route}/${value}',
    );
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}

export async function AddRouteLocation(
  pBusRouteId,
  pBusStopId,
  pEstimatedTravelTime,
  pDelayTravelTime,
) {
  try {
    data = {
      busroute_id: pBusRouteId,
      busstop_id: pBusStopId,
      estimated_travel_time: pEstimatedTravelTime,
      delay_travel_time: pDelayTravelTime,
    };
    const request = await Api.post('routelocations/add', data);
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}
