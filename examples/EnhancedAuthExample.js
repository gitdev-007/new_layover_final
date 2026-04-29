import React, { useState } from 'react'
import { AuthProvider } from '../context/AuthContext'
import EnhancedAuthModal from '../components/EnhancedAuthModal'

// Example of how to use the EnhancedAuthModal
const EnhancedAuthExample = () => {
  const [showAuthModal, setShowAuthModal] = useState(false)

  return (
    <AuthProvider>
      <div className="min-h-screen bg-surface text-white p-8">
        <h1 className="text-3xl font-bold mb-8">Enhanced Authentication Example</h1>
        
        {/* Button to open auth modal */}
        <div className="space-y-4">
          <button
            onClick={() => setShowAuthModal(true)}
            className="bg-primary-container text-on-primary-container px-6 py-3 rounded-xl font-medium hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            Open Authentication Modal
          </button>
        </div>

        {/* Features demonstration */}
        <div className="mt-12 space-y-6">
          <h2 className="text-2xl font-semibold mb-4">Features:</h2>
          
          <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
            <h3 className="text-lg font-medium mb-2">✅ Google OAuth Integration</h3>
            <p className="text-secondary/80">Continue with Google button for quick authentication</p>
          </div>

          <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
            <h3 className="text-lg font-medium mb-2">✅ Form Fields</h3>
            <p className="text-secondary/80">Name (signup only), Email, and Password fields with validation</p>
          </div>

          <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
            <h3 className="text-lg font-medium mb-2">✅ Toggle Functionality</h3>
            <p className="text-secondary/80">Seamless switching between Sign Up and Login modes</p>
          </div>

          <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
            <h3 className="text-lg font-medium mb-2">✅ Clean UI</h3>
            <p className="text-secondary/80">Minimal design with proper loading states and error handling</p>
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

export default EnhancedAuthExample
