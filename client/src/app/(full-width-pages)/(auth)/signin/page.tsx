// import SignInForm from "@/components/auth/SignInForm";
// import { Metadata } from "next";

// export const metadata: Metadata = {
//   title: "Next.js SignIn Page | TailAdmin - Next.js Dashboard Template",
//   description: "This is Next.js Signin Page TailAdmin Dashboard Template",
// };

// export default function SignIn() {
//   return <SignInForm />;
// }
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import SignInForm from "@/components/auth/SignInForm";
import { Metadata } from "next";
import { getServerSession } from "next-auth";
import { redirect } from "next/navigation";
// import { getServerSession } from "next-auth";
// import { authOptions } from "@/app/api/auth/[...nextauth]/route";
 
export const metadata: Metadata = {
  title: "Sign In | Living Things",
  description: "Sign in to Living Things - Intelligent Document Processing Platform",
};
 
export default async function SignIn() {
  const session = await getServerSession(authOptions);
 
  if (session) {
    redirect("/"); // already signed in
  }
 
  return <SignInForm />;
}