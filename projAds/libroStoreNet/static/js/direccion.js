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
        const alertPlaceholder = document.getElementById('liveAlertPlaceholder')

        const appendAlert = (message, type) => {
            const wrapper = document.createElement('div')
            wrapper.innerHTML = [
            `<div class="alert alert-${type} alert-dismissible" role="alert">`,
            `   <div>${message}</div>`,
            '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
            '</div>'
            ].join('')
        
            alertPlaceholder.append(wrapper)
        }

        let confirmacion = confirm("¿Desea guardar la nueva dirección?");
        if(!confirmacion) {
            e.preventDefault();
        }
        else {
            appendAlert('¡Dirección guardada con éxito!', 'success')
        }
    })
})();
