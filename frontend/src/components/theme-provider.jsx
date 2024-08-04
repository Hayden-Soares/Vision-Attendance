import { useEffect, useState } from "react"
import { ThemeProviderContext } from "@/hooks/theme-hook"



// eslint-disable-next-line react/prop-types
export function ThemeProvider({children, defaultTheme = "system", storageKey = "vite-ui-theme", ...props}) 
{
  const [theme, setTheme] = useState( () => (localStorage.getItem(storageKey)) || defaultTheme)

  useEffect(() => 
  {
    const root = window.document.documentElement
    root.classList.remove("light", "dark")

    if (theme === "system") 
    {
      const systemTheme = window.matchMedia("(prefers-color-scheme: dark)")//** MEDIA QUERY
        .matches
        ? "dark"
        : "light"

      root.classList.add(systemTheme)
      return
    }

    root.classList.add(theme)
    
  }, [theme])

  const value = 
  {
    theme,
    setTheme: (theme) => {
      localStorage.setItem(storageKey, theme)
      setTheme(theme)
    },
  }

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  )
}
