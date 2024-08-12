import Api from './Api';

export async function GetAllRouteHistories() {
  try {
    const request = await Api.get('routehistories/all');
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}

export async function GetRouteHistoryBy(value, route='id') {
  try {
    const request = await Api.get(
      !route | (route === 'id')
        ? 'routehistories/${value}'
        : 'routehistories/${route}/${value}',
    );
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}

export async function AddRouteHistory(
  pRouteLocationId,
  pLocationStudentId,
  pRouteStatus,
  pLocationStatus,
  pStudentStatus,
) {
  try {
    data = {
      routelocation_id: pRouteLocationId,
      locationstudent_id: pLocationStudentId,
      route_status: pRouteStatus,
      location_status: pLocationStatus,
      student_status: pStudentStatus,
    };
    const request = await Api.post('routehistories/add', data);
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}
