import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useForm, Controller } from "react-hook-form";
import { Form, Button, Radio, Select, Space, Typography, message, Spin } from "antd";
import { useEmployees, useCreateEmployee, useUpdateEmployee } from "../hooks/useEmployees";
import { useCafes } from "../hooks/useCafes";
import TextInput from "../components/TextInput";
import UnsavedChangesGuard from "../components/UnsavedChangesGuard";

const { Title } = Typography;

const SG_PHONE_REGEX = /^[89]\d{7}$/;
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function EmployeeFormPage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = Boolean(id);

  const { data: employees = [], isLoading: isFetchingEmployees } = useEmployees();
  const { data: cafes = [] } = useCafes();
  const createEmployee = useCreateEmployee();
  const updateEmployee = useUpdateEmployee();

  const {
    control,
    handleSubmit,
    reset,
    formState: { isDirty, isSubmitting },
  } = useForm({
    defaultValues: {
      name: "",
      email_address: "",
      phone_number: "",
      gender: "Male",
      cafe_id: null,
    },
  });

  useEffect(() => {
    if (isEditMode && employees.length > 0) {
      const employee = employees.find((e) => e.id === id);
      if (employee) {
        const matchedCafe = cafes.find((c) => c.name === employee.cafe);
        reset({
          name: employee.name,
          email_address: employee.email_address,
          phone_number: employee.phone_number,
          gender: employee.gender,
          cafe_id: matchedCafe?.id ?? null,
        });
      }
    }
  }, [isEditMode, employees, cafes, id, reset]);

  const onSubmit = async (values) => {
    const payload = {
      name: values.name,
      email_address: values.email_address,
      phone_number: values.phone_number,
      gender: values.gender,
      cafe_id: values.cafe_id || null,
    };

    try {
      if (isEditMode) {
        await updateEmployee.mutateAsync({ id, payload });
        message.success("Employee updated");
      } else {
        await createEmployee.mutateAsync(payload);
        message.success("Employee created");
      }
      navigate("/employees");
    } catch (err) {
      message.error(err?.response?.data?.detail ?? "Something went wrong");
    }
  };

  if (isEditMode && isFetchingEmployees) return <Spin />;

  return (
    <div className="max-w-lg">
      <UnsavedChangesGuard isDirty={isDirty} isSubmitting={isSubmitting}/>

      <Title level={4}>{isEditMode ? "Edit Employee" : "Add New Employee"}</Title>

      <Form layout="vertical" onFinish={handleSubmit(onSubmit)}>
        <TextInput
          name="name"
          label="Name"
          control={control}
          placeholder="6–10 characters"
          rules={{
            required: "Name is required",
            minLength: { value: 6, message: "Minimum 6 characters" },
            maxLength: { value: 10, message: "Maximum 10 characters" },
          }}
        />

        <TextInput
          name="email_address"
          label="Email Address"
          control={control}
          type="email"
          placeholder="e.g. alice@example.com"
          rules={{
            required: "Email is required",
            pattern: { value: EMAIL_REGEX, message: "Enter a valid email address" },
          }}
        />

        <TextInput
          name="phone_number"
          label="Phone Number"
          control={control}
          placeholder="8 or 9 followed by 7 digits"
          rules={{
            required: "Phone number is required",
            pattern: { value: SG_PHONE_REGEX, message: "Must start with 8 or 9 and be 8 digits" },
          }}
        />

        <Controller
          name="gender"
          control={control}
          render={({ field }) => (
            <Form.Item label="Gender">
              <Radio.Group {...field}>
                <Radio value="Male">Male</Radio>
                <Radio value="Female">Female</Radio>
              </Radio.Group>
            </Form.Item>
          )}
        />

        <Controller
          name="cafe_id"
          control={control}
          render={({ field }) => (
            <Form.Item label="Assigned Café (optional)">
              <Select
                {...field}
                allowClear
                placeholder="Select a café"
                options={cafes.map((c) => ({ value: c.id, label: c.name }))}
              />
            </Form.Item>
          )}
        />

        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit" loading={isSubmitting}>
              {isEditMode ? "Save Changes" : "Create Employee"}
            </Button>
            <Button onClick={() => navigate("/employees")}>Cancel</Button>
          </Space>
        </Form.Item>
      </Form>
    </div>
  );
}
