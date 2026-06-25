// "use client";

// import React from "react";

// export default function AdminLayoutClient({
//   children,
// }: {
//   children: React.ReactNode;
// }) {
//   return (
//     <div>
//       {/* You can add sidebar/navbar later */}
//       {children}
//     </div>
//   );
// }


"use client";

import React from "react";
import AppHeader from "@/layout/AppHeader";
import AppSidebar from "@/layout/AppSidebar";
import Backdrop from "@/layout/Backdrop";

export default function AdminLayoutClient({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen">
      <AppSidebar />
      <Backdrop />

      <div className="lg:ml-[290px]">
        <AppHeader />

        <main className="p-4 md:p-6">
          {children}
        </main>
      </div>
    </div>
  );
}