for (const btn of document.querySelectorAll('.upvote')) {
  btn.addEventListener('click', event => {
    event.target.classList.toggle('on');
  });
}

for (const btn of document.querySelectorAll('.downvote')) {
  btn.addEventListener('click', event => {
    event.target.classList.toggle('on');
  });
}

for (const btn of document.querySelectorAll('.star')) {
  btn.addEventListener('click', event => {
    event.target.classList.toggle('on');
  });
}

$('.like').click(function(){
    $.ajax({
        url: '/add_evaluation_like',
        method: 'POST',
        data: {'question_id': $(this).attr('name'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        success: function(response){
          alert(response.message);
          alert('Company likes count is now ' + response.likes_count);
        },
        error: function(rs, e) {
          alert(rs.responseText);
        }
    });
  })
