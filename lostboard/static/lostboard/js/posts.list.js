const show_delete_post_modal = (event) => {
  comment_node = event.target.parentNode.parentNode;
  const classname = ".modal.posts-delete"
  const modal = comment_node.querySelector(classname);
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
