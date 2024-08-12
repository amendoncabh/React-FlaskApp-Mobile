import axios from 'axios';
import {api} from '../../app.json'

const Api = axios.create({
  baseURL: api.url_base,
});

export default Api;
