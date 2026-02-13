import axios from 'axios';

export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Create axios instance with auth interceptor
const api = axios.create({
    baseURL: API_BASE_URL
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Helper to get user ID from stored token
export const getUserId = () => {
    const token = localStorage.getItem('token');
    if (!token) return 'default';

    try {
        // Decode JWT payload (base64)
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.sub || 'default';
    } catch (e) {
        return 'default';
    }
};

// Asset operations
export const ingestAsset = async (assetId) => {
    const response = await api.post(`/ingest/${assetId}`);
    return response.data;
};

export const retrieveContext = async (assetId, query) => {
    const params = new URLSearchParams({
        query: query || "investment analysis",
        asset_id: assetId
    });
    const response = await api.get(`/retrieve?${params.toString()}`);
    return response.data;
};

// One-shot analyze endpoint
export const analyzeAsset = async (assetId) => {
    const response = await api.get(`/analyze/${assetId}`);
    return response.data;
};

// History management
export const getHistory = async (limit = 20) => {
    const response = await api.get(`/api/v1/history?limit=${limit}`);
    return response.data;
};

// Profile management
export const getProfile = async () => {
    const response = await api.get(`/api/v1/profile/me`);
    return response.data;
};

export const updateProfile = async (profile) => {
    const response = await api.post(`/api/v1/profile`, profile);
    return response.data;
};

// Chat
export const sendChat = async (query) => {
    const response = await api.post(`/chat/general`, { query });
    return response.data;
};

// Market data
export const getMarketData = async (ticker) => {
    const response = await api.get(`/market-data/${ticker}`);
    return response.data;
};
