const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  host: "smtp.zoho.com", // or Gmail, your SMTP service
  port: 465,
  secure: true,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS
  }
});

async function sendLicense(email, licenseKey) {
  await transporter.sendMail({
    from: '"SELFIX" <support@yourdomain.com>',
    to: email,
    subject: "🎫 Your SELFIX License Key",
    text: `Thank you for purchasing SELFIX!\n\nHere is your license key:\n\n${licenseKey}\n\nKeep it safe.`,
  });

  console.log(`📧 License emailed to ${email}`);
}

module.exports = { sendLicense };
