import {api} from  '../../app.json'
export const baseUrl = `\${api.protocol}://\${api.host}${api.port ? `:\${api.port}` : ''}/\${api.urlBase}`;

