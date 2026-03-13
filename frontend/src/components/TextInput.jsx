import { Form, Input } from "antd";
import { Controller } from "react-hook-form";

/**
 * Reusable text input that bridges React Hook Form and Ant Design.
 * Used in both CafeFormPage and EmployeeFormPage.
 *
 * @param {string} name       - Field name matching the form schema
 * @param {string} label      - Label displayed above the input
 * @param {object} control    - React Hook Form control object
 * @param {object} rules      - React Hook Form validation rules
 * @param {string} [type]     - Input type (text, email, etc.)
 * @param {string} [placeholder]
 */
export default function TextInput({ name, label, control, rules, type = "text", placeholder }) {
  return (
    <Controller
      name={name}
      control={control}
      rules={rules}
      render={({ field, fieldState }) => (
        <Form.Item
          label={label}
          validateStatus={fieldState.error ? "error" : ""}
          help={fieldState.error?.message}
        >
          <Input {...field} type={type} placeholder={placeholder} />
        </Form.Item>
      )}
    />
  );
}
