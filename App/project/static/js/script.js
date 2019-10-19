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
