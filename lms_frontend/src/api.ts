import axios from "axios";

export const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" }
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem("token");
      if (window.location.pathname !== "/auth") window.location.href = "/auth";
    }
    return Promise.reject(err);
  }
);

export const login = async (email: string, password: string) => {
  const res = await api.post("/auth/login", { email, password });
  if (res.data.access_token) localStorage.setItem("token", res.data.access_token);
  return res.data;
};

export const register = async (email: string, password: string) => {
  return (await api.post("/auth/register", { email, password, role: "STUDENT" })).data;
};

export const logout = () => {
  localStorage.removeItem("token");
  window.location.href = "/";
};

export const getCourses = () => api.get("/courses");
export const getCourse = (id: string) => api.get(`/courses/${id}`);
export const createCourse = (data: any) => api.post("/courses", data);
export const updateCourse = (id: string, data: any) => api.put(`/courses/${id}`, data);
export const deleteCourse = (id: string) => api.delete(`/courses/${id}`);

export const getQuiz = (id: string) => api.get(`/quizzes/${id}`);
export const startQuiz = (id: string) => api.post(`/quizzes/${id}/start`);
export const updateQuiz = (id: string, data: any) => api.put(`/quizzes/${id}`, data);
export const deleteQuiz = (id: string) => api.delete(`/quizzes/${id}`);

export const submitAttempt = (id: string, answers: any[]) => 
  api.post(`/attempts/${id}/submit`, { answers });
export const getMyAttempts = () => api.get("/attempts/my");
export const retryQuiz = (quizId: string) => api.post(`/attempts/quiz/${quizId}/retry`);

export const getMyCourses = () => api.get("/users/me/courses");