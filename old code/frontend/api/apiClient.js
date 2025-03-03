// Simple example using fetch. For production, you may want axios and better error handling.

const apiClient = {
    get: async (url) => {
      const res = await fetch(url, { credentials: 'include' });
      if (!res.ok) throw new Error(`GET ${url} failed`);
      return res.json();
    },
    post: async (url, data) => {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(`POST ${url} failed`);
      return res.json();
    },
    put: async (url, data) => {
      const res = await fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(`PUT ${url} failed`);
      return res.json();
    },
    delete: async (url) => {
      const res = await fetch(url, {
        method: 'DELETE',
        credentials: 'include',
      });
      if (!res.ok) throw new Error(`DELETE ${url} failed`);
      return res.json();
    },
  };
  
  export default apiClient;
  