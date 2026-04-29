import React, { useState } from 'react'
import { AuthProvider } from '../context/AuthContext'
import EnhancedAuthModal from '../components/EnhancedAuthModal'

// Complete authentication implementation example
const FullAuthExample = () => {
  const [showAuthModal, setShowAuthModal] = useState(false)

  return (
    <AuthProvider>
      <div className="min-h-screen bg-surface text-white p-8">
        <h1 className="text-3xl font-bold mb-8">Complete Authentication Implementation</h1>
        
        {/* Authentication buttons */}
        <div className="space-y-4 mb-12">
          <button
            onClick={() => setShowAuthModal(true)}
            className="bg-primary-container text-on-primary-container px-6 py-3 rounded-xl font-medium hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            Open Authentication Modal
          </button>
        </div>

        {/* Features breakdown */}
        <div className="space-y-6">
          <h2 className="text-2xl font-semibold mb-4">Implemented Features:</h2>
          
          {/* 1. SIGN UP */}
          <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
            <h3 className="text-lg font-medium mb-3 text-primary">1. SIGN UP</h3>
            <div className="space-y-2 text-secondary/80">
              <p>✅ Email + password signup</p>
              <p>✅ Name passed in user metadata</p>
              <p>✅ Redirect after successful signup</p>
              <p>✅ Email confirmation handling</p>
            </div>
            <div className="mt-4 p-4 bg-surface/50 rounded-lg">
              <code className="text-sm text-primary">
                {`await signUp(email, password, name)`}
              </code>
            </div>
          </div>

          {/* 2. LOGIN */}
          <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
            <h3 className="text-lg font-medium mb-3 text-primary">2. LOGIN</h3>
            <div className="space-y-2 text-secondary/80">
              <p>✅ Email + password login</p>
              <p>✅ Show error if invalid credentials</p>
              <p>✅ Loading states during authentication</p>
              <p>✅ Auto-redirect on success</p>
            </div>
            <div className="mt-4 p-4 bg-surface/50 rounded-lg">
              <code className="text-sm text-primary">
                {`await signIn(email, password)`}
              </code>
            </div>
          </div>

          {/* 3. GOOGLE LOGIN */}
          <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
            <h3 className="text-lg font-medium mb-3 text-primary">3. GOOGLE LOGIN</h3>
            <div className="space-y-2 text-secondary/80">
              <p>✅ Supabase Google OAuth login</p>
              <p>✅ Handle redirect after login</p>
              <p>✅ OAuth callback page implementation</p>
              <p>✅ Error handling for OAuth flow</p>
            </div>
            <div className="mt-4 p-4 bg-surface/50 rounded-lg">
              <code className="text-sm text-primary">
                {`await signInWithGoogle()`}
              </code>
            </div>
          </div>

          {/* 4. LOADING & ERROR HANDLING */}
          <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
            <h3 className="text-lg font-medium mb-3 text-primary">4. LOADING + ERROR HANDLING</h3>
            <div className="space-y-2 text-secondary/80">
              <p>✅ Loading spinners during auth operations</p>
              <p>✅ User-friendly error messages</p>
              <p>✅ Success feedback and notifications</p>
              <p>✅ Form validation and error states</p>
            </div>
            <div className="mt-4 p-4 bg-surface/50 rounded-lg">
              <code className="text-sm text-primary">
                {`// Error handling examples
"Invalid login credentials"
"User already registered"
"Password must be at least 6 characters"
"Google sign-in failed"`}
              </code>
            </div>
          </div>
        </div>

        {/* Authentication Flow Diagram */}
        <div className="mt-12 bg-surface-container/50 rounded-xl p-6 border border-white/10">
          <h3 className="text-lg font-medium mb-4">Authentication Flow:</h3>
          <div className="space-y-3 text-sm">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                <span className="text-primary text-xs">1</span>
              </div>
              <span className="text-secondary/80">User opens auth modal → Shows login/signup options</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                <span className="text-primary text-xs">2</span>
              </div>
              <span className="text-secondary/80">Choose auth method → Google OAuth or Email/Password</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                <span className="text-primary text-xs">3</span>
              </div>
              <span className="text-secondary/80">Complete authentication → Loading state shown</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                <span className="text-primary text-xs">4</span>
              </div>
              <span className="text-secondary/80">Success/Error → Feedback displayed</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                <span className="text-primary text-xs">5</span>
              </div>
              <span className="text-secondary/80">Redirect → User sent to plan.html on success</span>
            </div>
          </div>
        </div>

        {/* Enhanced Auth Modal */}
        <EnhancedAuthModal 
          isOpen={showAuthModal} 
          onClose={() => setShowAuthModal(false)}
        />
      </div>
    </AuthProvider>
  )
}

export default FullAuthExample
