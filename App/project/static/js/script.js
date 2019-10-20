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

$(document).on('click','[id^="like_"]',function(){
  var spId = $(this).attr('id').split('_')[1];
  /*alert('You clicked');*/
  $.ajax({
      url: '/add_evaluation_like',
      method: 'POST',
      data: {'question_id': $(this).attr('id').split('_')[1], 'csrfmiddlewaretoken': '{{ csrf_token }}'},
      success: function(response){
        /*alert(response.message);*/
        $('#span_'+spId).html(' ' + response.likes_count + ' like this');
      },
      error: function(re, e){
        alert(rs.responseText);
      }
  });
})

$(document).on('click','[id^="solution_"]',function(){
  var spId = $(this).attr('id').split('_')[1];
  /*alert('You clicked');*/
  $.ajax({
      url: '/has_user_answered',
      method: 'POST',
      data: {'question_id': $(this).attr('id').split('_')[1], 'csrfmiddlewaretoken': '{{ csrf_token }}'},
      success: function(response){
        if (response.status == 1){
          location.href = response.url;
        }
        else{
          alert(response.message);
        }
      },
      error: function(re, e){
        alert(rs.responseText);
      }
  });
})
