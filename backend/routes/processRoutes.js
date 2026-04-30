import { Router } from 'express';
import supabaseClient from '../supabaseClient.js';

const router = Router();

// GET /qr-status/:id - Poll for processing status
router.get('/qr-status/:id', async (req, res) => {
  try {
    const { id } = req.params;

    // Fetch upload with current status
    const { data: upload, error: fetchError } = await supabaseClient
      .from('qr_uploads')
      .select('*')
      .eq('id', id)
      .single();

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
    console.error('QR status error:', error);
    res.status(500).json({
      success: false,
      message: error.message || 'Failed to check processing status'
    });
  }
});

// GET /process-qr/:id - Check processing status (background job does the actual work)
router.get('/process-qr/:id', async (req, res) => {
  try {
    const { id } = req.params;

    // Fetch upload with current status
    const { data: upload, error: fetchError } = await supabaseClient
      .from('qr_uploads')
      .select('*')
      .eq('id', id)
      .single();

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
