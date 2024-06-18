from django.db import models

# MOELOS

"""
Modelo para un libro
"""
class Libro(models.Model):
    tituloLibro = models.CharField(max_length = 100, null = False, blank = False)
    isbnLibro = models.CharField(max_length = 13, null = False, blank = False)
    resumenLibro = models.CharField(max_length = 500, null = True, blank = True)
    precioLibro = models.DecimalField(max_digits = 7,decimal_places = 2, null = False)
    stockLibro = models.IntegerField(null = False, blank = False, default = 0)
    descuento = models.DecimalField(max_digits = 3,decimal_places = 2, default = 0, null = True, 
                                    blank = True)
    portadalibro = models.ImageField(null = True, blank = True, upload_to='images/')
    editorial = models.ForeignKey('Editorial', on_delete = models.CASCADE, 
                                  related_name = 'librosPublicados', default = 0)

    def __str__(self):
        return self.tituloLibro

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        db_table = 'libro'
        ordering = ['tituloLibro']


"""
Modelo para autores de un libro, con una relacion muchos a muchos
"""
class Autor(models.Model):
    autor = models.CharField(max_length = 50, null = False, blank = False, default = "Sin Autor")
    libros = models.ManyToManyField(Libro, related_name = 'autores')

    def __str__(self):
        return f"Autor: {self.autor} - Libros: {self.libros}"
    
    # Personalización para el panel de administración de Django
    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        # Nombre personalizado para la BD
        db_table = 'autor'
        ordering = ['autor']


"""
Modelo para editoriales de los libros
"""
class Editorial(models.Model):
    editorial = models.CharField(max_length = 50, null = False, blank = False, 
                                 default= "Sin Editorial")

    def __str__(self):
        return self.editorial

    class Meta:
        verbose_name = 'Editorial'
        verbose_name_plural = 'Editoriales'
        db_table = 'editorial'
        ordering = ['editorial']


"""
Modelo para relacion intermedia entre transacciones y libros transaccionados
"""
class TransaccionInterLibro(models.Model):
    idTransaccion = models.ForeignKey('Transaccion', on_delete = models.CASCADE)
    idLibro = models.ForeignKey(Libro, on_delete = models.CASCADE)
    precio = models.DecimalField(max_digits = 7, decimal_places = 2, null = False)
    piezas = models.PositiveIntegerField(null = False, blank = False)

    def __str__(self):
        return f"Transaccion: {self.idTransaccion} - Libro: {self.idLibro}"

    # # Personalización para el panel de administración de Django
    class Meta:
        # Nombre personalizado para la BD
        db_table = 'transaccion_libro'
        # Se asegura que la combinacion de las FKs sea unica
        constraints = [
            models.UniqueConstraint(fields = ['idTransaccion', 'idLibro'], 
                                    name = 'unique_transaccion_libro')
        ]


"""
Modelo para transacciones
"""
class Transaccion(models.Model):
    tiempoTransaccion = models.DateTimeField(auto_now_add = True, unique = True)
    totalTransaccion = models.DecimalField(max_digits = 10,decimal_places = 2, null = False)
    libros = models.ManyToManyField(Libro, through = TransaccionInterLibro)
    tipoTransaccion = models.ForeignKey('TipoTransaccion', on_delete = models.DO_NOTHING, 
                                        default = 0)
    empleado = models.ForeignKey('Empleado', on_delete = models.DO_NOTHING, default = 0)
    cliente = models.ForeignKey('Cliente', on_delete = models.DO_NOTHING, default = 0) 

    def __str__(self):
        return f"Fecha y hora: {self.tiempoTransaccion} - Total: {self.totalTransaccion}"

    # Personalización para el panel de administración de Django
    class Meta:
        verbose_name = 'Transaccion'
        verbose_name_plural = 'Transacciones'
        # Nombre personalizado para la BD
        db_table = 'transaccion'
        ordering = ['tiempoTransaccion']


"""
Modelo para tipo de transacciones
"""
class TipoTransaccion(models.Model):
    tipoTransaccion = models.CharField(max_length = 3, null = False, blank = False, unique = True)
    
    def __str__(self):
        return self.tipoTransaccion
    
    # Personalización para el panel de administración de Django
    class Meta:
        verbose_name = 'Tipo de Transaccion'
        verbose_name_plural = 'Tipo de Transacciones'
        # Nombre personalizado para la BD
        db_table = 'tipoTransaccion'
        ordering = ['tipoTransaccion']


