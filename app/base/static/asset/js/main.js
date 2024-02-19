
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
  } else {
    pass_actual.type = "password";
  }
})

icon_nuevo.addEventListener("click",function(){
  if (pass_nuevo.type === "password"){
    pass_nuevo.type = "text";
  } else {
    pass_nuevo.type = "password";
  }
})

icon_repite.addEventListener("click",function(){
  if (pass_repite.type === "password"){
    pass_repite.type = "text";
  } else {
    pass_repite.type = "password";
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
 
  pass = document.getElementById('psw');
  pass1 = document.getElementById('new_psw');
  pass2 = document.getElementById('repite_psw');
  modal_wrapper = document.querySelector(".modal_wrapper");
  var error = document.getElementById("mensaje");
  const boton = document.getElementById("btns");
  const icon_error = document.getElementById("icon-error");
  const icon_ok = document.getElementById("icon-ok");

  if (pass.value.length==0){
    modal_wrapper.classList.add("active");
    error.innerHTML = "Ingrese la contraseña actual";
    return false;
  }
  else if (pass1.value.length==0){
    modal_wrapper.classList.add("active");
    error.innerHTML = "Ingrese la nueva contraseña";
    return false;
  }
  if (pass2.value.length==0){
    modal_wrapper.classList.add("active");
    error.innerHTML = "Repita la nueva contraseña";
    return false;
  }
  else if (pass1.value.length<8 || pass1.value.length<8){
    modal_wrapper.classList.add("active");
    error.innerHTML = "La contraseña debe ser mayor a 8 caracteres";
    return false;
  }
  else if (pass1.value != pass2.value){
    modal_wrapper.classList.add("active");
    error.innerHTML = "Las contraseñas deben ser iguales";
    return false;
  }
  else if (pass.value == pass1.value){
    modal_wrapper.classList.add("active");
    error.innerHTML = "La nueva contraseña debe ser distinta a su contraseña anterior";

    return false;
  }
  else{
    /*modal_wrapper.classList.add("active");
    boton.style.display="none";
    icon_error.style.display="none";
    icon_ok.style.display="block";
    error.innerHTML = "La contraseña ha sido cambiada con exito";
    setTimeout(() => {
      console.log("2 Segundo esperado")
    }, 2000);*/
    document.getElementById("f-psw").submit()
  }
 
}

 function cerrar(){
	modal_wrapper.classList.remove("active");
}

//mostrar contraseña
icon_actual.addEventListener("click",function(){
  if (pass_actual.type === "password"){
    pass_actual.type = "text";
  } else {
    pass_actual.type = "password";
  }
})