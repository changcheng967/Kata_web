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
      supporters: [
        {
          name: "Doulet Media",
          email: "xe59k0i3h1@wyoxafp.com",
          joinDate: "2025-03-19",
          totalSupported: "CA$100",
        },
      ],
    },
  ],
  hallOfFame: [
    {
      name: "Cheng",
      tier: "Ultimate Patron",
      joinDate: "2023-10-01",
      totalSupported: "CA$25",
    },
    {
      name: "Doulet Media",
      tier: "Corporate Sponsor",
      joinDate: "2025-03-19",
      totalSupported: "CA$100",
    },
  ],
};

// Function to display supporters
function displaySupporters() {
  const supportersList = document.getElementById("supporters-list");
  if (!supportersList) return; // Exit if the element doesn't exist

  supportersData.tiers.forEach((tier) => {
    const tierDiv = document.createElement("div");
    tierDiv.classList.add("supporter-card");

    // Create supporter details HTML
    const supportersHTML = tier.supporters.length > 0
      ? tier.supporters
          .map(
            (supporter) => `
          <div class="supporter-details">
            <p><strong>Name:</strong> ${supporter.name}</p>
            <p><strong>Email:</strong> ${supporter.email}</p>
            <p><strong>Join Date:</strong> ${supporter.joinDate}</p>
            <p><strong>Total Supported:</strong> ${supporter.totalSupported}</p>
          </div>
        `
          )
          .join("")
      : "<p>No supporters yet</p>";

    // Populate tier card
    tierDiv.innerHTML = `
      <h3>${tier.name}</h3>
      <p><strong>Price:</strong> ${tier.price}</p>
      <p><strong>Supporters:</strong></p>
      ${supportersHTML}
    `;
    supportersList.appendChild(tierDiv);
  });
}

// Function to display Hall of Fame
function displayHallOfFame() {
  const hallOfFameList = document.getElementById("hall-of-fame-list");
  if (!hallOfFameList) return; // Exit if the element doesn't exist

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

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth",
    });
  });
});

// Call the functions to display data
displaySupporters();
displayHallOfFame();
