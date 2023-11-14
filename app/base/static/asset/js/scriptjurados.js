function recuperar_calificacion(identificador,valor_calificacion){
	
    var select= document.getElementById(identificador);
    if(valor_calificacion != null){
        select.selectedIndex = valor_calificacion;
    }
}