
    // Sample data for autocomplete
    const skillAutocompleteData = [
      "HTML",
      "CSS",
      "JavaScript",
      "Python",
      "Java",
      "React",
      "Node.js",
      "Angular",
      "Vue.js"
    ];

    // Sample job data for autocomplete
    const jobAutocompleteData = [
      "Web Developer",
      "Software Engineer",
      "Data Scientist",
      "UX/UI Designer",
      // Add more job entries as needed
    ];

    const skillAutocompleteInput = document.getElementById("skill-autocomplete-input");
    const skillAutocompleteDropdown = document.getElementById("skill-autocomplete-dropdown");
    const skillTagsContainer = document.getElementById("skill-tags-container");

    const jobAutocompleteInput = document.getElementById("job-autocomplete-input");
    const jobAutocompleteDropdown = document.getElementById("job-autocomplete-dropdown");
    const jobTagsContainer = document.getElementById("job-tags-container");

    let numberOfSkillTags = 0;
    let numberOfJobTags = 0;
    const maxTags = 5;

    // Event listener for skill input changes
    skillAutocompleteInput.addEventListener("input", function() {
      const inputText = skillAutocompleteInput.value.toLowerCase();
      const filteredSkills = skillAutocompleteData.filter(item => item.toLowerCase().includes(inputText));

      // Display the filtered skills in the dropdown
      displaySkillAutocompleteResults(filteredSkills);
    });

    // Event listener for job input changes
    jobAutocompleteInput.addEventListener("input", function() {
      const inputText = jobAutocompleteInput.value.toLowerCase();
      const filteredJobs = jobAutocompleteData.filter(item => item.toLowerCase().includes(inputText));

      // Display the filtered jobs in the dropdown
      displayJobAutocompleteResults(filteredJobs);
    });

    // Event listener for clicking on a skill dropdown item
    skillAutocompleteDropdown.addEventListener("click", function(event) {
      if (event.target.classList.contains("autocomplete-item")) {
        const selectedValue = event.target.innerText;
        if (numberOfSkillTags < maxTags && !isSkillTagExists(selectedValue)) {
          addSkillTag(selectedValue);
          skillAutocompleteInput.value = "";
          skillAutocompleteDropdown.innerHTML = "";
        }
      }
    });

    // Event listener for clicking on a job dropdown item
    jobAutocompleteDropdown.addEventListener("click", function(event) {
      if (event.target.classList.contains("autocomplete-item")) {
        const selectedValue = event.target.innerText;
        if (numberOfJobTags < maxTags && !isJobTagExists(selectedValue)) {
          addJobTag(selectedValue);
          jobAutocompleteInput.value = "";
          jobAutocompleteDropdown.innerHTML = "";
        }
      }
    });

    // Event listener to hide skill dropdown when clicking outside
    document.addEventListener("click", function(event) {
      if (!event.target.closest("#skill-autocomplete-container")) {
        skillAutocompleteDropdown.style.display = "none";
      }
    });

    // Event listener to hide job dropdown when clicking outside
    document.addEventListener("click", function(event) {
      if (!event.target.closest("#job-autocomplete-container")) {
        jobAutocompleteDropdown.style.display = "none";
      }
    });

    // Display skill autocomplete results in the dropdown
    function displaySkillAutocompleteResults(results) {
      const dropdownContent = results.map(result => `<div class="autocomplete-item">${result}</div>`).join("");
      skillAutocompleteDropdown.innerHTML = dropdownContent;
      skillAutocompleteDropdown.style.display = results.length > 0 ? "block" : "none";
    }

    // Display job autocomplete results in the dropdown
    function displayJobAutocompleteResults(results) {
      const dropdownContent = results.map(result => `<div class="autocomplete-item">${result}</div>`).join("");
      jobAutocompleteDropdown.innerHTML = dropdownContent;
      jobAutocompleteDropdown.style.display = results.length > 0 ? "block" : "none";
    }

    // Add a skill tag to the skill tags container and save it to the Profile model
    function addSkillTag(skillValue) {
      const tagElement = document.createElement("div");
      tagElement.classList.add("tag");
      tagElement.textContent = skillValue;
      tagElement.addEventListener("click", function() {
        // Remove the skill tag when clicked
        skillTagsContainer.removeChild(tagElement);
        numberOfSkillTags--;

        // Save the skill to the Profile model
        saveSkillTag(skillValue);
      });
      skillTagsContainer.appendChild(tagElement);
      numberOfSkillTags++;
    }

// Add a job tag to the job tags container and save it to the Profile model
function addJobTag(jobValue) {
  const tagElement = document.createElement("div");
  tagElement.classList.add("tag");
  tagElement.textContent = jobValue;
  tagElement.addEventListener("click", function() {
    // Remove the job tag when clicked
    jobTagsContainer.removeChild(tagElement);
    numberOfJobTags--;

    // Save the job to the Profile model (you need to implement a similar function for jobs)
    saveJobTag(jobValue);
  });
  jobTagsContainer.appendChild(tagElement);
  numberOfJobTags++;
}

// Function to save a skill tag to the Profile model
function saveSkillTag(skillValue) {
  // You need to send an AJAX request to your Django server to save the skill to the Profile model
  // Here's an example using fetch:
  const csrfToken = getCSRFToken();  // Implement a function to get CSRF token
  const url = '/edit/';  // Update the URL to your Django endpoint

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({ skill: skillValue }),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('Skill tag saved successfully:', data);
  })
  .catch(error => {
    console.error('Error saving skill tag:', error);
  });
}

// Function to save a job tag to the Profile model
function saveJobTag(jobValue) {
  const csrfToken = getCSRFToken();  // Implement a function to get CSRF token
  const url = '/edit/';  // Update the URL to your Django endpoint

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({ job: jobValue }),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('Job tag saved successfully:', data);
  })
  .catch(error => {
    console.error('Error saving job tag:', error);
  });
}
    
    // Check if a skill tag already exists
    function isSkillTagExists(tagValue) {
      return Array.from(skillTagsContainer.children).some(tag => tag.textContent === tagValue);
    }

    // Check if a job tag already exists
    function isJobTagExists(tagValue) {
      return Array.from(jobTagsContainer.children).some(tag => tag.textContent === tagValue);
    }