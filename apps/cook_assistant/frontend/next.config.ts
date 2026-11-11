import type { NextConfig } from "next";

const BACKEND_URL = (process.env.BACKEND_URL ?? "http://localhost:8000").replace(/\/$/, "");

const nextConfig: NextConfig = {
  /* config options here */
  allowedDevOrigins: ['127.0.0.1'],
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },

  experimental: {
    proxyTimeout: 120_000,
  },

  async rewrites() {
    return [
      {
        source: "/api",
        destination: `${BACKEND_URL}/api`
      },
      {
        source: "/api/:path*",
        destination: `${BACKEND_URL}/api/:path*`
      }
    ]
  }
};

export default nextConfig;
