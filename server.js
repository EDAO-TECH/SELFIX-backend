// Load .env before using any environment variables
const dotenv = require('dotenv');
dotenv.config();

// Initialize Stripe with your secret key
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// Load Express
const express = require('express');
const app = express();

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Basic test route
app.get('/', (req, res) => {
  res.send('SELFIX backend is live ✅');
});

// Stripe Checkout Session Route
app.post('/create-checkout-session', async (req, res) => {
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      line_items: [
        {
          price: 'price_1RZa6uBekafS21xD3CPhtl9I', // Your real Stripe Price ID
          quantity: 1,
        },
      ],
      success_url: 'https://www.selfix.pro/success.html',
      cancel_url: 'https://www.selfix.pro/cancel.html',
    });

    res.status(200).json({ id: session.id });
  } catch (err) {
    console.error('Stripe error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`SELFIX backend running at http://localhost:${PORT}`);
});
