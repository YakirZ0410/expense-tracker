const form = document.getElementById("expense-form");
const statusEl = document.getElementById("status");

form.addEventListener("submit", async (event) => {
  event.preventDefault(); // מונע מהדפדפן לעשות "רענון" רגיל של הטופס

  // קורא את הערכים מהשדות בטופס
  const formData = new FormData(form);

  const payload = {
    date: formData.get("date"),
    amount: Number(formData.get("amount")),
    category: formData.get("category"),
    description: formData.get("description"),
  };

  statusEl.textContent = "Saving...";

  try {
    // שולח POST ל-API שלך
    const res = await fetch("/expenses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(errText);
    }

    statusEl.textContent = "Saved ✅";
    statusEl.style.color = "#22c55e"; // ירוק
    form.reset();

    setTimeout(() => {
      statusEl.textContent = "";
    }, 3000);
  } catch (err) {
    statusEl.textContent = "Failed to save expense ❌";
    statusEl.style.color = "#ef4444"; // אדום
  }
});
