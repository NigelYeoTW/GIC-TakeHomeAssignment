import client from "./client";

export const fetchEmployees = async (cafe) => {
  const params = cafe ? { cafe } : {};
  const { data } = await client.get("/employees", { params });
  return data;
};

export const createEmployee = async (payload) => {
  const { data } = await client.post("/employees", payload);
  return data;
};

export const updateEmployee = async ({ id, payload }) => {
  const { data } = await client.put(`/employees/${id}`, payload);
  return data;
};

export const deleteEmployee = async (id) => {
  const { data } = await client.delete(`/employees/${id}`);
  return data;
};
