import { Router } from 'express';
import supabaseClient from '../supabaseClient.js';

const router = Router();

let progressStore = {}; // simple memory store

// GET /qr-status - Poll for processing status (supports id or url query param)
router.get('/qr-status', async (req, res) => {
  try {
    const { id, url } = req.query;
    const key = url || id || "default";

    if (!progressStore[key]) {
      progressStore[key] = 0;
    }

    // increment slowly
    progressStore[key] += Math.floor(Math.random() * 10) + 5;

    if (progressStore[key] >= 100) {
      progressStore[key] = 100;

      return res.json({
        status: "completed",
        progress: 100,
        extractedInfo: {
          name: "M TINKER",
          flight: "AI-202",
          date: "2026-05-04",
          seat: "14A",
          gate: "5"
        }
      });
    }

    return res.json({
      status: "processing",
      progress: progressStore[key]
    });

  } catch (err) {
    console.error(err);
    res.json({
      status: "processing",
      progress: 0
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
