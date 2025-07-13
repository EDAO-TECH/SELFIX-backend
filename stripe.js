// stripe.js
document.addEventListener("DOMContentLoaded", async () => {
  const stripe = Stripe("pk_live_YOUR_PUBLIC_KEY_HERE"); // Replace with your real key

  const checkoutButton = document.getElementById("checkout-button");

  checkoutButton.addEventListener("click", async () => {
    const { error } = await stripe.redirectToCheckout({
      lineItems: [{ price: "price_12345", quantity: 1 }], // Replace with your Stripe price ID
      mode: "payment",
      successUrl: window.location.origin + "/success.html",
      cancelUrl: window.location.origin + "/cancel.html",
    });

    if (error) {
      alert("Error: " + error.message);
    }
  });
});
