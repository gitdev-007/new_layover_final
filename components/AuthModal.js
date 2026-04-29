import React, { useState } from 'react'
import { useAuth } from '../context/AuthContext'

const AuthModal = ({ isOpen, onClose }) => {
  const { signIn, signUp, loading } = useAuth()
  const [isLogin, setIsLogin] = useState(true)
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
      const { error } = isLogin 
        ? await signIn(email, password)
        : await signUp(email, password)

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
            setEmail('')
            setPassword('')
          }
        }
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.')
    }
  }

  const handleClose = () => {
    if (!loading) {
      onClose()
      setError('')
      setSuccess('')
      setEmail('')
      setPassword('')
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="bg-surface border border-white/10 rounded-[28px] p-8 max-w-md w-full mx-4">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-white">
            {isLogin ? 'Sign In' : 'Sign Up'}
          </h2>
          <button
            onClick={handleClose}
            disabled={loading}
            className="text-secondary hover:text-white transition-colors disabled:opacity-50"
          >
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>

        {/* Toggle */}
        <div className="flex bg-surface-container/50 rounded-full p-1 mb-6">
          <button
            onClick={() => {
              setIsLogin(true)
              setError('')
              setSuccess('')
            }}
            className={`flex-1 py-2 px-4 rounded-full text-sm font-medium transition-all ${
              isLogin 
                ? 'bg-primary-container text-on-primary-container' 
                : 'text-secondary hover:text-white'
            }`}
          >
            Login
          </button>
          <button
            onClick={() => {
              setIsLogin(false)
              setError('')
              setSuccess('')
            }}
            className={`flex-1 py-2 px-4 rounded-full text-sm font-medium transition-all ${
              !isLogin 
                ? 'bg-primary-container text-on-primary-container' 
                : 'text-secondary hover:text-white'
            }`}
          >
            Sign Up
          </button>
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
              className="w-full px-4 py-3 bg-surface-container/50 border border-white/10 rounded-xl text-white placeholder-secondary/40 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-container text-on-primary-container py-3 rounded-xl font-label-md hover:scale-[1.02] active:scale-[0.98] transition-all shadow-lg shadow-primary-container/20 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="material-symbols-outlined animate-spin">refresh</span>
                {isLogin ? 'Signing In...' : 'Signing Up...'}
              </span>
            ) : (
              isLogin ? 'Sign In' : 'Sign Up'
            )}
          </button>
        </form>
      </div>
    </div>
  )
}

export default AuthModal
