import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useForm } from "react-hook-form";
import { Form, Button, Upload, Space, Typography, message, Spin } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import { useCafeById, useCreateCafe, useUpdateCafe } from "../hooks/useCafes";
import TextInput from "../components/TextInput";
import UnsavedChangesGuard from "../components/UnsavedChangesGuard";

const { Title } = Typography;
const MAX_LOGO_SIZE_BYTES = 2 * 1024 * 1024;

export default function CafeFormPage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = Boolean(id);

  const { data: cafe, isLoading: isFetchingCafe } = useCafeById(id);
  const createCafe = useCreateCafe();
  const updateCafe = useUpdateCafe();

  const {
    control,
    handleSubmit,
    reset,
    setValue,
    watch,
    formState: { isDirty, isSubmitting },
  } = useForm({
    defaultValues: { name: "", description: "", location: "", logo: null },
  });

  useEffect(() => {
    if (cafe) {
      reset({
        name: cafe.name,
        description: cafe.description,
        location: cafe.location,
        logo: null,
      });
    }
  }, [cafe, reset]);

  const logoFile = watch("logo");

  const onSubmit = async (values) => {
    const formData = new FormData();
    formData.append("name", values.name);
    formData.append("description", values.description);
    formData.append("location", values.location);
    if (values.logo) {
      formData.append("logo", values.logo);
    }

    try {
      if (isEditMode) {
        await updateCafe.mutateAsync({ id, formData });
        message.success("Café updated");
      } else {
        await createCafe.mutateAsync(formData);
        message.success("Café created");
      }
      navigate("/cafes");
    } catch (err) {
      message.error(err?.response?.data?.detail ?? "Something went wrong");
    }
  };

  if (isEditMode && isFetchingCafe) return <Spin />;

  return (
    <div className="max-w-lg">
      <UnsavedChangesGuard isDirty={isDirty} isSubmitting={isSubmitting} />

      <Title level={4}>{isEditMode ? "Edit Café" : "Add New Café"}</Title>

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
          name="description"
          label="Description"
          control={control}
          placeholder="Max 256 characters"
          rules={{
            required: "Description is required",
            maxLength: { value: 256, message: "Maximum 256 characters" },
          }}
        />

        <TextInput
          name="location"
          label="Location"
          control={control}
          placeholder="e.g. Orchard"
          rules={{ required: "Location is required", maxLength: { value: 255, message: "Maximum 255 characters" } }}
        />

        <Form.Item label="Logo (optional, max 2MB)">
          <Upload
            beforeUpload={(file) => {
              if (file.size > MAX_LOGO_SIZE_BYTES) {
                message.error("Logo must be smaller than 2MB");
                return Upload.LIST_IGNORE;
              }
              setValue("logo", file, { shouldDirty: true });
              return false;
            }}
            onRemove={() => setValue("logo", null, { shouldDirty: true })}
            maxCount={1}
            accept="image/*"
            fileList={logoFile ? [{ uid: "-1", name: logoFile.name, status: "done" }] : []}
          >
            <Button icon={<UploadOutlined />}>Select Logo</Button>
          </Upload>
        </Form.Item>

        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit" loading={isSubmitting}>
              {isEditMode ? "Save Changes" : "Create Café"}
            </Button>
            <Button onClick={() => navigate("/cafes")}>Cancel</Button>
          </Space>
        </Form.Item>
      </Form>
    </div>
  );
}
