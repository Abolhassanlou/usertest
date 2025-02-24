import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const signup = (user) => axios.post(`${API_URL}/signup`, user);
export const login = (user) => axios.post(`${API_URL}/login`, user);
