jQuery(document).ready(function() {
	
    //BG Home + search
	calcularBgHome();
	var ancho = anchoSearchHome();
	ancho = Math.abs(ancho);
	anchoSearchHome2(ancho);
	
	/*
	//Al hacer click sobre el menu que no se cierre
	jQuery('.menuHeadResponsive').click(function() {
		jQuery('.menuHeadResponsive').css("display","block");
		jQuery(".rightInfo").css("display","block");
		return false;
	});
	*/
	
	//Asigo el alto del hover #000000 al  alto del body
	var altoBody2 = jQuery("body").height()+80;
	jQuery(".popUpContent").css("height",altoBody2);
	
	//Close hover #000000
	jQuery('.popUpContent').click(function() {
		jQuery("header.interna .max.head.headTop").css("z-index","inherit");
		jQuery(".rightInfo").css("display","block");
		closed();
	});
	
	//Muestro el titulo en las internas
	getTitle();
	
	//Hamburguesa
	showMenu();
	
	//Responsive menu
	jQuery('.hamburger').click(function() {
		jQuery('.hamburger').toggleClass('is-active');
		//Ciero el buscador en caso de estar abierto
		closeSearch();
		//Abro el menu
		popUpMenu();
		jQuery(".rightInfo").css("display","block");
		return false;
	});
	
	//?????
	jQuery('.popUpMenu').click(function() {
		closedMenu();
	});
	
	
	//Acciones del Boton de buscar
	jQuery('.iconSearch').click(function() {
		jQuery('.iconSearch').toggleClass('open');
		openCloseSearchResponsive();
		return false;
	});
	
	//Efecto acoordeon
	var acc = document.getElementsByClassName("accordion");
	var i;
	for (i = 0; i < acc.length; i++) {
		acc[i].addEventListener("click", function() {
			this.classList.toggle("active");
			var panel = this.nextElementSibling;
			if (panel.style.maxHeight){
				panel.style.maxHeight = null;
			} else {
				panel.style.maxHeight = panel.scrollHeight + "px";
			} 
		});
	}
	
	//Habilitar filtros de los resultados de busqueda
	jQuery('.filtrosRes').click(function() {
		jQuery('.filtrosRes').toggleClass('openFiltroRes');
		showFiltrosResBusqueda();
		return false;
	});
	
	//Calcular
	calcularAnchoRotadorRes();
	
	//Animacion para anclas
	$('.perfilMenu a').click(function(e){				
		e.preventDefault();		//evitar el eventos del enlace normal
		var strAncla=$(this).attr('href'); //id del ancla
			$('body,html').stop(true,true).animate({				
				scrollTop: $(strAncla).offset().top
			},1000);
		
	});
	
	//calcular altura de los box del perfil de profe - usuarioo logueado
	calcularAltoBoxPerfilProfe();
	
	//Muestro formualrio de contactenos al profe en perfil del profe
	showFormularioProfeRes();
	
	//Calcular los anchos de la ficha en perfil del profe
	anchoFichaPerfilProfe();
	
	
	
});


jQuery(window).resize(function() {
	//Muestro el titulo
	getTitle();
	//Hamburguesa
	showMenu();
	
	//BG Home + search
	calcularBgHome();
	var ancho = anchoSearchHome();
	ancho = Math.abs(ancho);
	
	calcularAnchoRotadorRes();
	
	//Muestro formualrio de contactenos al profe en perfil del profe
	showFormularioProfeRes();
	
	//Calcular los anchos de la ficha en perfil del profe
	anchoFichaPerfilProfe();
	
	//calcular altura de los box del perfil de profe - usuarioo logueado
	calcularAltoBoxPerfilProfe();
	
	//Ajusto alto/ancho de los box
	//jQuery(".boxBox").css("display","block");
	
	
});



