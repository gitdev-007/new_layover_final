/**
 * Parse QR data string into structured JSON
 * @param {string} qrData - Raw QR data string (e.g., "PNR: ABC123 | FLIGHT: AI202 | NAME: HARSHIT")
 * @returns {Object} Structured JSON with name, flight, pnr, airline
 */
export function parseQRData(qrData) {
  if (!qrData || typeof qrData !== 'string') {
    return {
      name: null,
      flight: null,
      pnr: null,
      airline: null
    };
  }

  const result = {
    name: null,
    flight: null,
    pnr: null,
    airline: null
  };

  // Split by common delimiters (|, ;, newline)
  const parts = qrData.split(/[|;\n]/).map(part => part.trim()).filter(Boolean);

  for (const part of parts) {
    // Match KEY: VALUE pattern
    const match = part.match(/^([A-Za-z]+)[\s]*:[\s]*(.+)$/i);
    if (match) {
      const key = match[1].toUpperCase().trim();
      const value = match[2].trim();

      switch (key) {
        case 'NAME':
          result.name = value;
          break;
        case 'FLIGHT':
          result.flight = value;
          // Extract airline code (first 2 letters of flight number)
          if (value && value.length >= 2) {
            result.airline = value.substring(0, 2).toUpperCase();
          }
          break;
        case 'PNR':
        case 'BOOKING':
        case 'REF':
        case 'REFERENCE':
          result.pnr = value;
          break;
        case 'AIRLINE':
          result.airline = value;
          break;
        default:
          // Ignore unknown keys
          break;
      }
    }
  }

  return result;
}

export default { parseQRData };
