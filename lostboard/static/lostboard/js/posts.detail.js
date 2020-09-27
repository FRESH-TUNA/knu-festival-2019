const show_delete_post_modal = (event) => {
  const classname = ".modal.posts-delete"
  const modal = document.querySelector(classname);
  const span = modal.querySelector(`span`);
  
  modal.style.display = "block";

  span.onclick = function () {
    modal.style.display = "none";
  }
  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
  event.stopPropagation()
}
