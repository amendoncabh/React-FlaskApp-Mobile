import Api from "./Api";

export async function LoginUser(username, password) {
  try {
    const request = await Api.post('users/signin', {username, password});
    return request.data;
  } catch (error) {
    return console.log(error);
  }
}
