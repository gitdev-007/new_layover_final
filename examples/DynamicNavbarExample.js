import React, { useState } from 'react'
import { AuthProvider } from '../context/AuthContext'
import DynamicNavbar from '../components/DynamicNavbar'
import MobileAuthMenu from '../components/MobileAuthMenu'

// Example showing how to integrate dynamic navbar with existing HTML structure
const DynamicNavbarExample = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <AuthProvider>
      <div className="min-h-screen bg-surface text-white">
        {/* Header with Dynamic Navbar */}
        <header className="fixed top-0 w-full z-50 bg-neutral-950/75 backdrop-blur-md shadow-2xl shadow-black/40 border-b border-white/10">
          <div className="max-w-7xl mx-auto px-6 md:px-8 py-4 flex justify-between items-center gap-6">
            {/* Logo */}
            <div className="flex items-center gap-8 lg:gap-12">
              <a className="text-2xl font-black tracking-tighter text-white" href="#">LayoverX</a>
              
              {/* Navigation Links */}
              <nav className="hidden md:flex items-center gap-6 lg:gap-8 font-['Plus_Jakarta_Sans'] text-sm tracking-wide">
                <a className="text-orange-500 border-b-2 border-orange-500 pb-1 transition-colors" href="#">Explore</a>
                <a className="text-neutral-400 hover:text-white transition-colors" href="#">About</a>
                <a className="text-neutral-400 hover:text-white transition-colors" href="#">Contact</a>
              </nav>
            </div>

            {/* Dynamic Auth Navbar */}
            <DynamicNavbar />

            {/* Mobile Menu Toggle */}
            <button 
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden w-11 h-11 rounded-full border border-white/10 bg-white/5 text-white flex items-center justify-center"
            >
              <span className="material-symbols-outlined">
                {mobileMenuOpen ? 'close' : 'menu'}
              </span>
            </button>
          </div>

          {/* Mobile Menu */}
          <div className={`md:hidden border-t border-white/10 bg-neutral-950/95 backdrop-blur-xl transition-all duration-300 ${mobileMenuOpen ? 'block' : 'hidden'}`}>
            <div className="px-6 py-5 space-y-3 font-['Plus_Jakarta_Sans']">
              {/* Mobile Navigation Links */}
              <a className="block rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-4 text-secondary hover:text-white transition" href="#">Explore</a>
              <a className="block rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-4 text-secondary hover:text-white transition" href="#">About</a>
              <a className="block rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-4 text-secondary hover:text-white transition" href="#">Contact</a>
              
              {/* Mobile Auth Menu */}
              <MobileAuthMenu />
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="pt-24 px-8">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl font-bold text-white mb-8">Dynamic Navbar Implementation</h1>
            
            <div className="space-y-6">
              <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
                <h2 className="text-2xl font-semibold mb-4 text-primary">Features Implemented:</h2>
                <ul className="space-y-3 text-secondary/80">
                  <li>✅ Profile fetching from "profiles" table using user ID</li>
                  <li>✅ "Welcome [Name]" display in navbar</li>
                  <li>✅ Logout button with Supabase sign out</li>
                  <li>✅ Dynamic UI updates based on auth state</li>
                  <li>✅ Mobile responsive auth menu</li>
                  <li>✅ Loading states during auth checks</li>
                </ul>
              </div>

              <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
                <h2 className="text-2xl font-semibold mb-4 text-primary">Auth State Flow:</h2>
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-primary text-xs">1</span>
                    </div>
                    <div>
                      <h3 className="font-medium text-white">Initial Load</h3>
                      <p className="text-secondary/60 text-sm">App checks for existing session and fetches user profile</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-primary text-xs">2</span>
                    </div>
                    <div>
                      <h3 className="font-medium text-white">Profile Fetching</h3>
                      <p className="text-secondary/60 text-sm">User profile is fetched from "profiles" table using user ID</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-primary text-xs">3</span>
                    </div>
                    <div>
                      <h3 className="font-medium text-white">UI Update</h3>
                      <p className="text-secondary/60 text-sm">Navbar updates to show "Welcome [Name]" and logout button</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-primary text-xs">4</span>
                    </div>
                    <div>
                      <h3 className="font-medium text-white">Sign Out</h3>
                      <p className="text-secondary/60 text-sm">Logout button calls Supabase sign out and updates UI automatically</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
                <h2 className="text-2xl font-semibold mb-4 text-primary">Profile Display Priority:</h2>
                <div className="bg-surface/50 rounded-lg p-4 font-mono text-sm">
                  <code className="text-primary">
                    {`displayName = 
  profile?.name || 
  user?.user_metadata?.name || 
  user?.email?.split('@')[0] || 
  'User'`}
                  </code>
                </div>
                <p className="text-secondary/60 text-sm mt-3">
                  The system prioritizes profile name, then user metadata, then email username, then fallback to "User"
                </p>
              </div>

              <div className="bg-surface-container/50 rounded-xl p-6 border border-white/10">
                <h2 className="text-2xl font-semibold mb-4 text-primary">Database Schema:</h2>
                <div className="bg-surface/50 rounded-lg p-4 font-mono text-sm">
                  <code className="text-secondary">
                    {`-- profiles table structure
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  name TEXT,
  email TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);`}
                  </code>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </AuthProvider>
  )
}

export default DynamicNavbarExample
