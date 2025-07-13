const express = require('express');
const router = express.Router();
const Stripe = require('stripe');
const { createLicense } = require('../services/license');
require('dotenv').config();

const stripe = Stripe(process.env.STRIPE_SECRET_KEY);

router.post('/', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;

  try {
    event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    console.error('❌ Invalid webhook signature:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // 🎯 Handle completed checkout
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const email = session.customer_details.email;
    const plan = session.metadata?.plan || 'unknown';

    console.log(`✅ Payment received from ${email} for ${plan}`);
    createLicense(email, plan);
  }

  res.json({ received: true });
});

module.exports = router;
