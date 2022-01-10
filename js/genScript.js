// Code based on:
//////////////////////////////////////////////
//    Title: Random Quote Generator Using HTML, CSS and JavaScript
//    Author: coder_srinivas
//    Date: 25 Feb, 2021
//    Availability: https://www.geeksforgeeks.org/random-quote-generator-using-html-css-and-javascript/
//
//////////////////////////////////////////////

// Global Variable used to store the quotes 

var data;
var prevIndex;
let front = true;
  
// Getting the front and the back author boxes
const authors = document.querySelectorAll(".author");
  
// Getting the front and the back texts
const texts = document.querySelectorAll(".text");

// Getting the front and the back translations
const translations = document.querySelectorAll(".translation");
  
// Getting the body
const body = document.getElementById("body");
  
// Getting the buttons
const button = document.querySelectorAll(".new-quote");
  
const blockFront = document.querySelector(".block__front");
const blockBack = document.querySelector(".block__back");
  
const authorFront = authors[0];
const authorBack = authors[1];
  
const textFront = texts[0];
const textBack = texts[1];

const transFront = translations[0];
const transBack = translations[1];
  
const buttonFront = button[0];
const buttonBack = button[1];
  
  
// An arrow function used to get a quote randomly
const displayQuote = () =>{
  
    // Generates a random number between 0 
    // and the length of the dataset
    let index = Math.floor(Math.random()*data.length);
    
    
    while(index == prevIndex){
      index = Math.floor(Math.random()*data.length);
    };
  
    // Stores the quote present at the randomly generated index
    let quote = data[index].text;
  
    // Stores the translation present at the randomly generated index
    let translation = data[index].translation;
  
    // Stores the author of the respective quote
    let author = data[index].author;
  
    // Making the author anonymous if no author is present
    if(!author){
        author = "Anonymous"
    }
  
    // If the quote does not require translation
    if(!translation){
        translation = ""
    }
  
    prevIndex = index;
  
    // Replacing the current quote and the author with a new one
  
    if(front){
        // Changing the front if back-side is displayed
        textFront.innerHTML = quote;
        transFront.innerHTML = translation;
        authorFront.innerHTML = author;
    }else{
        // Changing the back if front-side is displayed
        textBack.innerHTML = quote;
        transBack.innerHTML = translation;
        authorBack.innerHTML = author;
    }
      
    front = !front;
  
}
  
// Fetching the quotes from the type.fit API using promises
fetch('json/quotes.json')
    .then(function(response) {
        return response.json(); 
    }) // Getting the raw JSON data
    .then(function(data) {
  
        // Storing the quotes internally upon 
        // successful completion of request
        this.data = data; 
  
        // Displaying the quote When the Webpage loads
        displayQuote() 
});
  
  
// Adding an onclick listener for the button
function newQuote(){
      
    // Rotating the Quote Box
    blockBack.classList.toggle('rotateB');
    blockFront.classList.toggle('rotateF');
  
    // Displaying a new quote when the webpage loads
    displayQuote();
}