jQuery(function($) {
	//Coloco en position fixed Formualrio Contancto Profe En Perfil
	function fixDiv() {
		if(jQuery(".rightMin").length > 0){
			//Obtengo sus coordenadas
			var coordenadas = $(".rightMin").offset();
			//alert("coordenadas.left " + coordenadas.left + " - coordenadas.top " + coordenadas.top);
			var $cache = $('.rightMin');
			if ($(window).scrollTop() > 200){
				if($(".rightMin").css("position") === "fixed"){
				}else{
					$cache.css({
						'position': 'fixed',
						'left': coordenadas.left+'px',
						'top': '20px'
					});
				}
			}else{
				$cache.css({
					'position': 'relative',
					'top': 'auto',
					'left': 'auto'
				});
			}
		}
	}
	$(window).scroll(fixDiv);
});



function calcularAltoBoxPerfilProfe(){
	if (jQuery(window).width()>=1180) {
		//Fila 1
		var alto_infoBasca = jQuery("#infoBasca").height();
		var alto_ubicacion = jQuery("#ubicacion").height();
		//Fila 2
		var alto_mediosPago = jQuery("#mediosPago").height();
		var alto_profesores = jQuery("#profesores").height();
		//Fila 3
		var alto_facilidades = jQuery("#facilidades").height();
		var alto_comodidades = jQuery("#comodidades").height();
			
		//Asigno los altos del mas alto de cada fila
		//Fila 1
		if(alto_infoBasca>alto_ubicacion){
			jQuery("#ubicacion").css("height",alto_infoBasca);
		}else{
			jQuery("#infoBasca").css("height",alto_ubicacion);
		}
		//Fila 2
		if(alto_mediosPago>alto_profesores){
			jQuery("#profesores").css("height",alto_mediosPago);
		}else{
			jQuery("#mediosPago").css("height",alto_profesores);
		}
		//Fila 3
		if(alto_facilidades>alto_comodidades){
			jQuery("#comodidades").css("height",alto_facilidades);
		}else{
			jQuery("#facilidades").css("height",alto_comodidades);
		}
	}else{
		jQuery("#ubicacion").css("height","auto");
		jQuery("#infoBasca").css("height","auto");
		jQuery("#profesores").css("height","auto");
		jQuery("#mediosPago").css("height","auto");
		jQuery("#comodidades").css("height","auto");
		jQuery("#facilidades").css("height","auto");
	}
}



function anchoFichaPerfilProfe(){
	if (jQuery(window).width()<1180) {
		//Obtengo el ancho de max en el head
		var anchoMax = jQuery(".max").width();
		jQuery(".fichaPerfilProfe").css("width",anchoMax);
		jQuery(".bottomInfo").css("width",anchoMax);
	}else{
		
	}
	
}


function showFormularioProfeRes(){
	if(jQuery(".rightMin").length > 0){
		var aux = jQuery(".rightMin").html();
		if (jQuery(window).width()<1180) {
			var auxExisteResponsive = jQuery("#formularioRespEnvioProfe").html();
			if(auxExisteResponsive.length == 0){
				jQuery("#formularioRespEnvioProfe").html("<div class='max'>" + aux + "</div>");
			}
		}else{
			if(aux.length==0){
				jQuery(".rightMin").html(aux);
			}
		}
	}
}




function calcularAnchoRotadorRes(){
	/*if (jQuery(window).width()<1180) {
		var anchoRotaRes = jQuery(".stepcarousel .boxCarrusel").width();
		var anchoIMGRotRes = jQuery(".stepcarousel .boxCarrusel img").width();
		var maxValor = anchoRotaRes - anchoIMGRotRes -50;
		alert("anchoRotaRes " + anchoRotaRes + " - anchoIMGRotRes " + anchoIMGRotRes + " - maxValor " + maxValor);
		jQuery(".stepcarousel .boxCarrusel .rightInfo").css("width",maxValor);
		var anchoRotaRes = jQuery(".stepcarousel .boxCarrusel").css("width",anchoRotaRes-20);
	}*/
}



function showListado(){
	jQuery('.imageSelect img.list').addClass("tipoResSeleccionado");
	jQuery('.imageSelect img.map').removeClass("tipoResSeleccionado");
	jQuery('.listResult').css("display","block");
	jQuery('.mapResult').css("display","none");
}


