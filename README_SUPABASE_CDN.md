# Supabase CDN Setup for Plain HTML + JavaScript

Complete guide for using Supabase with plain HTML and JavaScript without ES modules.

## Problem Solved

**Issue**: `Failed to resolve module specifier "@supabase/supabase-js"`

**Solution**: Use Supabase CDN instead of ES module imports.

## Implementation

### 1. CDN Script Addition

Added Supabase CDN script to all HTML files:

```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
```

**Files Updated:**
- `index.html`
- `auth.html`
- `plan.html`
- `auth/callback.html`

### 2. Client Initialization

Changed from ES modules to CDN approach:

**Before (ES Modules):**
```javascript
import { createClient } from '@supabase/supabase-js'
export const supabase = createClient(URL, KEY)
```

**After (CDN):**
```javascript
const supabase = window.supabase.createClient(URL, KEY)
```

### 3. Updated Configuration

Using the current Supabase credentials:
```javascript
const supabase = window.supabase.createClient(
    'https://piygbsxvvptcivffhnvu.supabase.co',
    'sb_publishable_FnyuR71dNb05x2TVPPr0_A_mizcZUbP'
);
```

## File Changes

### HTML Files Updated

All HTML files now include:
1. **Supabase CDN script** in `<head>`
2. **Updated client initialization** in `<script>` tags
3. **Removed `type="module"`** from script tags

### JavaScript Files Updated

#### `lib/supabase.js` & `lib/supabaseClient.js`
- Removed ES module imports
- Added usage comments for CDN approach

#### `services/profileService.js`
- Updated to work without ES modules
- Made globally available via `window.profileService`

## Usage Examples

### Basic Authentication
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script>
    const supabase = window.supabase.createClient(URL, KEY);
    
    // Sign up
    async function signUp(email, password) {
        const { data, error } = await supabase.auth.signUp({ email, password });
        return { data, error };
    }
    
    // Sign in
    async function signIn(email, password) {
        const { data, error } = await supabase.auth.signInWithPassword({ email, password });
        return { data, error };
    }
    
    // Sign out
    async function signOut() {
        const { error } = await supabase.auth.signOut();
        return { error };
    }
</script>
```

### Database Operations
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="services/profileService.js"></script>
<script>
    // Access profiles table
    async function getProfile(userId) {
        const { data, error } = await window.profileService.getProfile(userId);
        return { data, error };
    }
    
    // Create profile
    async function createProfile(userId, userData) {
        const { data, error } = await window.profileService.createProfile(userId, userData);
        return { data, error };
    }
</script>
```

### Google OAuth
```html
<script>
    // Google sign in
    async function signInWithGoogle() {
        const { data, error } = await supabase.auth.signInWithOAuth({
            provider: 'google',
            options: {
                redirectTo: `${window.location.origin}/auth/callback.html`
            }
        });
        return { data, error };
    }
</script>
```

## Testing

### Test File Created
`test-supabase.html` - Comprehensive testing interface for:
- ✅ Connection testing
- ✅ Authentication methods
- ✅ Database access

### How to Test
1. Open `test-supabase.html` in browser
2. Click "Test Connection" to verify CDN works
3. Click "Test Auth Methods" to verify authentication
4. Click "Test Database Access" to verify database connectivity

## Benefits of CDN Approach

✅ **No build tools required** - Works directly in browser  
✅ **No module bundlers needed** - Plain HTML + JavaScript  
✅ **Instant setup** - Just add script tags  
✅ **Broad compatibility** - Works in all modern browsers  
✅ **Simplified deployment** - No build step required  

## Migration Guide

### From ES Modules to CDN

**1. Remove import statements:**
```javascript
// Remove
import { createClient } from '@supabase/supabase-js'
import { supabase } from './lib/supabaseClient'
```

**2. Add CDN script:**
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
```

**3. Update client initialization:**
```javascript
// Change from
const supabase = createClient(URL, KEY)

// To
const supabase = window.supabase.createClient(URL, KEY)
```

**4. Remove script type="module":**
```html
<!-- Change from -->
<script type="module">

<!-- To -->
<script>
```

**5. Make services global (if needed):**
```javascript
// In service files
if (typeof window !== 'undefined') {
    window.yourService = yourService
}
```

## Common Issues & Solutions

### Issue: "window.supabase is undefined"
**Solution**: Ensure CDN script loads before your code
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script>
    // Your code here
</script>
```

### Issue: "Cannot access 'supabase' before initialization"
**Solution**: Initialize supabase at the top of your script
```javascript
const supabase = window.supabase.createClient(URL, KEY);
// Rest of your code
```

### Issue: Service not available globally
**Solution**: Load service scripts after Supabase CDN
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="services/profileService.js"></script>
<script>
    // Now window.profileService is available
</script>
```

## File Structure After Migration

```
/ (root)
├── index.html              # Updated with CDN
├── auth.html               # Updated with CDN
├── plan.html               # Updated with CDN
├── auth/
│   └── callback.html       # Updated with CDN
├── test-supabase.html      # Test file (new)
├── lib/
│   ├── supabase.js         # Updated (no longer used)
│   └── supabaseClient.js   # Updated (no longer used)
└── services/
    └── profileService.js   # Updated for global access
```

## Environment Variables

For plain HTML setup, credentials are hardcoded in scripts:

```javascript
const supabase = window.supabase.createClient(
    'https://piygbsxvvptcivffhnvu.supabase.co',
    'sb_publishable_FnyuR71dNb05x2TVPPr0_A_mizcZUbP'
);
```

**Security Note**: In production, consider:
- Using environment variables in your build process
- Implementing proper CORS restrictions
- Using Row Level Security (RLS) in Supabase

## Next Steps

1. **Test the setup**: Open `test-supabase.html` to verify everything works
2. **Update your HTML files**: Use the CDN approach in all pages
3. **Remove unused files**: Delete ES module files if no longer needed
4. **Deploy**: Your setup now works without build tools

## Support

If you encounter issues:
1. Check browser console for errors
2. Verify CDN script loads before your code
3. Test with `test-supabase.html`
4. Ensure Supabase project is active and keys are correct
