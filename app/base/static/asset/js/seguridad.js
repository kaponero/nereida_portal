
// agrega la clase 'hovered' a la lista seleccionada
let list = document.querySelectorAll(".navigation li");
const boton_aceptar =  document.querySelector(".boton-wrap");
const pass_actual = document.getElementById("psw");
const icon_actual = document.getElementById("actual");
const pass_nuevo = document.getElementById("new_psw");
const icon_nuevo = document.getElementById("nueva");
const pass_repite = document.getElementById("repite_psw");
const icon_repite = document.getElementById("repite");


//mostrar contraseña
icon_actual.addEventListener("click",function(){
  if (pass_actual.type === "password"){
    pass_actual.type = "text";
    icon_actual.name = "eye-off-outline";
  } else {
    pass_actual.type = "password";
    icon_actual.name = "eye-outline";
  }
})

icon_nuevo.addEventListener("click",function(){
  if (pass_nuevo.type === "password"){
    pass_nuevo.type = "text";
    icon_nuevo.name = "eye-off-outline";
  } else {
    pass_nuevo.type = "password";
    icon_nuevo.name = "eye-outline";
  }
})

icon_repite.addEventListener("click",function(){
  if (pass_repite.type === "password"){
    pass_repite.type = "text";
    icon_repite.name = "eye-off-outline";
  } else {
    pass_repite.type = "password";
    icon_repite.name = "eye-outline";
  }
})

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

  const error = document.getElementById('error_tamanio');

  // Largo mínimo
  if (pass_nuevo.value.length < 8) {
    error.style.display = "block";
    return false;
  }

  error.style.display = "none";

  // Coincidencia (extra, aunque backend ya valida)
  if (pass_nuevo.value !== pass_repite.value) {
    alert("Las contraseñas no coinciden");
    return false;
  }

  // ✅ Todo OK → dejar que el navegador haga el POST
  return true;
}
