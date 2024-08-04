import { createContext, useContext } from 'react'

const initialState = 
{
  theme: "system",
  setTheme: () => null,
}
export const ThemeProviderContext = createContext(initialState)//Use React context


// eslint-disable-next-line react-refresh/only-export-components
export default function useTheme() 
{
  const context = useContext(ThemeProviderContext)

  if (context === undefined)
    throw new Error("useTheme must be used within a ThemeProvider")

  return context
}