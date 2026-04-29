import React from 'react'
import { useAuth } from '../context/AuthContext'

const DynamicNavbar = () => {
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
      <div className="hidden md:flex items-center gap-6">
        <div className="animate-pulse">
          <div className="h-8 w-20 bg-surface-container/50 rounded-full"></div>
        </div>
      </div>
    )
  }

  if (isAuthenticated) {
    return (
      <div className="hidden md:flex items-center gap-4">
        {/* Welcome message */}
        <div className="flex items-center gap-3">
          <span className="text-secondary/60 text-sm">Welcome,</span>
          <span className="text-white text-sm font-medium">{displayName}</span>
        </div>
        
        {/* Logout button */}
        <button
          onClick={handleSignOut}
          className="px-4 py-2 rounded-full border border-white/10 bg-white/[0.03] text-secondary hover:text-white hover:bg-white/[0.06] transition-colors text-sm"
        >
          Sign Out
        </button>
      </div>
    )
  }

  // Not authenticated - show sign in button
  return (
    <div className="hidden md:flex items-center gap-6">
      <a 
        href="auth.html" 
        className="px-4 py-2 rounded-full border border-white/10 bg-white/[0.03] text-secondary hover:text-white hover:bg-white/[0.06] transition-colors"
      >
        Sign In
      </a>
    </div>
  )
}

export default DynamicNavbar
