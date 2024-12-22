const VITE_API_URL = import.meta.env.VITE_API_URL;
const VITE_WS_URL = import.meta.env.VITE_WS_URL;

export const API_URL = VITE_API_URL || '';
export const WS_URL = VITE_WS_URL || '';
