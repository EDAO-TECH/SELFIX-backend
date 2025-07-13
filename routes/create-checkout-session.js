const express = require('express');
const router = express.Router();
const Stripe = require('stripe');
require('dotenv').config();

const stripe = Stripe(process.env.STRIPE_SECRET_KEY);

// Your price IDs (from Stripe dashboard)
const prices = {
  pro: 'price_1RjXuzBekafS21xDPIGDs5kH',
  team: 'price_1RjXwMBekafS21xDxSG6dRiy'
};

router.post('/', async (req, res) => {
  const { plan } = req.body;
  const priceId = prices[plan];

  if (!priceId) {
    return res.status(400).json({ error: 'Invalid plan' });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'subscription',
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: 'https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
      cancel_url: 'https://yourdomain.com/cancel',
      metadata: { plan } // Send plan to webhook
    });

    res.json({ url: session.url });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Stripe session creation failed' });
  }
});

module.exports = router;
