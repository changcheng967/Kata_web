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
      supporters: ["Jerjar"],
      perks: [
        "Early Access: Get early access to new features or updates on Kata_web.",
        "Name in Credits: Your name listed on the 'Supporters' page of Kata_web.",
        "Exclusive Updates: Monthly updates on how your support is helping the project."
      ]
    },
    {
      name: "Strategic Supporter",
      price: "CA$5 / month",
      supporters: [],
      perks: [
        "All perks from the Go Enthusiast tier.",
        "Custom Go Puzzles: Access to exclusive Go puzzles and challenges created by Kata_web.",
        "Priority Support: Faster response time for any questions or issues."
      ]
    },
    {
      name: "AI Explorer",
      price: "CA$10 / month",
      supporters: [],
      perks: [
        "All perks from the Strategic Supporter tier.",
        "Behind-the-Scenes Access: Monthly insights into how KataGo is integrated into Kata_web.",
        "Exclusive Tutorials: Access to advanced Go strategy tutorials powered by KataGo."
      ]
    },
    {
      name: "Go Champion",
      price: "CA$15 / month",
      supporters: [],
      perks: [
        "All perks from the AI Explorer tier.",
        "Personalized Shoutout: A personalized thank-you message on the Kata_web homepage or social media.",
        "Vote on Features: Influence the future development of Kata_web by voting on new features or improvements."
      ]
    },
    {
      name: "Ultimate Patron",
      price: "CA$25 / month",
      supporters: [],
      perks: [
        "All perks from the Go Champion tier.",
        "1-on-1 Go Session: A monthly 30-minute online Go session with the Kata_web team or a Go expert.",
        "Exclusive Merch: A digital thank-you card or exclusive Kata_web wallpaper for your devices."
      ]
    },
    {
      name: "Lifetime Legend",
      price: "CA$50 / month",
      supporters: [],
      perks: [
        "All perks from the Ultimate Patron tier.",
        "Permanent Recognition: Your name permanently featured on the Kata_web 'Hall of Fame' page.",
        "Custom Go Analysis: A personalized Go game analysis using KataGo (once per month)."
      ]
    },
    {
      name: "Corporate Sponsor",
      price: "CA$100 / month",
      supporters: [],
      perks: [
        "All perks from the Lifetime Legend tier.",
        "Logo Placement: Your logo featured on the Kata_web homepage and social media.",
        "Custom Partnership: Opportunity to collaborate on a custom project or feature."
      ]
    }
  ],
  hallOfFame: [
    {
      name: "Jerjar",
      contribution: "Go Enthusiast",
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
      <p><strong>${tier.price}</strong></p>
      <p><strong>Supporters:</strong> ${tier.supporters.length > 0 ? tier.supporters.join(", ") : "No supporters yet"}</p>
      <ul>
        ${tier.perks.map(perk => `<li>${perk}</li>`).join("")}
      </ul>
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
      <p><strong>Contribution:</strong> ${supporter.contribution}</p>
    `;
    hallOfFameList.appendChild(cardDiv);
  });
}

// Call the functions
displaySupporters();
displayHallOfFame();
