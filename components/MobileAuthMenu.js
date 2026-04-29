import React from 'react'
import { useAuth } from '../context/AuthContext'

const MobileAuthMenu = () => {
  const { isAuthenticated, displayName, signOut, loading } = useAuth()

  const handleSignOut = async () => {
    try {
      await signOut()
      // UI will update automatically through AuthContext
    } catch (error) {
      console.error('Sign out error:', error)
    }
  }

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-10 bg-surface-container/50 rounded-2xl"></div>
      </div>
    )
  }

  if (isAuthenticated) {
    return (
      <>
        {/* Welcome message */}
        <div className="px-4 py-3 border-b border-white/10">
          <p className="text-primary text-sm font-medium">Welcome, {displayName}</p>
          <p className="text-secondary/60 text-xs">Signed in</p>
        </div>
        
        {/* Logout button */}
        <button
          onClick={handleSignOut}
          className="w-full bg-primary-container text-on-primary-container px-6 py-3 rounded-2xl font-label-md mt-3"
        >
          Sign Out
        </button>
      </>
    )
  }

  // Not authenticated - show sign in button
  return (
    <a 
      href="auth.html" 
      className="block w-full bg-primary-container text-on-primary-container px-6 py-3 rounded-2xl font-label-md mt-3"
    >
      Sign In
    </a>
  )
}

export default MobileAuthMenu