function showMap(){
	jQuery('.imageSelect img.list').removeClass("tipoResSeleccionado");
	jQuery('.imageSelect img.map').addClass("tipoResSeleccionado");
	jQuery('.listResult').css("display","none");
	jQuery('.mapResult').css("display","block");
}


function showForSearch(){
	jQuery(".popUpContentBox").css("display","block");
	popUp();
}
function closedForSearch(){
	jQuery(".popUpContentBox").css("display","none");
	closed();
}


function showFiltrosResBusqueda(){
	if (jQuery(window).width()<1180) {
		if (jQuery(".filtrosRes").hasClass("openFiltroRes")) {
			jQuery("section.left").css("display","block");
			//Alto de los filtros
			var altoFiltros = jQuery("section.left").height();
			//Obtengo los altos de los controles del rotador
			var imgLeft = jQuery("#leftButtonRota").css("top"); //Ej. 120px			
			var auxLeft = imgLeft.substring(0, imgLeft.length-2);
			var resultado = parseInt(altoFiltros) + parseInt(auxLeft) + 40;
			jQuery("#leftButtonRota").css("top",resultado + "px");
			jQuery("#rightButtonRota").css("top",resultado + "px");
		}else{
			jQuery("section.left").css("display","none");
			//Alto de los filtros
			var altoFiltros = jQuery("section.left").height();
			//Obtengo los altos de los controles del rotador
			var imgLeft = jQuery("#leftButtonRota").css("top"); //Ej. 120px			
			var auxLeft = imgLeft.substring(0, imgLeft.length-2);
			var resultado = parseInt(auxLeft) - parseInt(altoFiltros) -40;
			jQuery("#leftButtonRota").css("top",resultado + "px");
			jQuery("#rightButtonRota").css("top",resultado + "px");
		}
	}
}



function openCloseSearchResponsive(){
	if (jQuery(".iconSearch").hasClass("open")) {
		//alert("abierto");
		jQuery(".bluePopUpContent").css("display","block");
		jQuery(".bluePopUpContent").css("z-index","2");
		jQuery("header.interna .max.head.headTop").css("z-index","3");
		jQuery(".popUpContent").css("display","block");
		jQuery(".popUpContent").css("z-index","1");
		jQuery(".hamburger").css("z-index","2");
		jQuery(".rightInfo").css("display","none");
	}else{
		//alert("cerrado");
		jQuery(".bluePopUpContent").css("display","none");
		jQuery("header.interna .max.head.headTop").css("z-index","inherit");
		//jQuery("header.interna .internaHeadLeft .logo").css("z-index","inherit");
		jQuery(".popUpContent").css("display","none");
		jQuery(".hamburger").css("z-index","1");
		jQuery(".rightInfo").css("display","block");
	}
}

//Verifico si est[a habilitado el buscador y lo deshabilito
function closeSearch(){
	if (jQuery(".iconSearch").hasClass("open")) {
		jQuery("header.interna .max.head.headTop").css("z-index","inherit");
		jQuery(".bluePopUpContent").css("display","none");
		jQuery(".popUpContent").css("display","none");
		if (jQuery(".iconSearch").hasClass("open")) {
			jQuery(".iconSearch").removeClass("open");
		}
	}
	
}

//Muestra o no el Menu responsive
function popUpMenu(){
	//Alto del body para asignarlo al .popUpMenu 
	var altoBody = jQuery("body").height();
	jQuery(".popUpMenu").css("height",altoBody);
	
	//jQuery("header.interna .max.head.headTop").css("z-index","1");
	jQuery("header.interna .max.head.headTop .hamburger").css("z-index","2");
	if (jQuery(".hamburger").hasClass("is-active")) {
		//alert("tiene");
		jQuery(".popUpMenu").css("display","block");
		jQuery(".menuHeadResponsive").css("display","block");
		jQuery(".hamburger").css("z-index","2");
	}else{
		//alert("NO tiene");
		jQuery(".popUpMenu").css("display","none");
		jQuery(".menuHeadResponsive").css("display","none");
		jQuery(".hamburger").css("z-index","1");
	}
}


