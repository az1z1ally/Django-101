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