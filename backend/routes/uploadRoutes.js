import { Router } from 'express';
import multer from 'multer';
import supabaseClient from '../supabaseClient.js';
import { scanQR } from '../services/qrScanner.js';
import { validateQR } from '../services/validation.js';
import { parseQRData } from '../services/parser.js';
import { detectFraud } from '../services/fraudDetection.js';
import { decodeBCBP } from '../services/bcbpDecoder.js';

const router = Router();

/**
 * Background QR processing function
 * Processes uploaded QR files asynchronously
 * @param {string} id - Upload ID
 */
async function processQRInBackground(id) {
  try {
    console.log(`[Background] Starting processing for upload ${id}`);
    
    // Fetch the upload record
    const { data: upload, error: fetchError } = await supabaseClient
      .from('qr_uploads')
      .select('*')
      .eq('id', id)
      .single();

    if (fetchError || !upload) {
      console.error(`[Background] Upload ${id} not found`);
      return;
    }

    // Update status to processing
    await supabaseClient
      .from('qr_uploads')
      .update({ status: 'processing' })
      .eq('id', id);

    // Extract file path from stored URL
    const filePath = upload.file_url.split('/').slice(-2).join('/');
    
    // Generate fresh signed URL
    const { data: signedUrlData, error: signedUrlError } = await supabaseClient
      .storage
      .from('qr-files')
      .createSignedUrl(filePath, 3600);

    if (signedUrlError) {
      throw new Error(`Failed to generate signed URL: ${signedUrlError.message}`);
    }

    // Download file
    const response = await fetch(signedUrlData.signedUrl);
    if (!response.ok) {
      throw new Error(`Failed to download file: ${response.statusText}`);
    }

    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    // Scan QR code
    const qrData = await scanQR(buffer);

    // Check for duplicate QR data
    const { data: existingUploads, error: duplicateError } = await supabaseClient
      .from('qr_uploads')
      .select('id')
      .eq('qr_data', qrData)
      .neq('id', id)
      .limit(1);

    const isDuplicate = existingUploads && existingUploads.length > 0;

    // Check if QR data matches BCBP format (starts with M or S followed by digit)
    const isBCBPFormat = /^[MS]\d/.test(qrData);
    
    // Parse QR data using appropriate parser
    let extractedInfo;
    if (isBCBPFormat) {
      console.log(`[Background] Detected BCBP format for upload ${id}`);
      extractedInfo = decodeBCBP(qrData);
    } else {
      console.log(`[Background] Using standard parser for upload ${id}`);
      extractedInfo = parseQRData(qrData);
    }
    
    const validationResult = validateQR(qrData);
    const isValid = validationResult.isValid;

    // Detect fraud
    const fraudResult = await detectFraud(qrData, extractedInfo);

    // Determine status
    let status = isValid ? 'verified' : 'failed';
    if (isDuplicate) {
      status = 'duplicate';
    }
    if (fraudResult.isFraud) {
      status = 'fraud';
    }

    // Update DB with results
    // Handle both BCBP (airlineCode) and standard parser (airline) formats
    const airlineCode = extractedInfo.airlineCode || extractedInfo.airline || null;
    
    await supabaseClient
      .from('qr_uploads')
      .update({
        qr_data: qrData,
        is_valid: isValid,
        status: status,
        is_duplicate: isDuplicate,
        is_fraud: fraudResult.isFraud,
        fraud_reason: fraudResult.reason,
        extracted_info: extractedInfo,
        airline: airlineCode
      })
      .eq('id', id);

    console.log(`[Background] Completed processing for upload ${id}. Status: ${status}, Fraud: ${fraudResult.isFraud}`);

  } catch (error) {
    console.error(`[Background] Error processing upload ${id}:`, error);
    
    // Update status to failed
    await supabaseClient
      .from('qr_uploads')
      .update({
        status: 'failed',
        qr_data: error.message
      })
      .eq('id', id);
  }
}

// Simple in-memory rate limiter (requests per IP)
const rateLimits = new Map();
const RATE_LIMIT_WINDOW = 60 * 1000; // 1 minute
const RATE_LIMIT_MAX = 10; // max 10 requests per minute

