import { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Input, Space, Popconfirm, Typography, message, Avatar } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { useCafes, useDeleteCafe } from "../hooks/useCafes";

const { Title } = Typography;

export default function CafesPage() {
  const navigate = useNavigate();
  const [location, setLocation] = useState("");
  const { data: cafes = [], isLoading } = useCafes(location || undefined);
  const deleteCafe = useDeleteCafe();

  const handleDelete = async (id) => {
    try {
      await deleteCafe.mutateAsync(id);
      message.success("Café deleted");
    } catch {
      message.error("Failed to delete café");
    }
  };

  const columnDefs = useMemo(() => [
    {
      headerName: "Logo",
      field: "logo",
      width: 80,
      cellRenderer: ({ value }) =>
        value ? (
          <Avatar src={value} shape="square" size={36} />
        ) : (
          <Avatar shape="square" size={36}>☕</Avatar>
        ),
    },
    { headerName: "Name", field: "name", flex: 1 },
    { headerName: "Description", field: "description", flex: 2 },
    {
      headerName: "Employees",
      field: "employees",
      width: 120,
      cellRenderer: ({ value, data }) => (
        <Button
          type="link"
          className="p-0"
          onClick={() => navigate(`/employees?cafe=${encodeURIComponent(data.name)}`)}
        >
          {value}
        </Button>
      ),
    },
    { headerName: "Location", field: "location", flex: 1 },
    {
      headerName: "Actions",
      width: 150,
      cellRenderer: ({ data }) => (
        <Space>
          <Button size="small" onClick={() => navigate(`/cafes/${data.id}/edit`)}>
            Edit
          </Button>
          <Popconfirm
            title="Delete this café?"
            description="This will also remove all employee assignments."
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
        <Title level={4} className="!m-0">Cafés</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => navigate("/cafes/new")}>
          Add New Café
        </Button>
      </div>

      <Input.Search
        placeholder="Filter by location"
        allowClear
        onSearch={setLocation}
        onChange={(e) => !e.target.value && setLocation("")}
        className="w-72 mb-4"
      />

      <div className="ag-theme-quartz h-[500px]">
        <AgGridReact
          rowData={cafes}
          columnDefs={columnDefs}
          loading={isLoading}
          rowHeight={52}
        />
      </div>
    </div>
  );
}
