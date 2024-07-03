$(document).ready(function() {

  const filtradoLibros = (value)=>{
    const baseUrl = window.location.origin + '/catalogo/';
    const queryParams = `?page=1&sort=tituloLibro&q=${encodeURIComponent(value)}`;
    window.location.href = baseUrl + queryParams;
  }

  $('#buscador').keydown(function(event){
    if(event.keyCode === 13) { // 13 is the Enter key code
        event.preventDefault(); // Prevent the default action if needed
        filtradoLibros($('#buscador').val());
        $('#buscador').val('')        
    } 
  });

  $('#btnBuscador').click(function(){
    filtradoLibros($('#buscador').val());
    $('#buscador').val('')
  });
});