import supabaseClient from '../supabaseClient.js';

/**
 * Detects potential fraud in QR data
 * @param {string} qrData - Raw QR data string
 * @param {Object} extractedInfo - Parsed QR data { name, flight, pnr, airline }
 * @returns {Promise<{isFraud: boolean, reason: string}>}
 */
export async function detectFraud(qrData, extractedInfo) {
  // Rule 1: Missing required fields
  if (!extractedInfo.name || !extractedInfo.flight || !extractedInfo.pnr) {
    return {
      isFraud: true,
      reason: 'Missing required fields (name, flight, or PNR)'
    };
  }

  // Rule 2: Airline code mismatch
  if (extractedInfo.flight && extractedInfo.airline) {
    const flightPrefix = extractedInfo.flight.substring(0, 2).toUpperCase();
    if (flightPrefix !== extractedInfo.airline.toUpperCase()) {
      return {
        isFraud: true,
        reason: `Airline code mismatch: flight ${extractedInfo.flight} does not match airline ${extractedInfo.airline}`
      };
    }
  }

  // Rule 3: Check for duplicate PNR usage
  try {
    const { data: pnrUploads, error: pnrError } = await supabaseClient
      .from('qr_uploads')
      .select('id, created_at')
      .eq('extracted_info->>pnr', extractedInfo.pnr)
      .limit(2);

    if (pnrError) {
      console.error('PNR check error:', pnrError);
    } else if (pnrUploads && pnrUploads.length > 1) {
      return {
        isFraud: true,
        reason: `Duplicate PNR detected: ${extractedInfo.pnr} has been used ${pnrUploads.length} times`
      };
    }
  } catch (err) {
    console.error('PNR fraud check error:', err);
  }

  // Rule 4: Check for duplicate QR data (same exact QR string)
  try {
    const { data: qrUploads, error: qrError } = await supabaseClient
      .from('qr_uploads')
      .select('id')
      .eq('qr_data', qrData)
      .limit(2);

    if (qrError) {
      console.error('QR check error:', qrError);
    } else if (qrUploads && qrUploads.length > 1) {
      return {
        isFraud: true,
        reason: 'Same QR code has been uploaded multiple times'
      };
    }
  } catch (err) {
    console.error('QR fraud check error:', err);
  }

  // Rule 5: Check for rapid multiple uploads from same user (if user_id available)
  try {
    const { data: { user } } = await supabaseClient.auth.getUser();
    if (user) {
      const { data: recentUploads, error: recentError } = await supabaseClient
        .from('qr_uploads')
        .select('id, created_at')
        .eq('user_id', user.id)
        .gte('created_at', new Date(Date.now() - 5 * 60 * 1000).toISOString()) // Last 5 minutes
        .limit(5);

      if (recentError) {
        console.error('Recent uploads check error:', recentError);
      } else if (recentUploads && recentUploads.length >= 5) {
        return {
          isFraud: true,
          reason: 'Suspicious activity: Too many uploads in short time period'
        };
      }
    }
  } catch (err) {
    console.error('User activity check error:', err);
  }

  // All checks passed
  return {
    isFraud: false,
    reason: null
  };
}

export default { detectFraud };
