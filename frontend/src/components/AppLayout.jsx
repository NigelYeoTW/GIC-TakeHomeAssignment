import { Outlet, useNavigate, useLocation } from "react-router-dom";
import { Layout, Menu } from "antd";
import { CoffeeOutlined, TeamOutlined } from "@ant-design/icons";

const { Sider, Content } = Layout;

const NAV_ITEMS = [
  { key: "/cafes", icon: <CoffeeOutlined />, label: "Cafés" },
  { key: "/employees", icon: <TeamOutlined />, label: "Employees" },
];

export default function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  const selectedKey = NAV_ITEMS.find((item) =>
    location.pathname.startsWith(item.key)
  )?.key;

  return (
    <Layout className="min-h-screen">
      <Sider theme="light" className="border-r border-gray-100">
        <div className="px-4 py-4 font-bold text-base">
          ☕ Café Manager
        </div>
        <Menu
          mode="inline"
          selectedKeys={[selectedKey]}
          items={NAV_ITEMS}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <Layout>
        <Content className="p-6 bg-white">
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
