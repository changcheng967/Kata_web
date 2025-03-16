// Add any interactive functionality here if needed
// Example: Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});

// Dataset: Supporters and Hall of Fame
const supportersData = {
  tiers: [
    {
      name: "Go Enthusiast",
      supporters: ["Jerjar"],
    },
    {
      name: "Strategic Supporter",
      supporters: [],
    },
    {
      name: "AI Explorer",
      supporters: [],
    },
    {
      name: "Go Champion",
      supporters: [],
    },
    {
      name: "Ultimate Patron",
      supporters: [],
    },
    {
      name: "Lifetime Legend",
      supporters: [],
    },
    {
      name: "Corporate Sponsor",
      supporters: [],
    }
  ],
  hallOfFame: [
    {
      name: "Jerjar",
      tier: "Go Enthusiast",
    },
  ],
};

// Function to display supporters
function displaySupporters() {
  const supportersList = document.getElementById("supporters-list");
  supportersData.tiers.forEach((tier) => {
    const tierDiv = document.createElement("div");
    tierDiv.classList.add("supporter-card");
    tierDiv.innerHTML = `
      <h3>${tier.name}</h3>
      <p><strong>Supporters:</strong> ${tier.supporters.length > 0 ? tier.supporters.join(", ") : "No supporters yet"}</p>
    `;
    supportersList.appendChild(tierDiv);
  });
}

// Function to display Hall of Fame
function displayHallOfFame() {
  const hallOfFameList = document.getElementById("hall-of-fame-list");
  supportersData.hallOfFame.forEach((supporter) => {
    const cardDiv = document.createElement("div");
    cardDiv.classList.add("hall-of-fame-card");
    cardDiv.innerHTML = `
      <h3>${supporter.name}</h3>
      <p>${supporter.tier}</p>
    `;
    hallOfFameList.appendChild(cardDiv);
  });
}

// Call the functions
displaySupporters();
displayHallOfFame();
