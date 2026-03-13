import axios from "axios";

const baseURL = "/api/v1";

const client = axios.create({ baseURL });

export default client;
