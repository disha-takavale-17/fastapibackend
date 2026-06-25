// // import { handlers } from "@/auth" // Referring to the auth.ts we just created

// // import { handlers } from "../../../../../auth";

// // export const { GET, POST } = handlers


// // import NextAuth from "next-auth";
// // import { authOptions } from "../../../../../auth";  // make sure tsconfig.json has "@/": ["src/*"]

// // const handler = NextAuth(authOptions);

// // export { handler as GET, handler as POST };


// import { handlers } from "../../../../../auth";

// export const { GET, POST } = handlers;

// import NextAuth, { AuthOptions } from "next-auth";
// import CredentialsProvider from "next-auth/providers/credentials";

// export const authOptions: AuthOptions ={
//   providers: [
//     CredentialsProvider({
//       name: "Credentials",
//       credentials: {
//         email: { label: "Email", type: "text" },
//         password: { label: "Password", type: "password" },
//       },
//       async authorize(credentials) {
//         // Call your FastAPI backend here
//         const res = await fetch("http://localhost:8000/login", {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify(credentials),
//         });

//         if (!res.ok) return null;
//         return await res.json();
//       },
//     }),
//   ],
//   session: { strategy: "jwt" },
//   secret: process.env.NEXTAUTH_SECRET,
// };
// const handler = NextAuth(authOptions);
// export { handler as GET, handler as POST };
import NextAuth, { AuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions: AuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        try {
          const res = await fetch("http://127.0.0.1:8000/users/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
              username: credentials?.email ?? "",   // backend expects "username"
              password: credentials?.password ?? "",
            }),
          });

          if (!res.ok) return null;

          const data = await res.json();

          // Must return a user object with at least id or email
          if (data?.email) {
            return {
              id: data.email,          // use email as id if backend doesn’t return one
              email: data.email,
              name: data.name,
              accessToken: data.access_token,
            };
          }

          return null;
        } catch (err) {
          console.error("Authorize error:", err);
          return null;
        }
      },
    }),
  ],
  session: { strategy: "jwt" },
  secret: process.env.NEXTAUTH_SECRET,

  // ✅ Callbacks to persist token
  callbacks: {
    async jwt({ token, user }) {
      // When user logs in, attach accessToken
      if (user?.accessToken) {
        token.accessToken = user.accessToken;
      }
      return token;
    },
    async session({ session, token }) {
      // Expose accessToken in session
      session.accessToken = token.accessToken as string;
      return session;
    },
  },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
