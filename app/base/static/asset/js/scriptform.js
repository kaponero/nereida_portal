var form_1 = document.querySelector(".form_1");
var form_2 = document.querySelector(".form_2");
var form_3 = document.querySelector(".form_3");
var form_4 = document.querySelector(".form_4");
var form_5 = document.querySelector(".form_5");

var form = document.querySelector("form")

var form_1_btns = document.querySelector(".form_1_btns");
var form_2_btns = document.querySelector(".form_2_btns");
var form_3_btns = document.querySelector(".form_3_btns");
var form_4_btns = document.querySelector(".form_4_btns");
var form_5_btns = document.querySelector(".form_5_btns");


var form_1_next_btn = document.querySelector(".form_1_btns .btn_next");
var form_2_back_btn = document.querySelector(".form_2_btns .btn_back");
var form_2_next_btn = document.querySelector(".form_2_btns .btn_next");
var form_3_back_btn = document.querySelector(".form_3_btns .btn_back");
var form_3_next_btn = document.querySelector(".form_3_btns .btn_next");
var form_4_back_btn = document.querySelector(".form_4_btns .btn_back");
var form_4_next_btn = document.querySelector(".form_4_btns .btn_next");
var form_5_back_btn = document.querySelector(".form_5_btns .btn_back");

var form_2_progessbar = document.querySelector(".form_2_progessbar");
var form_3_progessbar = document.querySelector(".form_3_progessbar");
var form_4_progessbar = document.querySelector(".form_4_progessbar");
var form_5_progessbar = document.querySelector(".form_5_progessbar");

var btn_done = document.querySelector(".btn_done");
var btn_cancel = document.querySelector(".btn_cancel");
var btn_aceptar = document.querySelector(".btn_aceptar");
var modal_wrapper = document.querySelector(".modal_wrapper");
var shadow = document.querySelector(".shadow");

var correo= /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
var cuil = /^[0-9]{11}$/
var telefono = /^[0-9]{3}[0-9]{7}|[0-9]{7}$/
var time_max = "04:00"
var time_min = "00:00"


form_1_next_btn.addEventListener("click", function(){

	var selectcat = document.getElementById('localidadCategoria').value
	var selectcat2 = document.getElementById('localidadCategoria2').value
	var selectgen = document.getElementById('generoPrograma').value
	var inputrazons = document.getElementById('razonSocial')
	var inputcuit = document.getElementById('numeroCuit').value
	var cuilvalido = cuil.test(inputcuit);
	var no_es_socio = document.getElementById("no_es_socio");
	var es_socio = document.getElementById("es_socio");

	valid_input('localidadCategoria', 'Selecione una categoria', 'error-localidadCategoria');
	valid_input('localidadCategoria2', 'Selecione una categoria', 'error-localidadCategoria2');
	valid_input('generoPrograma', 'Seleccione un género', 'error-genero');
	valid_input('razonSocial', 'Ingrese la razon social', 'error-razonSocial');
	valid_cuil('numeroCuit', 'Ingrese el cuit sin espacios', 'error-numeroCuit');
	

	if (es_socio.style.display == 'none'  && no_es_socio.style.display == 'none'){
		alert ("Verifique el cuit")
	}else if(inputrazons.value.length == 0 && inputrazons.readOnly == true){
		alert ("Verifique el cuit y localidad")
		valid_input('razonSocial', 'Verifique los datos', 'error-razonSocial');
	}
	else if ((selectcat  == 0 &&  selectcat2 == 0) || selectgen == 0 || 
	inputrazons.value.length == 0 || cuilvalido == false){
		alert ("Complete los campos")
	}
	else{
		form_1.style.display = "none";
		form_2.style.display = "block";
		form_1_btns.style.display = "none";
		form_2_btns.style.display = "flex"; 
		form_2_progessbar.classList.add("active");}
});

form_2_back_btn.addEventListener("click", function(){

	form_1.style.display = "block";
	form_2.style.display = "none";
	form_1_btns.style.display = "flex";
	form_2_btns.style.display = "none";
	form_2_progessbar.classList.remove("active");
});

form_2_next_btn.addEventListener("click", function(){

	var inputtnom = document.getElementById('nombrePrograma').value
	var selectviv = document.getElementById('enVivo').value
	var inputlocal= document.getElementById('localidadEmision').value
	var inputdate= document.getElementById('input_date').value
	var inputtime= document.getElementById('input_time').value
	var inputtarea= document.getElementById('input_tarea').value

	valid_input('nombrePrograma', 'Ingrese el nombe del programa', 'error-nombrePrograma');
	valid_input('enVivo', 'Elija una opción', 'error-vivo');
	valid_input('localidadEmision', 'Ingrese localidad de emisión', 'error-localidad');
	valid_input('input_date', 'Ingrese fecha de emisión', 'error-fecha');
	valid_input('input_tarea', 'Ingrese una breve descripción', 'error-tarea');
	valid_time('input_time', 'La duración tiene que ser menor a 4 hs', 'error-duracion');
	
	if (inputtnom.length == 0  || selectviv == 0 || inputlocal.length == 0 || 
		inputdate.length == 0 || inputtnom == time_min || inputtime > time_max || inputtarea.length == 0){
		alert ("Complete los campos")
	}
	else{
		form_2.style.display = "none";
		form_3.style.display = "block";
		form_3_btns.style.display = "flex";
		form_2_btns.style.display = "none";
		form_3_progessbar.classList.add("active");}
});

