# Enhanced Authentication Modal

A comprehensive authentication modal with Google OAuth, form validation, and seamless toggle functionality between Sign Up and Login modes.

## Features

✅ **Google OAuth Integration**: Continue with Google button for quick authentication  
✅ **Form Fields**: Name (signup only), Email, and Password with validation  
✅ **Toggle Functionality**: Seamless switching between Sign Up and Login  
✅ **Clean UI**: Minimal design with proper loading states and error handling  
✅ **Responsive**: Works on all screen sizes  
✅ **Accessible**: Semantic HTML and keyboard navigation  

## Components

### EnhancedAuthModal (`/components/EnhancedAuthModal.js`)

The main authentication modal component with all features integrated.

**Props:**
- `isOpen` (boolean): Controls modal visibility
- `onClose` (function): Callback when modal is closed

**Usage:**
```jsx
import EnhancedAuthModal from './components/EnhancedAuthModal'

function MyComponent() {
  const [showAuth, setShowAuth] = useState(false)

  return (
    <div>
      <button onClick={() => setShowAuth(true)}>
        Sign In
      </button>
      
      <EnhancedAuthModal 
        isOpen={showAuth} 
        onClose={() => setShowAuth(false)}
      />
    </div>
  )
}
```

## Authentication Methods

### 1. Google OAuth
```javascript
const { signInWithGoogle } = useAuth()

// Automatically redirects to Google OAuth flow
await signInWithGoogle()
```

### 2. Email/Password
```javascript
const { signIn, signUp } = useAuth()

// Sign in
await signIn(email, password)

// Sign up
await signUp(email, password)
```

## Form Fields

### Sign Up Mode:
- **Name** (required): User's full name
- **Email** (required): Valid email address
- **Password** (required): Minimum 6 characters

### Login Mode:
- **Email** (required): Valid email address
- **Password** (required): User's password

## UI Elements

### 1. Google Sign In Button
- Prominent "Continue with Google" button
- Google brand colors and logo
- Full-width button design

### 2. Form Divider
- Clean "or" separator between Google and email options
- Visual distinction between authentication methods

### 3. Email/Password Form
- Conditional name field (signup only)
- Input validation and error messages
- Loading states during submission

### 4. Toggle Links
- "Already have an account? Login" (in signup mode)
- "Don't have an account? Sign Up" (in login mode)
- Seamless mode switching

## Validation

### Client-side validation:
- Required field checking
- Email format validation
- Password minimum length (6 characters)
- Name requirement for signup

### Server-side validation:
- Supabase handles email uniqueness
- Password strength requirements
- OAuth provider validation

## Error Handling

### Common error messages:
- "Please fill in all required fields"
- "Please enter your name" (signup only)
- "Password must be at least 6 characters long"
- "User already registered"
- "Invalid login credentials"
- "Google sign-in failed"

### Success messages:
- "Login successful! Redirecting..."
- "Account created! Please check your email to confirm."
- "Redirecting to Google..."

## Integration Steps

### 1. Update AuthContext
The AuthContext already includes `signInWithGoogle` method:

```javascript
const { signIn, signUp, signInWithGoogle, signOut } = useAuth()
```

### 2. Configure Supabase OAuth
In your Supabase dashboard:
1. Go to Authentication → Providers
2. Enable Google provider
3. Add your Google OAuth credentials
4. Set redirect URL to your domain

### 3. Use the Modal
```jsx
import { AuthProvider } from './context/AuthContext'
import EnhancedAuthModal from './components/EnhancedAuthModal'

function App() {
  return (
    <AuthProvider>
      <YourApp />
    </AuthProvider>
  )
}
```

## Styling

The modal uses Tailwind CSS classes matching your design system:

- **Container**: `bg-surface border border-white/10 rounded-[28px]`
- **Inputs**: `bg-surface-container/50 border border-white/10`
- **Buttons**: `bg-primary-container text-on-primary-container`
- **Google Button**: `bg-white text-surface` with Google brand colors

## Accessibility

- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation support
- Focus management in modal
- Screen reader friendly

## Mobile Responsiveness

- Full-width modal on mobile
- Touch-friendly button sizes
- Proper spacing and layout
- Readable text sizes

## File Structure

```
/components/
  └── EnhancedAuthModal.js    # Main modal component
/context/
  └── AuthContext.js          # Updated with Google OAuth
/examples/
  └── EnhancedAuthExample.js  # Usage example
```

## Environment Variables

Ensure your `.env.local` has Supabase configuration:
```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## Customization

### Custom Styling
You can customize the modal by modifying the Tailwind classes in `EnhancedAuthModal.js`:

```jsx
// Example: Custom button colors
<button className="bg-blue-500 text-white py-3 rounded-xl">
  Custom Button
</button>
```

### Additional Fields
Add more form fields by extending the state and validation:

```jsx
const [phone, setPhone] = useState('')

// Add to form
<input
  type="tel"
  value={phone}
  onChange={(e) => setPhone(e.target.value)}
  placeholder="Phone number"
/>
```

### Custom OAuth Providers
Add more OAuth providers in AuthContext:

```javascript
const signInWithGitHub = async () => {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'github',
    options: { redirectTo: `${window.location.origin}/plan.html` }
  })
  // ...
}
```
