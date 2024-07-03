const $fromularioDireccion= document.getElementById('formulario-direccion');
const $txtCalle = document.getElementById('calle');
const $txtNumero = document.getElementById('numero');
const $txtColonia = document.getElementById('colonia');
const $txtCodigoPostal = document.getElementById('codigoPostal');
const $txtDelMnpio = document.getElementById('delMnpio');
const $txtEstado = document.getElementById('estado');
const btnGuardar = document.getElementById('liveAlertBtn');

(function () {
    $fromularioDireccion.addEventListener('submit', function(e) {
        let calle = String($txtCalle.value).trim();
        let numero = String($txtNumero.value).trim();
        let colonia = String($txtColonia.value).trim();
        let codigoPostal = String($txtCodigoPostal.value).trim();
        let delMnpio = String($txtDelMnpio.value).trim();
        let estado = String($txtEstado.value).trim();

        if(calle.length == 0 || 
            numero.length == 0 || 
            colonia.length == 0 || 
            codigoPostal.length == 0 || 
            delMnpio.length == 0 || 
            estado.length == 0
            ) {
            alert("¡Ningun campo puede estar vacio!");
            e.preventDefault();
        }
    });
    
    btnGuardar.addEventListener('click', function(e) {
        let confirmacion = confirm("¿Desea guardar la nueva dirección?");
        if(!confirmacion) {
            e.preventDefault();
        }
    })
})();