"""
Modelo para un empleado de tienda 
"""
class Empleado(models.Model):
    nombresEmpleado = models.CharField(max_length = 50, null = False)
    apellidoPaternoEmpleado = models.CharField(max_length = 50, null = False)
    apellidoMaternoEmpleado = models.CharField(max_length = 50, blank = True, null = True)
    usuarioEmpleado = models.CharField(max_length = 9, null = False)
    contraseniaEmpleado = models.CharField(max_length = 128, null = False)
    turnoEmpleado = models.CharField(max_length = 1, null = False)
    estatusEmpleado = models.CharField(max_length = 1, null = False)

    def __str__(self):
        return f"{self.apellidoPaternoEmpleado} {self.apellidoMaternoEmpleado} {self.nombresEmpleado}"
    
    # Personalización para el panel de administración de Django
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        # Nombre personalizado para la BD
        db_table = 'empleado'
        ordering = ['apellidoPaternoEmpleado']


"""
Modelo para corte de caja
"""
class CorteCaja(models.Model):
    tiempoCorte = models.DateTimeField(auto_now_add = True, unique = True)
    empleados = models.ForeignKey(Empleado, default = 0, on_delete = models.DO_NOTHING)

    def __str__(self):
        return str(self.tiempoCorte)
    
    class Meta:
        verbose_name = 'Corte de Caja'
        verbose_name_plural = 'Cortes de Caja'
        # Nombre personalizado para la BD
        db_table = 'corteCaja'
        ordering = ['tiempoCorte']


"""
Modelo para tipo de empleado
"""
class TipoEmpleado(models.Model):
    descripcionTipoEmpleado = models.CharField(max_length = 20, null = False, unique = True)
    empleados = models.ManyToManyField(Empleado, related_name = 'tipoEmpleados')

    def __str__(self):
        return self.descripcionTipoEmpleado

    # Personalización para el panel de administración de Django
    class Meta:
        # Nombre personalizado para la BD
        db_table = 'tipoEmpleado'
        ordering = ['descripcionTipoEmpleado']


"""
Modelo para cliente de la pagina web
"""
class Cliente(models.Model):
    nombresCliente = models.CharField(max_length = 50, null = False, blank = False)
    apellidoPaternoCliente = models.CharField(max_length = 50, null = False, blank = False)
    apellidoMaternoCliente = models.CharField(max_length = 50, blank = True, null = True)
    emailCliente = models.CharField(max_length = 9, null = False)
    contraseniaCliente = models.CharField(max_length = 128, null = False)
    estatusCliente = models.CharField(max_length = 1, null = False)
    esVerificadoCliente = models.BooleanField(null = False, default = False)

    def __str__(self):
        return f"{self.apellidoPaternoCliente} {self.apellidoMaternoCliente} {self.nombresCliente}"
    
    # Personalización para el panel de administración de Django
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        # Nombre personalizado para la BD
        db_table = 'cliente'
        ordering = ['apellidoPaternoCliente']


"""
Modelo para el domicilio de un cliente
"""
class Domicilio(models.Model):
    calleDomicilio = models.CharField(max_length = 50, null = False)
    numeroExteriorDomicilio = models.CharField(max_length = 10, null = False, default = "s/n")
    codigoPostalDomicilio = models.CharField(max_length = 5, blank = False, null = False)
    coloniaDomicilio = models.CharField(max_length = 50, null = False)
    municipioDomicilio = models.CharField(max_length = 50, null = False, default = 0)
    estadoDomicilio = models.CharField(max_length = 50, null = False, default = 0)
    cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE, default = 0,
                                related_name = 'domicilio')

    def __str__(self):
        return f"{self.calleDomicilio}, Num: {self.numeroExteriorDomicilio}, {self.codigoPostalDomicilio}"
    
    # Personalización para el panel de administración de Django
    class Meta:
        verbose_name = 'Domicilio'
        verbose_name_plural = 'Domicilios'
        # Nombre personalizado para la BD
        db_table = 'domicilio'
        ordering = ['codigoPostalDomicilio']


"""
Orden de comandos para la base de datos usando el ORM:
    1. python manage.py check 'NOMBRE_DE_LA_APP' (verifica que este todo bien con la aplicacion)
    2. python manage.py migrate (crea la bd)
    3. python manage.py makemigratios (crea el modelo especifiacdo en Aplicaciones/Aplicacion
        /models.py
        y lo especifica en el archivo Aplicaciones/Aplicacion/migrations/####_initial.py)
    4. python manage.py sqlmigrate 'NOMBRE_DE_LA_APP' '0001 o 0002 o 003 etc' 
        (muestra en consola el scrip SQL de para la creación de la tabla del modelo)
    5. python manage.py migrate
"""