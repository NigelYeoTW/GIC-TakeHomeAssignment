import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchCafes, fetchCafeById, createCafe, updateCafe, deleteCafe } from "../api/cafes";
import { EMPLOYEES_KEY } from "./useEmployees";

export const CAFES_KEY = "cafes";

export const useCafes = (location) =>
  useQuery({
    queryKey: [CAFES_KEY, location],
    queryFn: () => fetchCafes(location),
  });

export const useCafeById = (id) =>
  useQuery({
    queryKey: [CAFES_KEY, "detail", id],
    queryFn: () => fetchCafeById(id),
    enabled: Boolean(id),
  });

export const useCreateCafe = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createCafe,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: [CAFES_KEY] }),
  });
};

export const useUpdateCafe = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateCafe,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: [CAFES_KEY] }),
  });
};

export const useDeleteCafe = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteCafe,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [CAFES_KEY] });
      queryClient.invalidateQueries({ queryKey: [EMPLOYEES_KEY] });
    },
  });
};