function showMenu(){
	if (jQuery(window).width()<1180) {
		jQuery(".hamburger").css("display", "block");
		jQuery(".menu").css("display", "none");
		jQuery(".menuHeadResponsive").css("display", "none");
	}else{
		jQuery(".menu").css("display", "block");
		jQuery(".hamburger").css("display", "none");
		jQuery(".menuHeadResponsive").css("display", "none");
	}
	
}

function getTitle(){
	var aux = jQuery(".titleH1").html();
	if (jQuery(window).width()<1180) {
		jQuery(".titleRes").html("<h1>" + aux + "</h1>");
	}
}

function calcularBgHome(){
	if (jQuery(window).width()<330) {
		var alto = jQuery(window).height() + 180;
		jQuery("header.home").css("height",alto);
	}else if (jQuery(window).width()<980) {
		var alto = jQuery(window).height() + 100;
		jQuery("header.home").css("height",alto);
	}else{
		var alto = jQuery(window).height();
		jQuery("header.home").css("height",alto);
	}
}

function anchoSearchHome(){
	var anchoTotal = jQuery(".formulario").outerWidth();
	var anchoBox1 = jQuery(".boxCombo").outerWidth();
	var anchoBoxDir = jQuery(".dir").outerWidth();
	var ancho = anchoTotal - anchoBox1 - anchoBox1 - anchoBoxDir;
	ancho = ancho - 40; /* le resto el padding-left*/
	if (jQuery(window).width()>1180) {
		jQuery(".formulario .search").css("width", ancho);
		return ancho;
	}else{
		jQuery(".formulario .search").css("width", ancho);
		return ancho;
	}
}



function anchoSearchHome2(search){
	var anchoTotal = jQuery(".formulario2").outerWidth();
	var alto = jQuery(".formulario2").height();
	var ancho = anchoTotal - search;
	ancho = ancho - 80; /* resto padding*/
	jQuery(".formulario2 input.profe").css("width",ancho);
	jQuery(".formulario2 .search").css("width",search);
	jQuery(".formulario2 input").css("height",alto);
}

function popUp(){
	jQuery(".popUpContent").css("display","block");
	jQuery(".popUpContentBox").css("display","block");
}

function closed(){
	jQuery(".popUpContent").css("display","none");
	jQuery(".popUpContentBox").css("display","none");
	jQuery(".bluePopUpContent").css("display","none");
	if (jQuery(".iconSearch").hasClass("open")) {
		jQuery(".iconSearch").removeClass("open");
	}
}

function closedMenu(){
	jQuery(".popUpMenu").css("display","none");
	jQuery('.hamburger').toggleClass('is-active');
	
}


function irA(url){
	if(url=="registro"){
		window.location = "registro.html";
	} else {
		
		window.location = url;

	}
	
}



function clickMenu(){
	var index = 0;
	/*
		jQuery("#itemItau").click(function(){
			if (jQuery(window).width()<980) {
				if (jQuery("#itemItau").hasClass(".openmenu") ) {
			 		jQuery("#itemItau").removeClass(".openmenu");
			 		jQuery("#itemItau").addClass(".closemenu");
					jQuery(".menu-local-items").hide(300);
					index++;
			 	} else {
					jQuery("#itemItau").addClass(".openmenu");
					jQuery("#itemItau").removeClass(".closemenu");
					jQuery(".menu-local-items").show(300);
					index = 0;
			 	}
			}else{
				if (jQuery("#itemItau").hasClass(".closemenu") ) {
					jQuery("#itemItau").removeClass(".closemenu");
					jQuery(".menu-local-items").show(300);
				}
			}
		});
	*/
}



/*

// selector
var menu = document.querySelector('.hamburger');

// method
function toggleMenu (event) {
  this.classList.toggle('is-active');
  document.querySelector( ".menuppal" ).classList.toggle("is_active");
  event.preventDefault();
}

// event
menu.addEventListener('click', toggleMenu, false);
*/
//Solución con jQUery
/*jQuery(document).ready(function(){
	jQuery('.hamburger').click(function() {
		jQuery('.hamburger').toggleClass('is-active');
		jQuery('.menuresponsive').toggleClass('is-active');
		return false;
	});
});*/





