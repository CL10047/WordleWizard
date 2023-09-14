function showPasswordRequirements() {
    document.getElementById('password_requirement').style.display = "block";
}

document.getElementById('password_field').onblur = function() {
    document.getElementById("password_requirement").style.display = "none";
}

document.getElementById('password_field').onkeyup = function() {
    var lowerCaseLetters = /[a-z]/g;
    if(myInput.value.match(lowerCaseLetters)) {  
      letter.classList.remove("invalid");
      letter.classList.add("valid");
    } else {
      letter.classList.remove("valid");
      letter.classList.add("invalid");
    }

    var upperCaseLetters = /[A-Z]/g;
    if(myInput.value.match(upperCaseLetters)) {  
      capital.classList.remove("invalid");
      capital.classList.add("valid");
    } else {
      capital.classList.remove("valid");
      capital.classList.add("invalid");
    }

    var numbers = /[0-9]/g;
    if(myInput.value.match(numbers)) {  
      number.classList.remove("invalid");
      number.classList.add("valid");
    } else {
      number.classList.remove("valid");
      number.classList.add("invalid");
    }

    if(myInput.value.length >= 8) {
      length.classList.remove("invalid");
      length.classList.add("valid");
    } else {
      length.classList.remove("valid");
      length.classList.add("invalid");
    }
  }

let myInput = document.getElementById("password_field");
let length = document.getElementById("password_requirement_1");
let capital = document.getElementById("password_requirement_2");
let letter = document.getElementById("password_requirement_3");
let number = document.getElementById("password_requirement_4");
