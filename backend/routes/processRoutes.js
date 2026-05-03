import { Router } from 'express';
import supabaseClient from '../supabaseClient.js';

const router = Router();

// GET /qr-status - Poll for processing status (supports id or url query param)
router.get('/qr-status', async (req, res) => {
  try {
    const { id, url } = req.query;

    console.log("Received QR ID:", id);

    if (!id && !url) {
      return res.status(400).json({
        success: false,
        message: 'id or url required'
      });
    }

    // Try DB lookup
    let query = supabaseClient
      .from('qr_uploads')
      .select('*');

    if (id) {
      query = query.eq('id', id);
    } else if (url) {
      query = query.ilike('file_url', `%${decodeURIComponent(url)}%`);
    }

    const { data, error } = await query.single();

    if (error || !data) {
      // DB record not found — return processing status instead of error
      console.log("QR upload not found in DB, returning processing status for ID:", id);
      return res.json({
        success: true,
        status: "processing",
        progress: 0,
        id
      });
    }

    res.json({
      success: true,
      qrData: data.qr_data,
      isValid: data.is_valid,
      isDuplicate: data.is_duplicate,
      isFraud: data.is_fraud,
      fraudScore: data.fraud_score,
      status: data.status,
      progress: data.progress || 0,
      extractedInfo: data.extracted_info,
      airline: data.airline,
      id: data.id
    });

  } catch (err) {
    console.error(err);
    res.json({
      success: true,
      status: "processing",
      progress: 0,
      id: req.query.id
    });
  }
});
// GET /process-qr - Check processing status (supports id or url query param)
router.get('/process-qr', async (req, res) => {
  try {
    const { id, url } = req.query;

    // Validate that at least one param is provided
    if (!id && !url) {
      return res.status(400).json({
        success: false,
        message: 'id or url required'
      });
    }

    // Build query based on provided param
    let query = supabaseClient.from('qr_uploads').select('*');
    if (id) {
      query = query.eq('id', id);
    } else if (url) {
      query = query.eq('file_url', url);
    }

    const { data: upload, error: fetchError } = await query.single();

    if (fetchError || !upload) {
      return res.status(404).json({ 
        success: false, 
        message: 'QR upload not found' 
      });
    }

    // Return current status (background job updates this)
    res.json({
      success: true,
      qrData: upload.qr_data,
      isValid: upload.is_valid,
      isDuplicate: upload.is_duplicate,
      status: upload.status,
      extractedInfo: upload.extracted_info,
      airline: upload.airline
    });

  } catch (error) {
    console.error('Process QR error:', error);
    res.status(500).json({
      success: false,
      message: error.message || 'Failed to check processing status'
    });
  }
});

export default router;
