/**
 * Authenticated fetch wrapper.
 *
 * Automatically attaches the JWT Bearer token from localStorage.
 * On 401, clears the token and redirects to login.
 */

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function authFetch(path, options = {}) {
  const token = localStorage.getItem("auth_token");

  const headers = {
    ...(options.headers || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Don't set Content-Type for FormData (browser sets boundary automatically)
  if (!(options.body instanceof FormData) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const url = path.startsWith("http") ? path : `${API_URL}${path}`;

  const res = await fetch(url, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    localStorage.removeItem("auth_token");
    window.location.href = "/";
    throw new Error("Session expired. Please log in again.");
  }

  return res;
}
