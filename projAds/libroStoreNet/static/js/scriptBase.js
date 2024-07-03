
        // JavaScript para ocultar los mensajes después de 5 segundos
        $(document).ready(function(){
            setTimeout(function() {
                $('.messages .alert').fadeOut('slow', function() {
                    $(this).remove();
                });
            }, 5000); // 5 segundos
        });
    