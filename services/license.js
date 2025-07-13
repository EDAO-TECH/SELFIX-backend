const fs = require('fs');
const path = require('path');

function createLicense(email, plan) {
  const licensesDir = path.join(__dirname, '../licenses');
  if (!fs.existsSync(licensesDir)) {
    fs.mkdirSync(licensesDir);
  }

  const licenseKey = `LICENSE-${Date.now()}-${Math.random().toString(36).substr(2, 8).toUpperCase()}`;
  const licenseData = {
    email,
    plan,
    licenseKey,
    createdAt: new Date().toISOString()
  };

  const fileName = email.replace(/[@.]/g, '_') + '.json';
  const filePath = path.join(licensesDir, fileName);
  fs.writeFileSync(filePath, JSON.stringify(licenseData, null, 2));

  console.log(`🎉 License created for ${email}: ${licenseKey}`);
  return licenseKey;
}

module.exports = { createLicense };
