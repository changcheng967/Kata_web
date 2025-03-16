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
      price: "CA$3 / month",
      supporters: [],
    },
    {
      name: "Strategic Supporter",
      price: "CA$5 / month",
      supporters: [],
    },
    {
      name: "AI Explorer",
      price: "CA$10 / month",
      supporters: [],
    },
    {
      name: "Go Champion",
      price: "CA$15 / month",
      supporters: [],
    },
    {
      name: "Ultimate Patron",
      price: "CA$25 / month",
      supporters: [
        {
          name: "Cheng",
          email: "440003227@gapps.yrdsb.ca",
          joinDate: "2023-10-01",
          totalSupported: "CA$25",
        },
      ],
    },
    {
      name: "Lifetime Legend",
      price: "CA$50 / month",
      supporters: [],
    },
    {
      name: "Corporate Sponsor",
      price: "CA$100 / month",
      supporters: [],
    }
  ],
  hallOfFame: [
    {
      name: "Cheng",
      tier: "Ultimate Patron",
      joinDate: "2023-10-01",
      totalSupported: "CA$25",
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
      <p><strong>Price:</strong> ${tier.price}</p>
      <p><strong>Supporters:</strong> ${tier.supporters.length > 0 ? tier.supporters.map(supporter => `
        <div class="supporter-details">
          <p><strong>Name:</strong> ${supporter.name}</p>
          <p><strong>Join Date:</strong> ${supporter.joinDate}</p>
          <p><strong>Total Supported:</strong> ${supporter.totalSupported}</p>
        </div>
      `).join("") : "No supporters yet"}
      </p>
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
      <p><strong>Tier:</strong> ${supporter.tier}</p>
      <p><strong>Join Date:</strong> ${supporter.joinDate}</p>
      <p><strong>Total Supported:</strong> ${supporter.totalSupported}</p>
    `;
    hallOfFameList.appendChild(cardDiv);
  });
}

// Call the functions
displaySupporters();
displayHallOfFame();
