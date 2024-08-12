import Api from './Api';

export async function GetAllLocationStudents() {
  try {
    const request = await Api.get('locationstudents/all');
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}

export async function GetLocationStudentBy(value, route = 'id') {
  try {
    const request = await Api.get(
      !route | (route === 'id')
        ? 'locationstudents/${value}'
        : 'locationstudents/${route}/${value}',
    );
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}

export async function AddLocationStudent(pStudentId, pBusStopLocationId) {
  try {
    data = {
      student_id: pStudentId,
      busstop_location_id: pBusStopLocationId,
    };
    const request = await Api.post('locationstudents/add', data);
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}
