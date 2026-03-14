import { useMemo } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Button, Space, Popconfirm, Typography, message } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { useEmployees, useDeleteEmployee } from "../hooks/useEmployees";

const { Title } = Typography;

export default function EmployeesPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const cafeFilter = searchParams.get("cafe") || undefined;

  const { data: employees, isLoading } = useEmployees(cafeFilter);
  const deleteEmployee = useDeleteEmployee();

  const handleDelete = async (id) => {
    try {
      await deleteEmployee.mutateAsync(id);
      message.success("Employee deleted");
    } catch {
      message.error("Failed to delete employee");
    }
  };

  const columnDefs = useMemo(() => [
    { headerName: "ID", field: "id", width: 130 },
    { headerName: "Name", field: "name", flex: 1 },
    { headerName: "Email", field: "email_address", flex: 1 },
    { headerName: "Phone", field: "phone_number", width: 130 },
    { headerName: "Days Worked", field: "days_worked", width: 130 },
    { headerName: "Café", field: "cafe", flex: 1 },
    {
      headerName: "Actions",
      width: 150,
      cellRenderer: ({ data }) => (
        <Space>
          <Button size="small" onClick={() => navigate(`/employees/${data.id}/edit`)}>
            Edit
          </Button>
          <Popconfirm
            title="Delete this employee?"
            onConfirm={() => handleDelete(data.id)}
            okText="Delete"
            cancelText="Cancel"
            okButtonProps={{ danger: true }}
          >
            <Button size="small" danger>Delete</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ], [navigate]);

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <Title level={4} className="!m-0">
          {cafeFilter ? `Employees — ${cafeFilter}` : "Employees"}
        </Title>
        <Space>
          {cafeFilter && (
            <Button onClick={() => navigate("/employees")}>Show All</Button>
          )}
          <Button type="primary" icon={<PlusOutlined />} onClick={() => navigate("/employees/new")}>
            Add New Employee
          </Button>
        </Space>
      </div>

      <div className="ag-theme-quartz h-[500px]">
        <AgGridReact
          rowData={employees}
          columnDefs={columnDefs}
          loading={isLoading}
          rowHeight={48}
        />
      </div>
    </div>
  );
}
