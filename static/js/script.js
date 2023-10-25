/*
Resource: Interesting Facts On The Colour Blue - https://www.janelockhart.com/blog/interesting-facts-colour-blue/
*/

const listItems = document.querySelectorAll(".main-menu li");

listItems.forEach((listItem) => {
  listItem.addEventListener("click", () => {
    listItems.forEach((otherItem) => {
      otherItem.classList.remove('active')
    })
    listItem.classList.add('active')
  });
});