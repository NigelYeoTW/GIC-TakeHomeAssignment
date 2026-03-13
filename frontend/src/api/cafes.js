import client from "./client";

export const fetchCafes = async (location) => {
  const params = location ? { location } : {};
  const { data } = await client.get("/cafes", { params });
  return data;
};

export const fetchCafeById = async (id) => {
  const { data } = await client.get(`/cafes/${id}`);
  return data;
};

export const createCafe = async (formData) => {
  const { data } = await client.post("/cafes", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

export const updateCafe = async ({ id, formData }) => {
  const { data } = await client.put(`/cafes/${id}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

export const deleteCafe = async (id) => {
  await client.delete(`/cafes/${id}`);
};
