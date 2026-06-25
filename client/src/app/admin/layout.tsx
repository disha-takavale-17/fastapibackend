import AdminLayoutClient from "../../components/auth/AdminLayoutClient";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AdminLayoutClient>{children}</AdminLayoutClient>;
}
// export default function AdminLayout({ children }) {
//   return (
//     <div>
//       <Sidebar />
//       <main>{children}</main>
//     </div>
//   );
// }