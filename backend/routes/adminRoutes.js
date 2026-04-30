import { Router } from 'express';
import supabaseClient from '../supabaseClient.js';

const router = Router();

/**
 * Admin middleware - verify admin role
 * In production, this should check if user has admin role
 */
async function requireAdmin(req, res, next) {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader) {
      return res.status(401).json({
        success: false,
        message: 'Authentication required'
      });
    }

    const token = authHeader.replace('Bearer ', '');
    const { data: { user }, error: authError } = await supabaseClient.auth.getUser(token);

    if (authError || !user) {
      return res.status(401).json({
        success: false,
        message: 'Invalid or expired token'
      });
    }

    // Store user for later use
    req.user = user;
    next();

  } catch (error) {
    console.error('Admin auth error:', error);
    res.status(500).json({
      success: false,
      message: 'Authentication check failed'
    });
  }
}

/**
 * POST /admin/update-status/:id
 * Update upload status (admin only)
 */
router.post('/update-status/:id', requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const { status } = req.body;

    // Validate status
    const allowedStatuses = ['approved', 'rejected', 'verified', 'failed'];
    if (!status || !allowedStatuses.includes(status)) {
      return res.status(400).json({
        success: false,
        message: `Invalid status. Allowed: ${allowedStatuses.join(', ')}`
      });
    }

    // Update the upload
    const { data: updated, error: updateError } = await supabaseClient
      .from('qr_uploads')
      .update({
        status: status,
        reviewed_by: req.user.id,
        reviewed_at: new Date().toISOString()
      })
      .eq('id', id)
      .select()
      .single();

    if (updateError) {
      throw new Error(`Update failed: ${updateError.message}`);
    }

    if (!updated) {
      return res.status(404).json({
        success: false,
        message: 'QR upload not found'
      });
    }

    res.json({
      success: true,
      message: `Status updated to ${status}`,
      data: {
        id: updated.id,
        status: updated.status,
        reviewed_by: updated.reviewed_by,
        reviewed_at: updated.reviewed_at
      }
    });

  } catch (error) {
    console.error('Admin update error:', error);
    res.status(500).json({
      success: false,
      message: error.message || 'Failed to update status'
    });
  }
});

/**
 * GET /admin/uploads
 * Get all uploads (admin view)
 */
router.get('/uploads', requireAdmin, async (req, res) => {
  try {
    const { data: uploads, error } = await supabaseClient
      .from('qr_uploads')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) {
      throw new Error(`Failed to fetch uploads: ${error.message}`);
    }

    res.json({
      success: true,
      count: uploads?.length || 0,
      data: uploads || []
    });

  } catch (error) {
    console.error('Admin uploads error:', error);
    res.status(500).json({
      success: false,
      message: error.message || 'Failed to fetch uploads'
    });
  }
});

export default router;