form_3_back_btn.addEventListener("click", function(){
	
	form_2.style.display = "block";
	form_3.style.display = "none";
	form_2_btns.style.display = "flex";
	form_3_btns.style.display = "none";
	form_3_progessbar.classList.remove("active");
});

form_3_next_btn.addEventListener("click", function(){
	
	var inputrutina = document.getElementById('linkRutina').value
	var inputvideo1 = document.getElementById('linkVideo1').value
	var inputvideo2 = document.getElementById('linkVideo2').value
	var inputvideo3 = document.getElementById('linkVideo3').value
	var inputcover= document.getElementById('linkCover').value

	valid_input('linkRutina', 'Ingrese link de la rutina', 'error-rutina');
	valid_input('linkVideo1', 'Ingrese link del video 1', 'error-video1');
	valid_input('linkVideo2', 'Ingrese link del video 2', 'error-video2');
	valid_input('linkVideo3', 'Ingrese link del video 3', 'error-video3');
	valid_input('linkCover', 'Ingrese link del cover', 'error-cover');
	
	if (inputrutina.length == 0 || inputvideo1.length  == 0 || inputvideo2.length == 0 || 
		inputvideo3.length == 0 || inputcover.length == 0 ){
		alert ("Complete los campos")
	}
	else{
		form_3.style.display = "none";
		form_4.style.display = "block";
		form_4_btns.style.display = "flex";
		form_3_btns.style.display = "none";
		form_4_progessbar.classList.add("active");
	}
});

form_4_back_btn.addEventListener("click", function(){

	form_3.style.display = "block";
	form_4.style.display = "none";
	form_4_btns.style.display = "none";
	form_3_btns.style.display = "flex";
	form_4_progessbar.classList.remove("active");
});

form_4_next_btn.addEventListener("click", function(){
	
	var inputproductor = document.getElementById('nombreProductor').value
	var inputcoproductor = document.getElementById('nombreCoproductor').value
	var inputautor = document.getElementById('nombreAutor').value
	var inputeditor = document.getElementById('nombreEditor').value
	var inputdirector = document.getElementById('nombreDirector').value
	var inputcamara = document.getElementById('nombreCamara').value
	var inputsonido = document.getElementById('nombreSonido').value
	var inputconductor = document.getElementById('nombreConductor').value
	var inputprotagonista = document.getElementById('nombreProtagonista').value
	var inputcronista = document.getElementById('nombreCronista').value

	valid_input('nombreProductor', 'Ingrese el nombre del Productor', 'error-nombreProductor');
	valid_input('nombreCoproductor', 'Ingrese el nombre del Coproductor', 'error-nombreCoproductor');
	valid_input('nombreAutor', 'Ingrese el nombre del Autor', 'error-nombreAutor');
	valid_input('nombreEditor', 'Ingrese el nombre del Editor', 'error-nombreEditor');
	valid_input('nombreDirector', 'Ingrese el nombre del Director', 'error-nombreDirector');
	valid_input('nombreCamara', 'Ingrese el nombre del Camarógrafo', 'error-nombreCamara');
	valid_input('nombreSonido', 'Ingrese datos del Sonidista', 'error-nombreSonido');
	valid_input('nombreConductor', 'Ingrese el nombre del Conductor/Presentador/Locutor', 'error-nombreConductor');
	valid_input('nombreProtagonista', 'Ingrese el nombre del Protagonista', 'error-nombreProtagonista');
	valid_input('nombreCronista', 'Ingrese el nombre del Cronista', 'error-nombreCronista');

	if (inputproductor.length == 0 || inputcoproductor.length  == 0 || inputautor.length == 0 || 
		inputeditor.length == 0 || inputdirector.length  == 0 || inputcamara.length  == 0 || 
		inputsonido.length == 0 || inputconductor.length  == 0 || inputprotagonista.length  == 0 || 
		inputcronista.length == 0){
		alert ("Complete los campos")
	}
	else{
		form_4.style.display = "none";
		form_5.style.display = "block";
		form_5_btns.style.display = "flex";
		form_4_btns.style.display = "none";
		form_5_progessbar.classList.add("active");}
});

form_5_back_btn.addEventListener("click", function(){
	
	form_4.style.display = "block";
	form_5.style.display = "none";
	form_5_btns.style.display = "none";
	form_4_btns.style.display = "flex";
	form_5_progessbar.classList.remove("active");
});


