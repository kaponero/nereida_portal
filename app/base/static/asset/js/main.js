
// agrega la clase 'hovered' a la lista seleccionada
let list = document.querySelectorAll(".navigation li");

function activeLink(){
    list.forEach((item) => {
        item.classList.remove("hovered");
    });
    this.classList.add("hovered");
}

list.forEach(item => item.addEventListener("mouseover", activeLink));

// Desplazamiento del Menu
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function(){
    navigation.classList.toggle("active");
    main.classList.toggle("active");
}


//tamaño del archivo
let fileInput = document.getElementById("fotoPerfil");
let fileResult = document.getElementById("file-result");
let fileSubmit = document.getElementById("file-submit");

fileInput.addEventListener("change", function () {  
    if (fileInput.files.length > 0) {
      const fileSize = fileInput.files.item(0).size;
      const fileMb = fileSize / 1024 ** 2;
      if (fileMb >= 3) {
        fileResult.style.color = 'red'
        fileResult.innerHTML = "Por favor seleccionar un archivo de menos de 3MB";
        fileSubmit.disabled = true;
      } else {
        fileResult.style.color = 'green'
        fileResult.innerHTML = "Su archivo es de " + fileMb.toFixed(1) + "MB.";
        fileSubmit.disabled = false;
      }
    }
  });


function verificarPasswords() {
 
  pass1 = document.getElementById('new_psw');
  pass2 = document.getElementById('repite_psw');

  if (pass1.value != pass2.value){
    alert("las contraseñas deben ser iguales");
    return false;
  }
  else{
    document.getElementById("f-psw").submit()
  }
 
}