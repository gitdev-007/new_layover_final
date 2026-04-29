import React, { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '../lib/supabaseClient'
import { profileService } from '../services/profileService'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [session, setSession] = useState(null)

  // Detect if user is logged in on app load
  useEffect(() => {
    const getSession = async () => {
      try {
        const { data: { session }, error } = await supabase.auth.getSession()
        
        if (error) {
          console.error('Error getting session:', error)
        } else {
          setSession(session)
          setUser(session?.user ?? null)
          
          // Fetch user profile if user exists
          if (session?.user) {
            await fetchUserProfile(session.user.id)
          } else {
            setProfile(null)
          }
        }
      } catch (error) {
        console.error('Session error:', error)
      } finally {
        setLoading(false)
      }
    }

    getSession()

    // Listen for auth state changes
    supabase.auth.onAuthStateChange(async (event, session) => {
      console.log('Auth state changed:', event, session)
      
      if (event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') {
        setSession(session)
        setUser(session?.user ?? null)
        
        if (session?.user) {
          await fetchUserProfile(session.user.id)
          
          // Create profile if it doesn't exist
          if (!profile) {
            await profileService.createProfile(session.user.id, {
              name: session.user.user_metadata?.name || '',
              email: session.user.email || ''
            })
            await fetchUserProfile(session.user.id)
          }
        }
      } else if (event === 'SIGNED_OUT') {
        setSession(null)
        setUser(null)
        setProfile(null)
        
        // Redirect to home page if user was on protected page
        if (window.location.pathname.includes('plan.html')) {
          window.location.href = '/index.html'
        }
      }
    })

    return () => {
      subscription.unsubscribe()
    }
  }, [])

  // Fetch user profile function
  const fetchUserProfile = async (userId) => {
    try {
      const { data, error } = await profileService.getProfile(userId)
      
      if (error) {
        console.error('Error fetching profile:', error)
        setProfile(null)
      } else {
        setProfile(data)
      }
    } catch (error) {
      console.error('Profile fetch error:', error)
      setProfile(null)
    }
  }

  // Authentication functions
  const signUp = async (email, password, name = '') => {
    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            name: name.trim(),
            full_name: name.trim()
          }
        }
      })

      if (error) throw error
      
      return { data, error: null }
    } catch (error) {
      console.error('Sign up error:', error)
      return { data: null, error }
    }
  }

  const signIn = async (email, password) => {
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
      })

      if (error) throw error
      
      return { data, error: null }
    } catch (error) {
      console.error('Sign in error:', error)
      return { data: null, error }
    }
  }

  const signInWithGoogle = async () => {
    try {
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback.html`,
          queryParams: {
            access_type: 'offline',
            prompt: 'consent',
          }
        }
      })

      if (error) throw error
      
      return { data, error: null }
    } catch (error) {
      console.error('Google sign in error:', error)
      return { data: null, error }
    }
  }

  // Handle OAuth redirect callback
  const handleOAuthCallback = async () => {
    try {
      const { data, error } = await supabase.auth.getSession()
      
      if (error) throw error
      
      if (data.session) {
        // Successfully authenticated via OAuth
        window.location.href = '/plan.html'
      }
      
      return { data, error: null }
    } catch (error) {
      console.error('OAuth callback error:', error)
      return { data: null, error }
    }
  }

  const signOut = async () => {
    try {
      const { error } = await supabase.auth.signOut()
      
      if (error) throw error
      
      // State will be updated by the onAuthStateChange listener
    } catch (error) {
      console.error('Sign out error:', error)
    }
  }

  const value = {
    user,
    profile,
    session,
    loading,
    signUp,
    signIn,
    signInWithGoogle,
    handleOAuthCallback,
    signOut,
    updateProfile: async (updates) => {
      if (!user) return { error: { message: 'No user logged in' } }
      
      try {
        const { data, error } = await profileService.updateProfile(user.id, updates)
        if (!error) {
          setProfile(data)
        }
        return { data, error }
      } catch (error) {
        return { data: null, error }
      }
    },
    isAuthenticated: !!user,
    displayName: profile?.name || user?.user_metadata?.name || user?.email?.split('@')[0] || 'User'
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
