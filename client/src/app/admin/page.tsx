"use client";

import { useRouter } from "next/navigation";
import { useSession, signOut } from "next-auth/react";
import { useState } from "react";

import { EcommerceMetrics } from "@/components/ecommerce/EcommerceMetrics";
import MonthlyTarget from "@/components/ecommerce/MonthlyTarget";
import MonthlySalesChart from "@/components/ecommerce/MonthlySalesChart";
import StatisticsChart from "@/components/ecommerce/StatisticsChart";
import RecentOrders from "@/components/ecommerce/RecentOrders";
import DemographicCard from "@/components/ecommerce/DemographicCard";

export default function AdminDashboard() {
  const router = useRouter();
  const { data: session, status } = useSession();

  // Handle session states
  if (status === "loading") return <p>Loading...</p>;
  if (status === "unauthenticated") {
    router.push("/signin"); // redirect unauthenticated users
    return null;
  }

  // Book search state
  const [title, setTitle] = useState("");
  const [book, setBook] = useState<any>(null);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    setError("");
    setBook(null);
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/books/title/${encodeURIComponent(title)}`
      );
      if (!res.ok) {
        setError("Book not found");
        return;
      }
      const data = await res.json();
      setBook(data);
    } catch {
      setError("Error fetching book");
    }
  };

  return (
    <div className="grid grid-cols-12 gap-4 md:gap-6">
      {/* Logout button */}
      <div className="col-span-12 flex justify-end">
        <button
          onClick={() => signOut({ callbackUrl: "/signin" })}
          className="px-4 py-2 bg-red-600 text-white rounded"
        >
          Logout
        </button>
      </div>

      {/* Book search */}
      <div className="col-span-12 flex gap-2 items-center">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter book title"
          className="border px-3 py-2 rounded w-full"
        />
        <button
          onClick={handleSearch}
          className="px-4 py-2 bg-blue-600 text-white rounded"
        >
          Search
        </button>
      </div>

      {/* Book details */}
      {error && <p className="col-span-12 text-red-600">{error}</p>}
      {book && (
        <div className="col-span-12 border p-4 rounded bg-gray-50">
          <h2 className="text-lg font-bold">{book.title}</h2>
          <p>Author: {book.author}</p>
          <p>Published Year: {book.published_year}</p>
          <p>Status: {book.status || "N/A"}</p>
        </div>
      )}

      {/* TailAdmin dashboard components */}
      <div className="col-span-12 space-y-6 xl:col-span-7">
        <EcommerceMetrics />
        <MonthlySalesChart />
      </div>
      <div className="col-span-12 xl:col-span-5">
        <MonthlyTarget />
      </div>
      <div className="col-span-12">
        <StatisticsChart />
      </div>
      <div className="col-span-12 xl:col-span-5">
        <DemographicCard />
      </div>
      <div className="col-span-12 xl:col-span-7">
        <RecentOrders />
      </div>
    </div>
  );
}
