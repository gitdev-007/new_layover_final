import supabaseClient from '../supabaseClient.js';

/**
 * Partner unlock middleware
 * Allows access ONLY IF:
 * - is_valid = true
 * - user_confirmed = true
 * - is_fraud = false
 * 
 * Otherwise blocks access with 403 Forbidden
 */
export async function requirePartnerUnlock(req, res, next) {
  try {
    const { uploadId } = req.params;

    if (!uploadId) {
      return res.status(400).json({
        success: false,
        message: 'Upload ID required'
      });
    }

    // Fetch the upload record
    const { data: upload, error } = await supabaseClient
      .from('qr_uploads')
      .select('is_valid, user_confirmed, is_fraud, status')
      .eq('id', uploadId)
      .single();

    if (error || !upload) {
      return res.status(404).json({
        success: false,
        message: 'QR upload not found'
      });
    }

    // Check all unlock conditions
    const checks = {
      isValid: upload.is_valid === true,
      isConfirmed: upload.user_confirmed === true,
      isNotFraud: upload.is_fraud !== true
    };

    // If all conditions pass, allow access
    if (checks.isValid && checks.isConfirmed && checks.isNotFraud) {
      // Attach upload data to request for later use
      req.upload = upload;
      return next();
    }

    // Build specific error message based on which check failed
    let reason = '';
    if (!checks.isValid) {
      reason = 'QR code is not valid';
    } else if (!checks.isConfirmed) {
      reason = 'QR code not confirmed by user';
    } else if (!checks.isNotFraud) {
      reason = 'QR code flagged as fraudulent';
    }

    // Block access
    return res.status(403).json({
      success: false,
      message: 'Access denied - partner unlock failed',
      reason: reason,
      checks: {
        isValid: checks.isValid,
        isConfirmed: checks.isConfirmed,
        isNotFraud: checks.isNotFraud
      }
    });

  } catch (error) {
    console.error('Partner unlock check error:', error);
    return res.status(500).json({
      success: false,
      message: 'Failed to verify partner unlock status'
    });
  }
}

/**
 * Simple check function (for use in services, not middleware)
 * Returns boolean without sending response
 */
export async function checkPartnerUnlock(uploadId) {
  try {
    const { data: upload, error } = await supabaseClient
      .from('qr_uploads')
      .select('is_valid, user_confirmed, is_fraud')
      .eq('id', uploadId)
      .single();

    if (error || !upload) {
      return { unlocked: false, reason: 'Upload not found' };
    }

    const isValid = upload.is_valid === true;
    const isConfirmed = upload.user_confirmed === true;
    const isNotFraud = upload.is_fraud !== true;

    if (isValid && isConfirmed && isNotFraud) {
      return { unlocked: true, reason: null };
    }

    // Determine why it failed
    if (!isValid) {
      return { unlocked: false, reason: 'QR code is not valid' };
    } else if (!isConfirmed) {
      return { unlocked: false, reason: 'QR code not confirmed by user' };
    } else {
      return { unlocked: false, reason: 'QR code flagged as fraudulent' };
    }

  } catch (error) {
    console.error('Partner unlock check error:', error);
    return { unlocked: false, reason: 'Verification failed' };
  }
}

export default { requirePartnerUnlock, checkPartnerUnlock };
