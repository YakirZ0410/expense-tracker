const form = document.getElementById("expense-form");
const statusEl = document.getElementById("status");

async function loadExpenses() {
  console.log("loadExpenses() called"); // לבדיקה

  const res = await fetch("/expenses");
  console.log("GET /expenses status:", res.status); // לבדיקה

  const expenses = await res.json();

  const tbody = document.querySelector("#expenses-table tbody");
  tbody.innerHTML = "";

  expenses.forEach((e) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${e.date}</td>
      <td>${Number(e.amount).toFixed(2)}</td>
      <td>${e.category}</td>
      <td>${e.description}</td>
    `;
    tbody.appendChild(tr);
  });
}

window.addEventListener("DOMContentLoaded", () => {
  loadExpenses();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);

  const payload = {
    date: formData.get("date"),
    amount: Number(formData.get("amount")),
    category: formData.get("category"),
    description: formData.get("description"),
  };

  statusEl.textContent = "Saving...";

  try {
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
    statusEl.style.color = "#22c55e";
    form.reset();

    await loadExpenses(); // מרענן טבלה אחרי שמירה

    setTimeout(() => {
      statusEl.textContent = "";
    }, 3000);
  } catch (err) {
    console.error(err);
    statusEl.textContent = "Failed to save expense ❌";
    statusEl.style.color = "#ef4444";
  }
});
