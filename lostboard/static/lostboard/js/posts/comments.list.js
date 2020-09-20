const posts_comments_list = async (url) => {
  // functions //
  const posts_comments_list_request = async (url) => {
    return await fetch(url)
      .then(
        (response) => {
          return response
        }
      )
      .catch(() => {
        return false;
      });
  }

  const posts_comments_list_draw = (comments, parent = null, depth = 0) => {
    const draw_comment = (comments_dom, comment) => {
      const return_body_html = (comment) => {
        if(comment.active) {
          return `
            <div class="body">
              <p class="detail-comment">${comment.content}</p> \
              <div class="detail-comment-date">${comment.created_at}</div> \
              <div class="buttons">
                <button onclick="show_add_reply_modal(event, '${comment.comments}')" class="btn-addcmt"></button>
                <button onclick="show_delete_comment_modal(event, '${comment.url}')"></button>
              </div>
            </body>
          `
        }
        else {
          return `
            <div class="body">
              <p class="detail-comment">삭제된 댓글입니다</p> \
              <div class="detail-comment-date"></div> \
              <div class="buttons">
              </div>
            </body>
          `
        }
      }
       
      const return_hierarchy_html = (depth) => {
        template_html = ` \
            <div class="line">
              <i></i>
            </div>
          `
        return template_html.repeat(depth);
      }

      template = document.createElement('template');
      template.innerHTML =
        `<div class="comment"> \
            <div class="hierachy">
              ${return_hierarchy_html(depth)}
              <div class="line">
                <i></i>
              </div>
            </div>
            ${return_body_html(comment)}
          </div>`.trim();
      comments_dom.appendChild(template.content.firstChild)
    }

    const comments_dom = document.querySelector('.board-detail-comments')

    let next_gen_comments = comments.filter(
      subcomment => subcomment.depth >= depth + 1,
    )

    let filtered_comments = comments.filter(
      comment => {
        return comment.depth === depth && comment.parent === parent
      }
    )

    for (comment of filtered_comments) {
      draw_comment(comments_dom, comment)
      if(next_gen_comments.length > 0)
        posts_comments_list_draw(next_gen_comments, comment.id, depth + 1)
    }
  }

  response = await posts_comments_list_request(url);

  if (response === false | response.status != 200)
    alert('서버 장애입니다!')
  else
    posts_comments_list_draw(await response.json())
}

const show_add_comment_modal = (event) => {
  const classname = ".modal.posts-comments-create"
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
