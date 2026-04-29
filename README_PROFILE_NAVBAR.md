# Profile Fetching and Dynamic Navbar Implementation

Complete implementation of profile fetching from Supabase with dynamic navbar updates based on authentication state.

## Overview

This implementation provides:

✅ **Profile fetching** from "profiles" table using user ID  
✅ **Welcome message** display with user name  
✅ **Logout button** with Supabase sign out  
✅ **Dynamic UI updates** based on auth state changes  
✅ **Mobile responsive** auth menu  

## Database Schema

### Profiles Table

```sql
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  name TEXT,
  email TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Profile Creation Flow:**
1. User signs up → Auth user created
2. Profile automatically created with user metadata
3. Profile fetched and stored in context

## Components

### 1. Profile Service (`/services/profileService.js`)

Handles all profile-related database operations:

```javascript
export const profileService = {
  // Fetch user profile by user ID
  async getProfile(userId) {
    const { data, error } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', userId)
      .single()
    return { data, error }
  },

  // Create profile for new user
  async createProfile(userId, userData) {
    const profile = {
      id: userId,
      name: userData.name || '',
      email: userData.email || '',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    // Insert into profiles table
  },

  // Update user profile
  async updateProfile(userId, updates) {
    const { data, error } = await supabase
      .from('profiles')
      .update({ ...updates, updated_at: new Date().toISOString() })
      .eq('id', userId)
    return { data, error }
  }
}
```

### 2. Enhanced AuthContext (`/context/AuthContext.js`)

Updated to include profile management:

```javascript
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  // Fetch user profile function
  const fetchUserProfile = async (userId) => {
    const { data, error } = await profileService.getProfile(userId)
    if (!error) {
      setProfile(data)
    }
  }

  // Update profile function
  const updateProfile = async (updates) => {
    const { data, error } = await profileService.updateProfile(user.id, updates)
    if (!error) {
      setProfile(data)
    }
    return { data, error }
  }

  // Display name helper
  const displayName = profile?.name || 
                     user?.user_metadata?.name || 
                     user?.email?.split('@')[0] || 
                     'User'
}
```

### 3. Dynamic Navbar (`/components/DynamicNavbar.js`)

Responsive navbar that updates based on auth state:

```javascript
const DynamicNavbar = () => {
  const { isAuthenticated, displayName, signOut, loading } = useAuth()

  if (loading) {
    return <LoadingSkeleton />
  }

  if (isAuthenticated) {
    return (
      <div className="flex items-center gap-4">
        <span className="text-secondary/60 text-sm">Welcome,</span>
        <span className="text-white text-sm font-medium">{displayName}</span>
        <button onClick={signOut}>Sign Out</button>
      </div>
    )
  }

  return <SignInButton />
}
```

### 4. Mobile Auth Menu (`/components/MobileAuthMenu.js`)

Mobile-optimized auth menu with same functionality:

```javascript
const MobileAuthMenu = () => {
  const { isAuthenticated, displayName, signOut } = useAuth()

  if (isAuthenticated) {
    return (
      <>
        <div className="px-4 py-3">
          <p className="text-primary text-sm">Welcome, {displayName}</p>
        </div>
        <button onClick={signOut}>Sign Out</button>
      </>
    )
  }

  return <SignInButton />
}
```

## Authentication Flow

### 1. Initial App Load
```javascript
// AuthContext useEffect
useEffect(() => {
  const getSession = async () => {
    const { data: { session } } = await supabase.auth.getSession()
    
    if (session?.user) {
      setUser(session.user)
      await fetchUserProfile(session.user.id) // Fetch profile
    }
  }
  
  getSession()
}, [])
```

### 2. User Sign In
```javascript
// Auth state change listener
supabase.auth.onAuthStateChange(async (event, session) => {
  if (event === 'SIGNED_IN') {
    setUser(session.user)
    
    // Fetch or create profile
    let { data: profile } = await profileService.getProfile(session.user.id)
    
    if (!profile) {
      // Create profile if doesn't exist
      await profileService.createProfile(session.user.id, {
        name: session.user.user_metadata?.name || '',
        email: session.user.email
      })
      
      // Fetch newly created profile
      const { data } = await profileService.getProfile(session.user.id)
      setProfile(data)
    } else {
      setProfile(profile)
    }
  }
})
```

### 3. User Sign Out
```javascript
const signOut = async () => {
  await supabase.auth.signOut()
  // Auth state listener will update UI automatically
  setUser(null)
  setProfile(null)
}
```

## Display Name Priority

The system uses a priority hierarchy for displaying user names:

```javascript
const displayName = 
  profile?.name ||           // 1. Profile table name (highest priority)
  user?.user_metadata?.name || // 2. User metadata name
  user?.email?.split('@')[0] || // 3. Email username
  'User'                     // 4. Fallback
