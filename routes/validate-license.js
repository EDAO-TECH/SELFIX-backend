const express = require('express');
const fs = require('fs');
const path = require('path');
const router = express.Router();

router.post('/', (req, res) => {
  const { email, licenseKey } = req.body;

  if (!email || !licenseKey) {
    return res.status(400).json({ valid: false, reason: "Missing email or license key" });
  }

  const safeEmail = email.toLowerCase().replace(/[@.]/g, '_');
  const filePath = path.join(__dirname, '../licenses', `${safeEmail}.json`);

  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ valid: false, reason: "License not found" });
  }

  try {
    const license = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

    if (license.licenseKey !== licenseKey) {
      return res.status(403).json({ valid: false, reason: "Invalid license key" });
    }

    res.json({ valid: true, plan: license.plan });
  } catch (err) {
    console.error(err);
    res.status(500).json({ valid: false, reason: "Error reading license file" });
  }
});

module.exports = router;
