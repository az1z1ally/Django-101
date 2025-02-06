document.addEventListener('DOMContentLoaded', function() {
  //===== MENU DROPDOWN

  const summaries = document.querySelectorAll('.menuSummary');

  // Add event listener to close all details when clicking outside
  document.addEventListener('click', function(event) {
    summaries.forEach(summary => {
      if (!summary.parentNode.contains(event.target)) {
        summary.parentNode.removeAttribute('open');
      }
    });
  });

  // Add event listeners for focus and blur for each summary
  summaries.forEach(summary => {
    const details = summary.parentNode;

    // Add focus and blur events to handle closing the details
    summary.addEventListener('focus', function() {
      details.setAttribute('data-focus', 'true');  // Custom attribute to track focus
    });

    summary.addEventListener('blur', function(event) {
      // Delay to allow for checking if focus moved within the details
      setTimeout(() => {
        if (!details.contains(document.activeElement)) {
          details.removeAttribute('open');
        }
        details.removeAttribute('data-focus');  // Remove custom attribute
      }, 1);
    });

    // Ensure the summary element can receive focus
    summary.setAttribute('tabindex', '0');
  });


  //===== PAGINATION SECTION
  //GET SEARCH FORM AND PAGE LINKS
  let searchForm = document.querySelector('#searchForm')
  let pageLinks = document.querySelectorAll('.page-link')

  //ENSURE SEARCH FORM EXISTS
  if (searchForm) {
    for (let i = 0; pageLinks.length > i; i++) {
      pageLinks[i].addEventListener('click', (e) => {
        e.preventDefault()

        //GET THE DATA ATTRIBUTE FOR THE PAGE NUMBER
        let page = e.currentTarget.dataset.page

        //ADD HIDDEN SEARCH INPUT TO FORM WITH THE PAGE NUMBER
        searchForm.innerHTML += `<input value=${page} name="page" hidden/>`

        //SUBMIT FORM
        searchForm.submit()
      })
    }
  }


  //===== CUSTOM TAGS
  let tags = document.querySelectorAll('.project-tag')

  for (let i = 0; tags.length > i; i++) {
    tags[i].addEventListener('click', (e) => {
      let tagId = e.target.dataset.tag
      let projectId = e.target.dataset.project

      fetch('http://127.0.0.1:8000/api/remove-tag/', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'project': projectId, 'tag': tagId })
      })
      .then(response => response.json())
      .then(data => {
        e.target.remove()
      })
    })
  }

});
