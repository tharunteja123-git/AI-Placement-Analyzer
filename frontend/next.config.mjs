/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    const backendUrl = (process.env.BACKEND_API_URL || "http://127.0.0.1:8000").replace(/\/+$/, "");
    return [
      { source: "/api/health", destination: `${backendUrl}/health` },
      { source: "/api/:path*", destination: `${backendUrl}/api/:path*` },
    ];
  },
  experimental: {
    agentFeedback: true,
  },
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
