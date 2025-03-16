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
      supporters: ["Alice", "Bob", "Charlie"],
    },
    {
      name: "Strategic Supporter",
      supporters: ["David", "Eve"],
    },
    {
      name: "AI Explorer",
      supporters: ["Frank"],
    },
    {
      name: "Go Champion",
      supporters: ["Grace"],
    },
    {
      name: "Ultimate Patron",
      supporters: ["Hank"],
    },
  ],
  hallOfFame: [
    {
      name: "John Doe",
      contribution: "Lifetime Legend",
    },
    {
      name: "Jane Smith",
      contribution: "Corporate Sponsor",
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
      <p>${tier.supporters.join(", ")}</p>
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
      <p>${supporter.contribution}</p>
    `;
    hallOfFameList.appendChild(cardDiv);
  });
}

// Call the functions
displaySupporters();
displayHallOfFame();
