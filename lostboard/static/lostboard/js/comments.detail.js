const show_delete_comment_modal = (event, url) => {
  const classname = ".modal.comments-delete"
  const modal = document.querySelector(classname);
  const span = modal.querySelector('span');
  const form = modal.querySelector('form');

  form.setAttribute("action", url.substring(0, url.length - 5));
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
