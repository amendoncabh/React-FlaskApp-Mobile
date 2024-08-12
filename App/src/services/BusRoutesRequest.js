import Api from './Api';

export async function GetAllBusRoutes() {
  try {
    const request = await Api.get('busroutes/all');
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}

export async function GetBusRouteBy(value, route = 'id') {
  try {
    const request = await Api.get(
      !route | (route === 'id')
        ? 'busroutes/${value}'
        : 'busroutes/${route}/${value}',
    );
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}

export async function AddBusRoute(
  pName,
  pBusId,
  pDriverId,
  pSupervisorId,
  pTeamName,
  pJourneyType,
  pSchoolId,
  pEstimatedStartTime,
  pEstimatedEndTime,
) {
  try {
    data = {
      name: pName,
      bus_id: pBusId,
      bus_team: {
        name: pTeamName,
        driver_id: pDriverId,
        supervisor_id: pSupervisorId,
      },
      journey_type: pJourneyType,
      school_id: pSchoolId,
      estimated_start_time: pEstimatedStartTime,
      estimated_end_time: pEstimatedEndTime,
    };
    const request = await Api.post('busroutes/add', data);
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}
