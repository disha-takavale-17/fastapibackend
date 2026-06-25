import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },

      async authorize(credentials) {
        const res = await fetch("http://127.0.0.1:8000/users/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams({
            username: String(credentials?.email ?? ""),
            password: String(credentials?.password ?? ""),
          }),
        });

        if (!res.ok) return null;

        const user = await res.json();

        return {
          id: user.email,
          email: user.email,
          name: user.name,
          accessToken: user.access_token,
        };
      },
    }),
  ],
 

  session: {
    strategy: "jwt",
  },

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.email = user.email;
        token.accessToken = (user as any).accessToken;
      }

      return token;
    },

    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
      }

      session.accessToken = token.accessToken as string;

      return session;
    },
  },

  secret: process.env.AUTH_SECRET,
});