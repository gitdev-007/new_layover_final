const fs = require('fs');
const html = fs.readFileSync('c:\\Users\\Dev Tinker\\Desktop\\layoverX_dummy\\hotel.html', 'utf8');
const lines = html.split(/\r?\n/);
// Find line containing hotel-item
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes('hotel-item')) {
    fs.writeFileSync('c:\\Users\\Dev Tinker\\Desktop\\layoverX_dummy\\_dump.txt', 'Line ' + (i+1) + ':\n' + lines[i]);
    break;
  }
}
console.log('dump done');
