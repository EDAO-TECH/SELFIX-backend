require('dotenv').config();
const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const app = express();

app.use(express.json());

app.post('/create-checkout-session', async (req, res) => {
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [{
        price_data: {
          currency: 'usd',
          product_data: { name: 'Selfix Premium Access' },
          unit_amount: 1999, // $19.99
        },
        quantity: 1,
      }],
      mode: 'payment',
      success_url: 'https://selfix.pro/success',
      cancel_url: 'https://selfix.pro/cancel',
    });
    res.json({ id: session.id });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(4242, () => console.log('✅ Stripe server running on http://localhost:4242'));
