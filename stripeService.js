// stripeService.js or inside your plan selector component

import { loadStripe } from '@stripe/stripe-js';

const STRIPE_PUBLIC_KEY = 'pk_test_XXXX'; // Replace with your real one
const stripePromise = loadStripe(STRIPE_PUBLIC_KEY);

export const redirectToCheckout = async (priceId) => {
  const stripe = await stripePromise;

  const response = await fetch('/api/create-checkout-session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ priceId })
  });

  const session = await response.json();

  const result = await stripe.redirectToCheckout({
    sessionId: session.id,
  });

  if (result.error) {
    console.error(result.error.message);
  }
};
