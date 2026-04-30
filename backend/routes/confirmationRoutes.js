import { Router } from 'express';
import supabaseClient from '../supabaseClient.js';

const router = Router();

// POST /confirm-qr/:id - Confirm QR by user
router.post('/confirm-qr/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { user_confirmed } = req.body;

    // Validate input
    if (typeof user_confirmed !== 'boolean') {
      return res.status(400).json({
        error: 'user_confirmed must be a boolean value'
      });
    }

    // Update qr_uploads table
    const { data, error } = await supabaseClient
      .from('qr_uploads')
      .update({
        user_confirmed: user_confirmed,
        confirmed_at: user_confirmed ? new Date().toISOString() : null
      })
      .eq('id', id)
      .select()
      .single();

    if (error) {
      throw new Error(`Database update failed: ${error.message}`);
    }

    if (!data) {
      return res.status(404).json({ error: 'QR upload not found' });
    }

    // Return success response
    res.json({
      success: true,
      message: user_confirmed ? 'QR confirmed successfully' : 'QR confirmation revoked',
      data: {
        id: data.id,
        user_confirmed: data.user_confirmed,
        confirmed_at: data.confirmed_at
      }
    });

  } catch (error) {
    console.error('Confirm QR error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to confirm QR'
    });
  }
});

export default router;
