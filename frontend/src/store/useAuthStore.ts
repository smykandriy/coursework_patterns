import { create } from "zustand";

interface AuthState {
  token: string | null;
  setToken: (token: string) => void;
  logout: () => void;
}

const useAuthStore = create<AuthState>(set => ({
  token: null,
  setToken: token => set({ token }),
  logout: () => set({ token: null })
}));

export default useAuthStore;
