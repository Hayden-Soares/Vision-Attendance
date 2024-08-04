import { useContext, createContext } from 'react'

// create a context for authentication
export const AuthContext = createContext({ session: null, user: null, signOut: () => {} });

// export the useAuth hook
export const useAuth = () => {
    return useContext(AuthContext);
};