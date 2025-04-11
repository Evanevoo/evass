import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const auth = {
  login: (email: string, password: string) =>
    api.post('/token', { email, password }),
  register: (userData: any) => api.post('/register', userData),
  getUser: () => api.get('/users/me'),
};

export const cylinders = {
  getAll: () => api.get('/cylinders'),
  getById: (id: string) => api.get(`/cylinders/${id}`),
  create: (cylinderData: any) => api.post('/cylinders', cylinderData),
  update: (id: string, cylinderData: any) =>
    api.put(`/cylinders/${id}`, cylinderData),
  delete: (id: string) => api.delete(`/cylinders/${id}`),
  search: (identifier: string) => api.get(`/cylinders/search/${identifier}`),
  getQRCode: (id: string) => api.get(`/cylinders/${id}/qr-code`),
};

export const customers = {
  getAll: () => api.get('/customers'),
  getById: (id: string) => api.get(`/customers/${id}`),
  create: (customerData: any) => api.post('/customers', customerData),
  update: (id: string, customerData: any) =>
    api.put(`/customers/${id}`, customerData),
  delete: (id: string) => api.delete(`/customers/${id}`),
  getLocations: (customerId: string) =>
    api.get(`/customers/${customerId}/locations`),
  createLocation: (customerId: string, locationData: any) =>
    api.post(`/customers/${customerId}/locations`, locationData),
  deleteLocation: (customerId: string, locationId: string) =>
    api.delete(`/customers/${customerId}/locations/${locationId}`),
};

export const movements = {
  getAll: () => api.get('/movements/cylinder'),
  getById: (id: string) => api.get(`/movements/cylinder/${id}`),
  create: (movementData: any) => api.post('/movements/cylinder', movementData),
  getTransactions: () => api.get('/movements/transaction'),
  getTransactionById: (id: string) => api.get(`/movements/transaction/${id}`),
  createTransaction: (transactionData: any) =>
    api.post('/movements/transaction', transactionData),
  completeTransaction: (id: string) =>
    api.put(`/movements/transaction/${id}/complete`),
};

export const maintenance = {
  getAll: () => api.get('/maintenance'),
  getById: (id: string) => api.get(`/maintenance/${id}`),
  create: (maintenanceData: any) => api.post('/maintenance', maintenanceData),
  update: (id: string, maintenanceData: any) =>
    api.put(`/maintenance/${id}`, maintenanceData),
  getByCylinder: (cylinderId: string) =>
    api.get(`/maintenance/cylinder/${cylinderId}`),
  getUpcoming: (days: number) => api.get(`/maintenance/upcoming?days=${days}`),
  getOverdue: () => api.get('/maintenance/overdue'),
  createSchedule: (cylinderId: string, scheduleData: any) =>
    api.post(`/maintenance/schedule/${cylinderId}`, scheduleData),
};

export const analytics = {
  getMetrics: () => api.get('/analytics/metrics'),
  getUsageTrends: (timeRange: string) =>
    api.get(`/analytics/usage-trends?range=${timeRange}`),
  getCustomerDistribution: () => api.get('/analytics/customer-distribution'),
  getMaintenanceTrends: (timeRange: string) =>
    api.get(`/analytics/maintenance-trends?range=${timeRange}`),
};

export const bulkUploadCustomers = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/api/v1/bulk/customers', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const bulkUploadCylinders = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/api/v1/bulk/cylinders', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export default api; 