// https://www.youtube.com/watch?v=qO1bgMG7sO8&list=PL4cUxeGkcC9ib4HsrXEYpQnTOTZE1x0uc&index=32
const titleInput = document.querySelector('input[name=title]');
const slugInput = document.querySelector('input[name=slug]');

const slugify = (val) => {
  return val.toString().toLowerCase().trim()
    .replace(/&/g, '-and-')  // replace & with -and-
    .replace(/[\s\W-]+/g, '-') // replaces spaces, non word chars and dashes with a single dash
}

titleInput.addEventListener('keyup', (e)=> {
  slugInput.setAttribute('value', slugify(titleInput.value));
})