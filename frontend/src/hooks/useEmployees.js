import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchEmployees, createEmployee, updateEmployee, deleteEmployee } from "../api/employees";
import { CAFES_KEY } from "./useCafes";

export const EMPLOYEES_KEY = "employees";

const patchCafeCounts = (queryClient, affectedCafes) => {
  if (!affectedCafes?.length) return;
  queryClient.setQueriesData({ queryKey: [CAFES_KEY] }, (oldCafes) => {
    if (!oldCafes) return oldCafes;
    return oldCafes.map((cafe) => {
      const updated = affectedCafes.find((a) => a.id === cafe.id);
      return updated ? { ...cafe, employees: updated.employees } : cafe;
    });
  });
};

export const useEmployees = (cafe) =>
  useQuery({
    queryKey: [EMPLOYEES_KEY, cafe],
    queryFn: () => fetchEmployees(cafe),
  });

export const useCreateEmployee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createEmployee,
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: [EMPLOYEES_KEY] });
      patchCafeCounts(queryClient, response.affected_cafes);
    },
  });
};

export const useUpdateEmployee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateEmployee,
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: [EMPLOYEES_KEY] });
      patchCafeCounts(queryClient, response.affected_cafes);
    },
  });
};

export const useDeleteEmployee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteEmployee,
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: [EMPLOYEES_KEY] });
      patchCafeCounts(queryClient, response.affected_cafes);
    },
  });
};
