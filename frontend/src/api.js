export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Get or create user ID
const getUserId = () => {
    let userId = localStorage.getItem('vois_user_id');
    if (!userId) {
        userId = 'user_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('vois_user_id', userId);
    }
    return userId;
};

export const ingestAsset = async (assetId) => {
    const response = await fetch(`${API_BASE_URL}/ingest/${assetId}`, {
        method: "POST",
    });
    if (!response.ok) throw new Error("Ingestion failed");
    return response.json();
};

export const retrieveContext = async (assetId, query) => {
    const params = new URLSearchParams({
        query: query || "investment analysis",
        asset_id: assetId,
        user_id: getUserId(),
    });
    const response = await fetch(`${API_BASE_URL}/retrieve?${params.toString()}`);
    if (!response.ok) throw new Error("Retrieval failed");
    return response.json();
};

// One-shot analyze endpoint
export const analyzeAsset = async (assetId) => {
    const params = new URLSearchParams({
        user_id: getUserId(),
    });
    const response = await fetch(`${API_BASE_URL}/analyze/${assetId}?${params.toString()}`);
    if (!response.ok) throw new Error("Analysis failed");
    return response.json();
};

// Profile management
export const getProfile = async () => {
    const response = await fetch(`${API_BASE_URL}/api/v1/profile/${getUserId()}`);
    if (!response.ok) throw new Error("Failed to fetch profile");
    return response.json();
};

export const updateProfile = async (profile) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/profile`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...profile, user_id: getUserId() }),
    });
    if (!response.ok) throw new Error("Failed to update profile");
    return response.json();
};

export { getUserId };