// Rate limiter middleware
function rateLimit(req, res, next) {
  const ip = req.ip || req.connection.remoteAddress || 'unknown';
  const now = Date.now();
  
  // Clean up old entries
  for (const [key, data] of rateLimits.entries()) {
    if (now - data.timestamp > RATE_LIMIT_WINDOW) {
      rateLimits.delete(key);
    }
  }
  
  // Check current IP
  const ipData = rateLimits.get(ip);
  if (ipData) {
    if (now - ipData.timestamp > RATE_LIMIT_WINDOW) {
      // Reset window
      rateLimits.set(ip, { count: 1, timestamp: now });
    } else if (ipData.count >= RATE_LIMIT_MAX) {
      // Rate limit exceeded
      return res.status(429).json({
        success: false,
        error: 'Rate limit exceeded. Maximum 10 uploads per minute allowed.'
      });
    } else {
      // Increment count
      ipData.count++;
    }
  } else {
    // First request from this IP
    rateLimits.set(ip, { count: 1, timestamp: now });
  }
  
  next();
}

// Configure multer for memory storage
const storage = multer.memoryStorage();
const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit
  fileFilter: (req, file, cb) => {
    // Only allow: image/png, image/jpeg, application/pdf
    const allowedTypes = ['image/png', 'image/jpeg', 'application/pdf'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error(`Invalid file type: ${file.mimetype}. Only PNG, JPEG, and PDF files are allowed.`), false);
    }
  }
});

// GET /my-uploads - Get user's uploads
router.get('/my-uploads', async (req, res) => {
  try {
    // Get user from JWT token
    const authHeader = req.headers.authorization;
    
    if (!authHeader) {
      return res.status(401).json({
        success: false,
        error: 'Authentication required'
      });
    }

    const token = authHeader.replace('Bearer ', '');
    const { data: { user }, error: authError } = await supabaseClient.auth.getUser(token);

    if (authError || !user) {
      return res.status(401).json({
        success: false,
        error: 'Invalid or expired token'
      });
    }

    // Fetch user's uploads
    const { data: uploads, error } = await supabaseClient
      .from('qr_uploads')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false });

    if (error) {
      throw new Error(`Failed to fetch uploads: ${error.message}`);
    }

    res.json({
      success: true,
      data: uploads || []
    });

  } catch (error) {
    console.error('Fetch uploads error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to fetch uploads'
    });
  }
});

// Multer error handler middleware
function handleMulterError(err, req, res, next) {
  if (err instanceof multer.MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({
        success: false,
        error: 'File size exceeds 5MB limit'
      });
    }
    return res.status(400).json({
      success: false,
      error: err.message
    });
  } else if (err) {
    return res.status(400).json({
      success: false,
      error: err.message
    });
  }
  next();
}

// POST /upload-qr - Upload QR file
router.post('/upload-qr', rateLimit, upload.single('file'), handleMulterError, async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // Get user from JWT token
    const authHeader = req.headers.authorization;
    let userId = null;
    
    if (authHeader) {
      const token = authHeader.replace('Bearer ', '');
      const { data: { user }, error: authError } = await supabaseClient.auth.getUser(token);
      
      if (authError) {
        console.error('Auth error:', authError.message);
      } else if (user) {
        userId = user.id;
      }
    }

    const file = req.file;
    const timestamp = Date.now();
    const fileName = `${timestamp}-${file.originalname}`;
    const filePath = `uploads/${fileName}`;

    // Upload file to Supabase Storage
    const { data: storageData, error: storageError } = await supabaseClient
      .storage
      .from('qr-files')
      .upload(filePath, file.buffer, {
        contentType: file.mimetype,
        cacheControl: '3600'
      });

    if (storageError) {
      throw new Error(`Storage upload failed: ${storageError.message}`);
    }

    // Generate signed URL (1 hour expiry) for private bucket
    const { data: signedUrlData, error: signedUrlError } = await supabaseClient
      .storage
      .from('qr-files')
      .createSignedUrl(filePath, 3600); // 3600 seconds = 1 hour

    if (signedUrlError) {
      throw new Error(`Failed to generate signed URL: ${signedUrlError.message}`);
    }

    const fileUrl = signedUrlData.signedUrl;

    // Insert record in qr_uploads table
    const insertData = {
      file_url: fileUrl,
      status: 'uploaded'
    };
    
    // Add user_id if authenticated
    if (userId) {
      insertData.user_id = userId;
    }
    
    const { data: insertResult, error: insertError } = await supabaseClient
      .from('qr_uploads')
      .insert([insertData])
      .select()
      .single();

    if (insertError) {
      throw new Error(`Database insert failed: ${insertError.message}`);
    }

    // Trigger async processing (don't await - run in background)
    processQRInBackground(insertResult.id);

    // Return immediately with upload ID
    res.status(201).json({
      success: true,
      data: insertResult
    });

  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to upload file'
    });
  }
});

// Export cleanup function for testing/development
export function cleanupRateLimits() {
  rateLimits.clear();
}

export default router;
