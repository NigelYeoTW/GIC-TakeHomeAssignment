import axios from "axios";

const baseURL = import.meta.env.API_URL
  ? `${import.meta.env.API_URL}/api/v1`
  : "/api/v1";

const client = axios.create({ baseURL });

export default client;