btn_done.addEventListener("click", function(){

	var inputnombrec= document.getElementById('nombreCanal').value
	var inputdireccionc = document.getElementById('direccionCanal').value
	var inputlocalidadc = document.getElementById('localidadCanal').value
	var inputcontactoc = document.getElementById('contactoCanal').value
	var inputtelefonoc = document.getElementById('telefonoCanal').value
	var inputemailc = document.getElementById('emailCanal').value
	var correovalido = correo.test(inputemailc);
	var telvalido = telefono.test(inputtelefonoc);
	var inputcheck = document.getElementById('condiciones').checked

	valid_input('nombreCanal', 'Ingrese el nombre del Canal', 'error-nombreCanal');
	valid_input('direccionCanal', 'Ingrese el domicilio del Canal', 'error-direccionCanal');
	valid_input('localidadCanal', 'Ingrese la localidad del Canal', 'error-localidadCanal');
	valid_input('contactoCanal', 'Ingrese un medio de contacto', 'error-contactoCanal');
	valid_tel('telefonoCanal', 'Ingrese el teléfono del Canal', 'error-telefonoCanal');
	valid_correo('emailCanal', 'Ingrese un correo valido', 'error-emailCanal');
	valid_condiciones('condiciones', 'Debe aceptar los terminos y condiciones', 'error-condiciones');
	
	if (inputnombrec.length == 0 || inputdireccionc.length == 0 || inputlocalidadc.length == 0 || 
		inputcontactoc .length == 0 || telvalido == false  || correovalido == false || inputcheck==false){
		alert ("Complete los campos")
	}
	else{
		document.getElementById('form1').submit();
	}
})


function valid_input(identificador,mensaje, diverror){
	var inputtnom = document.getElementById(identificador).value
	var error = document.getElementById(diverror);
	error.style.color = "red";

	var mensajeError = [];
	if(inputtnom.length == 0){
		mensajeError.push(mensaje);
	} 
	error.innerHTML = mensajeError.join(', ');
}

function valid_correo(identificador,mensaje, diverror){
	var inputtnom = document.getElementById(identificador).value
	var error = document.getElementById(diverror);
	var correovalido = correo.test(inputtnom);

	error.style.color = "red";

	var mensajeError = [];
	if(correovalido == false){
		mensajeError.push(mensaje);
	} 
	error.innerHTML = mensajeError.join(', ');
}

function valid_cuil(identificador,mensaje, diverror){
	var inputtnom = document.getElementById(identificador).value
	var error = document.getElementById(diverror);
	var cuilvalido = cuil.test(inputtnom);

	error.style.color = "red";

	var mensajeError = [];
	if(cuilvalido == false){
		mensajeError.push(mensaje);
	} 
	error.innerHTML = mensajeError.join(', ');
}

function valid_tel(identificador,mensaje, diverror){
	var inputtnom = document.getElementById(identificador).value
	var error = document.getElementById(diverror);
	var telvalido = telefono.test(inputtnom);

	error.style.color = "red";

	var mensajeError = [];
	if(telvalido == false){
		mensajeError.push(mensaje);
	} 
	error.innerHTML = mensajeError.join(', ');
}

function valid_time(identificador,mensaje, diverror){
	var inputtnom = document.getElementById(identificador).value
	var error = document.getElementById(diverror);
	error.style.color = "red";

	var mensajeError = [];
	if (inputtnom == time_min){
		mensajeError.push("Seleccione duración");
	}
	if(inputtnom > time_max){
		mensajeError.push(mensaje);
	} 
	error.innerHTML = mensajeError.join(', ');
}

function valid_condiciones(identificador,mensaje, diverror){
	var inputtnom = document.getElementById(identificador).checked
	var error = document.getElementById(diverror);
	error.style.color = "red";

	var mensajeError = [];
	if(inputtnom == false){
		mensajeError.push(mensaje);
	} 
	error.innerHTML = mensajeError.join(', ');
}

function ver_categoria(){
	var inputtnom = document.getElementById("socio");
	var es_socio = document.getElementById("es_socio");
	var no_es_socio = document.getElementById("no_es_socio");
	var selectcat = document.getElementById('localidadCategoria')
	var selectcat2 = document.getElementById('localidadCategoria2')

	if (inputtnom.options[inputtnom.selectedIndex].value == "si"){
		es_socio.style.display = 'block';
		no_es_socio.style.display = 'none';
		selectcat2.selectedIndex = "";
		modal_wrapper.classList.add("active");
	}
	else{
		es_socio.style.display = 'none';
		no_es_socio.style.display = 'block';
		selectcat.selectedIndex = "";
	}
}

btn_cancel.addEventListener("click", function(){
	var socio = document.getElementById("socio");
	var es_socio = document.getElementById("es_socio");
	var no_es_socio = document.getElementById("no_es_socio");
	no_es_socio.style.display = 'none';
	es_socio.style.display = 'none';
	socio.selectedIndex = "";
	modal_wrapper.classList.remove("active");

});

btn_aceptar.addEventListener("click", function(){
	var n_socio = document.getElementById("n_socio").value;
	var n_cuit = document.getElementById("n_cuit").value;
	var error = document.getElementById("error_socio");
	error.style.color = "red";
	var mensajeError = [];
	
	if (n_socio == "100" && n_cuit == "200")
	{
		modal_wrapper.classList.remove("active");
	}
	else
		mensajeError.push("ingrese un N° de socio y cuit valido");

	error.innerHTML = mensajeError.join(', ');

});