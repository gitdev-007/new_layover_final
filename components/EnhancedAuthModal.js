import React, { useState } from 'react'
import { useAuth } from '../context/AuthContext'

const EnhancedAuthModal = ({ isOpen, onClose }) => {
  const { signIn, signUp, signInWithGoogle, loading } = useAuth()
  const [isLogin, setIsLogin] = useState(true)
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  if (!isOpen) return null

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    try {
      // Basic validation
      if (!email || !password) {
        setError('Please fill in all required fields')
        return
      }

      if (!isLogin && !name.trim()) {
        setError('Please enter your name')
        return
      }

      if (password.length < 6) {
        setError('Password must be at least 6 characters long')
        return
      }

      const { error } = isLogin 
        ? await signIn(email, password)
        : await signUp(email, password, name)

      if (error) {
        setError(error.message)
      } else {
        if (isLogin) {
          setSuccess('Login successful! Redirecting...')
          setTimeout(() => {
            onClose()
            // Redirect will be handled by AuthContext
          }, 1500)
        } else {
          setSuccess('Account created! Please check your email to confirm.')
          if (!error) {
            // Clear form on successful signup
            setName('')
            setEmail('')
            setPassword('')
          }
        }
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.')
    }
  }

  const handleGoogleSignIn = async () => {
    try {
      setError('')
      const { error } = await signInWithGoogle()
      
      if (error) {
        setError(error.message)
      } else {
        // OAuth will redirect automatically, show loading state
        setSuccess('Redirecting to Google...')
        setTimeout(() => {
          onClose()
        }, 1000)
      }
    } catch (err) {
      setError('Google sign-in failed. Please try again.')
    }
  }

  const handleClose = () => {
    if (!loading) {
      onClose()
      setError('')
      setSuccess('')
      setName('')
      setEmail('')
      setPassword('')
    }
  }

  const toggleMode = () => {
    setIsLogin(!isLogin)
    setError('')
    setSuccess('')
    setName('')
    setEmail('')
    setPassword('')
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div className="bg-surface border border-white/10 rounded-[28px] p-8 max-w-md w-full">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-white">
            {isLogin ? 'Welcome Back' : 'Create Account'}
          </h2>
          <button
            onClick={handleClose}
            disabled={loading}
            className="text-secondary hover:text-white transition-colors disabled:opacity-50"
          >
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>

        {/* Google Sign In */}
        <button
          onClick={handleGoogleSignIn}
          disabled={loading}
          className="w-full flex items-center justify-center gap-3 bg-white text-surface py-3 rounded-xl font-medium hover:bg-white/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed mb-6"
        >
          <svg className="w-5 h-5" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Continue with Google
        </button>

        {/* Divider */}
        <div className="flex items-center gap-4 mb-6">
          <div className="flex-1 h-px bg-white/10"></div>
          <span className="text-secondary/60 text-sm">or</span>
          <div className="flex-1 h-px bg-white/10"></div>
        </div>

        {/* Messages */}
        {error && (
          <div className="mb-4 p-3 rounded-xl bg-error-container/10 border border-error-container/20 text-error text-sm">
            {error}
          </div>
        )}
        
        {success && (
          <div className="mb-4 p-3 rounded-xl bg-primary/10 border border-primary/20 text-primary text-sm">
            {success}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Name field - only for signup */}
          {!isLogin && (
            <div>
              <label className="block text-sm font-medium text-secondary/80 mb-2">
                Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required={!isLogin}
                placeholder="John Doe"
                className="w-full px-4 py-3 bg-surface-container/50 border border-white/10 rounded-xl text-white placeholder-secondary/40 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
              />
            </div>
          )}

          {/* Email field */}
          <div>
            <label className="block text-sm font-medium text-secondary/80 mb-2">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="you@example.com"
              className="w-full px-4 py-3 bg-surface-container/50 border border-white/10 rounded-xl text-white placeholder-secondary/40 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
            />
          </div>

          {/* Password field */}
          <div>
            <label className="block text-sm font-medium text-secondary/80 mb-2">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
              minLength="6"
              className="w-full px-4 py-3 bg-surface-container/50 border border-white/10 rounded-xl text-white placeholder-secondary/40 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
            />
          </div>

          {/* Submit button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-container text-on-primary-container py-3 rounded-xl font-label-md hover:scale-[1.02] active:scale-[0.98] transition-all shadow-lg shadow-primary-container/20 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="material-symbols-outlined animate-spin">refresh</span>
                {isLogin ? 'Signing In...' : 'Creating Account...'}
              </span>
            ) : (
              isLogin ? 'Sign In' : 'Create Account'
            )}
          </button>
        </form>

        {/* Toggle link */}
        <div className="mt-6 text-center">
          <span className="text-secondary/60 text-sm">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
          </span>
          <button
            onClick={toggleMode}
            disabled={loading}
            className="text-primary hover:text-primary/80 text-sm font-medium transition-colors disabled:opacity-50"
          >
            {isLogin ? 'Sign Up' : 'Login'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default EnhancedAuthModal
