import React from 'react'
import { useAuth } from '../context/AuthContext'

// Example component showing how to use authentication state
const AuthExample = () => {
  const { user, loading, isAuthenticated, signIn, signUp, signOut } = useAuth()

  if (loading) {
    return <div>Loading authentication state...</div>
  }

  return (
    <div>
      {isAuthenticated ? (
        <div>
          <h1>Welcome, {user?.email}</h1>
          <p>User is authenticated</p>
          <button onClick={signOut}>Sign Out</button>
        </div>
      ) : (
        <div>
          <h1>Please sign in</h1>
          <p>User is not authenticated</p>
          <button onClick={() => signIn('user@example.com', 'password')}>
            Sign In
          </button>
          <button onClick={() => signUp('user@example.com', 'password')}>
            Sign Up
          </button>
        </div>
      )}
    </div>
  )
}

export default AuthExample