```

**Priority Order:**
1. **Profile name** - User's preferred name from profiles table
2. **Metadata name** - Name stored during signup
3. **Email username** - First part of email address
4. **"User"** - Default fallback

## Dynamic UI Updates

### Auth State Changes
All UI updates happen automatically through React state:

```javascript
// Any component using useAuth will automatically update
const { isAuthenticated, displayName, profile } = useAuth()

// UI re-renders when auth state changes
return (
  <div>
    {isAuthenticated ? (
      <span>Welcome, {displayName}</span>
    ) : (
      <a href="/auth">Sign In</a>
    )}
  </div>
)
```

### Loading States
```javascript
// Show loading skeleton during auth checks
if (loading) {
  return (
    <div className="animate-pulse">
      <div className="h-8 w-20 bg-surface-container/50 rounded-full"></div>
    </div>
  )
}
```

## Integration Steps

### 1. Set up Database
```sql
-- Create profiles table in Supabase
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  name TEXT,
  email TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Enable RLS (Row Level Security)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Create policy for users to read their own profile
CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

-- Create policy for users to update their own profile
CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);
```

### 2. Wrap App with AuthProvider
```jsx
import { AuthProvider } from './context/AuthContext'

function App() {
  return (
    <AuthProvider>
      <YourAppComponents />
    </AuthProvider>
  )
}
```

### 3. Use Dynamic Navbar
```jsx
import DynamicNavbar from './components/DynamicNavbar'

function YourLayout() {
  return (
    <header>
      <YourLogo />
      <Navigation />
      <DynamicNavbar /> {/* Replaces static auth buttons */}
    </header>
  )
}
```

### 4. Mobile Menu Integration
```jsx
import MobileAuthMenu from './components/MobileAuthMenu'

function MobileMenu() {
  return (
    <div className="mobile-menu">
      <NavigationLinks />
      <MobileAuthMenu /> {/* Mobile auth menu */}
    </div>
  )
}
```

## Usage Examples

### Accessing Profile Data
```javascript
import { useAuth } from './context/AuthContext'

function UserProfile() {
  const { user, profile, displayName, updateProfile } = useAuth()

  const handleUpdateName = async (newName) => {
    await updateProfile({ name: newName })
    // Profile and displayName update automatically
  }

  return (
    <div>
      <h1>Welcome, {displayName}</h1>
      <p>Email: {user?.email}</p>
      <p>Profile Name: {profile?.name}</p>
      <p>Created: {new Date(profile?.created_at).toLocaleDateString()}</p>
    </div>
  )
}
```

### Conditional Rendering
```javascript
function ProtectedComponent() {
  const { isAuthenticated, profile } = useAuth()

  if (!isAuthenticated) {
    return <PleaseSignIn />
  }

  return (
    <div>
      <h1>Hello, {profile?.name || 'User'}!</h1>
      {/* Protected content */}
    </div>
  )
}
```

## Error Handling

### Profile Fetch Errors
```javascript
const fetchUserProfile = async (userId) => {
  try {
    const { data, error } = await profileService.getProfile(userId)
    
    if (error) {
      console.error('Profile fetch error:', error)
      setProfile(null) // Fallback to user metadata
    } else {
      setProfile(data)
    }
  } catch (error) {
    console.error('Unexpected error:', error)
    setProfile(null)
  }
}
```

### Network Errors
```javascript
const signOut = async () => {
  try {
    await supabase.auth.signOut()
    // UI updates automatically through auth state listener
  } catch (error) {
    console.error('Sign out error:', error)
    // Still update UI to prevent stuck state
    setUser(null)
    setProfile(null)
  }
}
```

## Best Practices

1. **Always handle loading states** to prevent UI flicker
2. **Use fallback values** for profile data
3. **Implement proper error boundaries** for auth failures
4. **Cache profile data** to reduce database calls
5. **Use optimistic updates** for better UX
6. **Implement proper RLS policies** in Supabase

## File Structure

```
/context/
  └── AuthContext.js              # Enhanced with profile management
/services/
  └── profileService.js           # Profile database operations
/components/
  ├── DynamicNavbar.js            # Desktop responsive navbar
  └── MobileAuthMenu.js           # Mobile auth menu
/examples/
  └── DynamicNavbarExample.js     # Complete integration example
```

## Troubleshooting

### Profile Not Loading
1. Check if profiles table exists
2. Verify RLS policies allow access
3. Check network requests in browser console
4. Ensure user ID matches profile ID

### Display Name Not Showing
1. Check profile.name field
2. Verify user_metadata.name
3. Check email format for fallback
4. Verify auth state is properly loaded

### Logout Not Working
1. Check Supabase sign out function
2. Verify auth state listener is active
3. Check for JavaScript errors
4. Ensure proper cleanup on sign out
