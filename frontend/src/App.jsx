import { createBrowserRouter, RouterProvider, Navigate, Outlet } from "react-router-dom";
import AppLayout from "./components/AppLayout";
import CafesPage from "./pages/CafesPage";
import EmployeesPage from "./pages/EmployeesPage";
import CafeFormPage from "./pages/CafeFormPage";
import EmployeeFormPage from "./pages/EmployeeFormPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/cafes" replace /> },
      { path: "cafes", element: <CafesPage /> },
      { path: "cafes/new", element: <CafeFormPage /> },
      { path: "cafes/:id/edit", element: <CafeFormPage /> },
      { path: "employees", element: <EmployeesPage /> },
      { path: "employees/new", element: <EmployeeFormPage /> },
      { path: "employees/:id/edit", element: <EmployeeFormPage /> },
    ],
  },
]);

export default function App() {
  return <RouterProvider router={router} />;
}
