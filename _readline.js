const fs = require('fs');
const lines = fs.readFileSync('c:\\Users\\Dev Tinker\\Desktop\\layoverX_dummy\\hotel.html', 'utf8').split('\n');
console.log(lines[199]);
