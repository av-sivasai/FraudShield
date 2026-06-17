document.addEventListener("DOMContentLoaded", () => {
    fetchSummary();
    
    // Refresh button
    document.getElementById("refresh-btn").addEventListener("click", fetchSummary);
    
    // Export button
    document.getElementById("export-btn").addEventListener("click", () => {
        window.location.href = "/api/v1/analytics/export";
    });

    // Form submission
    document.getElementById("predict-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const amount = document.getElementById("amount").value;
        const btnText = document.querySelector(".btn-text");
        const loader = document.querySelector(".loader");
        const resultCard = document.getElementById("prediction-result");
        
        // Show loader
        btnText.textContent = "Analyzing...";
        loader.classList.remove("hidden");
        resultCard.classList.add("hidden");

        // Build mock transaction data, but use the real Amount
        const txData = { Amount: parseFloat(amount) };
        for(let i=1; i<=28; i++) txData[`V${i}`] = 0;
        txData["Time"] = 0;

        try {
            const res = await fetch("/api/v1/predict/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(txData)
            });
            const data = await res.json();
            
            showResult(data);
            fetchSummary(); // update metrics silently
        } catch (error) {
            console.error("Prediction failed", error);
            alert("Error running prediction. Check API logs.");
        } finally {
            btnText.textContent = "Run Prediction";
            loader.classList.add("hidden");
        }
    });

    // Simulate Fraud button
    document.getElementById("simulate-fraud-btn").addEventListener("click", async () => {
        const btnText = document.querySelector(".btn-text");
        const loader = document.querySelector(".loader");
        const resultCard = document.getElementById("prediction-result");
        
        // Show loader
        btnText.textContent = "Analyzing...";
        loader.classList.remove("hidden");
        resultCard.classList.add("hidden");

        // Build known fraudulent transaction data using the user's typed Amount
        const amount = document.getElementById("amount").value || 0;
        const txData = { Amount: parseFloat(amount) };
        for(let i=1; i<=28; i++) txData[`V${i}`] = 0;
        txData["Time"] = 0;
        
        // Inject a known, verified fraud pattern from the Kaggle dataset (Index 541)
        txData["V1"] = -2.312226542; txData["V2"] = 1.951992011; txData["V3"] = -1.609850732;
        txData["V4"] = 3.997905588;  txData["V5"] = -0.522187865; txData["V6"] = -1.426545319;
        txData["V7"] = -2.537387306; txData["V8"] = 1.391657248;  txData["V9"] = -2.770089277;
        txData["V10"] = -2.772272145; txData["V11"] = 3.202033207; txData["V12"] = -2.899907388;
        txData["V13"] = -0.595221881; txData["V14"] = -4.289253782; txData["V15"] = 0.38972412;
        txData["V16"] = -1.14074718;  txData["V17"] = -2.830055675; txData["V18"] = -0.016822468;
        txData["V19"] = 0.416955705;  txData["V20"] = 0.126910559;  txData["V21"] = 0.517232371;
        txData["V22"] = -0.035049369; txData["V23"] = -0.465211076; txData["V24"] = 0.320198199;
        txData["V25"] = 0.044519167;  txData["V26"] = 0.177839798;  txData["V27"] = 0.261145003;
        txData["V28"] = -0.143275875;

        try {
            const res = await fetch("/api/v1/predict/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(txData)
            });
            const data = await res.json();
            
            showResult(data);
            fetchSummary(); // update metrics silently
        } catch (error) {
            console.error("Prediction failed", error);
            alert("Error running prediction. Check API logs.");
        } finally {
            btnText.textContent = "Run Prediction";
            loader.classList.add("hidden");
        }
    });
});

async function fetchSummary() {
    try {
        const res = await fetch("/api/v1/analytics/summary");
        const data = await res.json();
        
        // Animate numbers
        document.getElementById("total-predictions").textContent = data.total_predictions.toLocaleString();
        document.getElementById("total-frauds").textContent = data.total_frauds.toLocaleString();
        document.getElementById("fraud-rate").textContent = `${data.fraud_rate}%`;
        
        updateTable(data.recent_activity);
    } catch (e) {
        console.error("Failed to fetch analytics", e);
    }
}

function updateTable(history) {
    const tbody = document.getElementById("history-body");
    tbody.innerHTML = "";
    
    history.forEach(tx => {
        const tr = document.createElement("tr");
        const date = new Date(tx.timestamp).toLocaleString();
        const badgeClass = tx.prediction === 1 ? "fraud" : "safe";
        const badgeText = tx.prediction === 1 ? "FRAUD" : "SAFE";
        
        tr.innerHTML = `
            <td>#${tx.id}</td>
            <td>${date}</td>
            <td>$${tx.amount.toFixed(2)}</td>
            <td>${(tx.probability * 100).toFixed(1)}%</td>
            <td><span class="badge ${badgeClass}">${badgeText}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function showResult(data) {
    const card = document.getElementById("prediction-result");
    const title = document.getElementById("result-title");
    const prob = document.getElementById("res-prob");
    const conf = document.getElementById("res-conf");
    const expBox = document.getElementById("res-explanation");
    
    card.classList.remove("hidden");
    
    if (data.fraud_prediction === 1) {
        title.textContent = "🚨 FRAUD DETECTED";
        title.className = "text-danger";
    } else {
        title.textContent = "✅ LEGITIMATE TRANSACTION";
        title.className = "text-success";
    }
    
    prob.textContent = `${(data.probability * 100).toFixed(2)}%`;
    conf.textContent = data.confidence_score;
    
    if (data.explanation && Object.keys(data.explanation).length > 0) {
        let html = `<strong>AI Insight:</strong> Top contributing features:<br><ul>`;
        for (const [feat, val] of Object.entries(data.explanation)) {
            html += `<li>${feat} (Weight: ${val.toFixed(4)})</li>`;
        }
        html += `</ul>`;
        expBox.innerHTML = html;
        expBox.style.display = "block";
    } else {
        expBox.style.display = "none";
    }
}
