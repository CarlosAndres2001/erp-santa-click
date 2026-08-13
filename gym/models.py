from datetime import timedelta, timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone
#================
# Modelo Rol
#================
class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fk_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)  # ← NUEVO
    class Meta:
        db_table = 'rol'

    def __str__(self):
        
        return self.nombre
    
# ========================================
# Modulo (NUEVO)
# ========================================
class Modulo(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100, unique=True)
    icono = models.CharField(max_length=50, blank=True)
    orden = models.IntegerField(default=0)
    modulo_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'modulo'
        ordering = ['orden', 'id']

    def __str__(self):
        return self.nombre
    
# ========================================
# PermisoRol (NUEVO)
# ========================================
class PermisoRol(models.Model):
    rol = models.ForeignKey('Rol', on_delete=models.CASCADE, related_name='permisos')
    modulo = models.ForeignKey('Modulo', on_delete=models.CASCADE, related_name='permisos_roles')
    
    puede_ver = models.BooleanField(default=False)
    puede_crear = models.BooleanField(default=False)
    puede_editar = models.BooleanField(default=False)
    puede_eliminar = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'permiso_rol'
        unique_together = ('rol', 'modulo')

    def __str__(self):
        return f"{self.rol.nombre} - {self.modulo.nombre}"

#================
# Modelo PlanEmpresa
#================
class PlanEmpresa(models.Model):
    nombre = models.CharField(max_length=100)
    dias_duracion = models.IntegerField(default=7)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'plan_empresa'

    def __str__(self):
        return self.nombre

#================
# Modelo Empresa
#================
class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100, blank=True)
    color_primario = models.CharField(max_length=7, blank=True)
    color_secundario = models.CharField(max_length=7, blank=True)
    color = models.CharField(max_length=50, blank=True)
    logo = models.URLField(max_length=500, blank=True)
    fecha_inicio_plan = models.DateTimeField(null=True, blank=True)
    fk_plan_empresa = models.ForeignKey(PlanEmpresa, on_delete=models.SET_NULL, null=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    TEMA_CHOICES = [('claro', 'Claro'), ('oscuro', 'Oscuro')]
    MONEDA_CHOICES = [('BOB', 'Boliviano'), ('GUY', 'Guaraní'), ('USD', 'Dólar'), ('ARS', 'Peso Argentino'), ('CLP', 'Peso Chileno')]
    tema = models.CharField(max_length=10, choices=TEMA_CHOICES, default='claro')
    moneda = models.CharField(max_length=5, choices=MONEDA_CHOICES, default='BOB')
    simbolo_moneda = models.CharField(max_length=5, default='Bs.')
    pie_ticket = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        db_table = 'empresa'

    def __str__(self):
        return self.nombre
# ---------- Vigencia del plan ----------

    @property
    def fecha_vencimiento_plan(self):
        """Fecha en que expira el plan actual, o None si no hay plan/fecha de inicio."""
        if not self.fecha_inicio_plan or not self.fk_plan_empresa:
            return None
        return self.fecha_inicio_plan + timedelta(days=self.fk_plan_empresa.dias_duracion)

    @property
    def dias_restantes(self):
        """Días que le quedan al plan. Negativo si ya venció. None si no aplica."""
        vencimiento = self.fecha_vencimiento_plan
        if not vencimiento:
            return None
        delta = vencimiento - timezone.now()
        return delta.days

    @property
    def plan_vigente(self):
        """
        True si la empresa puede operar: tiene plan asignado, plan activo (estado=True),
        empresa activa, y no se ha pasado la fecha de vencimiento.
        """
        if not self.estado:
            return False
        if not self.fk_plan_empresa or not self.fk_plan_empresa.estado:
            return False
        vencimiento = self.fecha_vencimiento_plan
        if not vencimiento:
            return False
        return timezone.now() <= vencimiento

    # ---------- Propietario ----------

    @property
    def propietario(self):
        """
        El usuario Administrador principal de la empresa (el que se creó
        junto con la empresa en registro_empresa).
        """
        return (
            Usuario.objects
            .filter(sucursal__fk_empresa=self, rol__nombre='Administrador')
            .order_by('id')
            .first()
        )
#================
# Modelo Sucursal
#================
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sucursal'

    def __str__(self):
        return self.nombre
    
# ========================================
# Usuario (reemplaza User de Django)
# ========================================
        
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
 
 
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # ← login real, único a nivel global
    username = models.CharField(max_length=50, blank=True, null=True)  # solo display, ya NO es único
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    rol = models.ForeignKey('Rol', on_delete=models.PROTECT)
    sucursal = models.ForeignKey('Sucursal', on_delete=models.PROTECT)  # obligatorio, ya no null=True
 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    # Reemplaza a is_logged_in: session_key real, validado contra la
    # tabla de sesiones de Django (no un booleano que nunca se apaga solo).
    session_key = models.CharField(max_length=40, blank=True, null=True)
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'rol', 'sucursal']
 
    objects = UsuarioManager()
 
    def __str__(self):
        return f"{self.nombre} {self.apellido or ''}".strip()
 
    @property
    def fk_empresa(self):
        """Atajo de solo lectura: la empresa siempre se saca de la sucursal."""
        return self.sucursal.fk_empresa if self.sucursal_id else None
 
    def tiene_permiso(self, codigo_modulo, accion='ver'):
        if self.rol.nombre.lower() == 'administrador':
            return True
        try:
            permiso = PermisoRol.objects.get(
                rol=self.rol,
                modulo__codigo=codigo_modulo,
                modulo__is_active=True
            )
            if accion == 'ver':
                return permiso.puede_ver
            elif accion == 'crear':
                return permiso.puede_crear
            elif accion == 'editar':
                return permiso.puede_editar
            elif accion == 'eliminar':
                return permiso.puede_eliminar
            return False
        except PermisoRol.DoesNotExist:
            return False
 
    def tiene_modulo(self, codigo_modulo):
        return self.tiene_permiso(codigo_modulo, 'ver')
 
    def tiene_permiso_menu(self, codigo):
        if self.rol.nombre.lower() == 'administrador':
            return True
        return PermisoRol.objects.filter(
            rol=self.rol,
            modulo__codigo=codigo,
            puede_ver=True
        ).exists()
 
    class Meta:
        db_table = 'usuario'
 
#=========================================
# Canal de Venta
#=========================================
class CanalVenta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.nombre  
    
    class Meta:
        db_table = 'canal_venta'
    
# ========================================
# Unidad de medida
# ========================================
class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'unidad_medida'

# ========================================
# Categoria
# ========================================
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)   

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        
#================
# Modelo Producto
#================
class TipoProducto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'tipo_producto'
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True)
    fk_tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.PROTECT, null=True)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)
    unidades_por_caja = models.PositiveIntegerField(default=0)  # ej: 12
    tara_por_caja = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # ej: 2.00 kg
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    visible_venta = models.BooleanField(default=True)
    visible_compra = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'producto'

    def __str__(self):
        return self.nombre

class ProductoVariante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variantes')
    nombre_variante = models.CharField(max_length=100, help_text="Ej: S / Negro o Chocolate")
    sku = models.CharField(max_length=50, unique=True, help_text="Código único para esta variante")
    codigo_barras = models.CharField(max_length=100, blank=True, null=True)
    precio_referencial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    foto = models.ImageField(upload_to='variantes/', null=True, blank=True)
    foto_url = models.URLField(max_length=500, blank=True, null=True)
    maneja_stock = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.nombre_variante}"

    class Meta:
        db_table = 'producto_variante' 
        
    @property
    def foto_display(self):
        """URL a usar en templates, priorizando el archivo subido sobre el link externo."""
        if self.foto:
            return self.foto.url
        if self.foto_url:
            return self.foto_url
        return None
    
class DetallePack(models.Model):
    producto_padre = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE, related_name='padre_packs')
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.PROTECT, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # costo interno del producto en el pack
    class Meta:
        db_table = 'detalle_pack'
    def __str__(self):
        nombre_item = ""
        if self.producto_variante:
            nombre_item = str(self.producto_variante)
        elif self.producto:
            nombre_item = self.producto.nombre
        else:
            nombre_item = "Sin definir"
            
        return f"{self.cantidad} x {nombre_item} en {self.producto_padre.nombre_variante}"

#========================================
# Receta y DetalleReceta
#========================================
class Receta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='recetas')
    nombre = models.CharField(max_length=100)  # opcional, o podés usar el nombre del producto
    is_active = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'receta'
        
class DetalleReceta(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='ingredientes')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    class Meta:
        db_table = 'detalle_receta'
        
# ========================================
# Precios de Producto
# ========================================
class PrecioProducto(models.Model):
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE, related_name='precios')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='precios')
    canal = models.ForeignKey(CanalVenta, on_delete=models.CASCADE, related_name='precios_producto')
    fecha = models.DateTimeField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'precio_producto'

    
#========================================
# Almacen
#========================================    
class Almacen(models.Model):
    nombre = models.CharField(max_length=100) # Ej: "Depósito", "Barra de Proteínas", "Vitrina"
    descripcion = models.TextField(blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='almacenes')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.sucursal.nombre})"
    
    class Meta:
        db_table = 'almacen'
        
#================
# Modelo Stock
#================
class Stock(models.Model):
    # Claves Foráneas  
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, related_name='inventario_stock')
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE, related_name='stock_inventario')
    # 2. CONTROL FÍSICO (Cantidad Disponible)
    cantidad_actual = models.DecimalField(max_digits=15, decimal_places=3, default=0, help_text="Cantidad total de unidades, kilos, o litros en stock.")
    cajas_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Cantidad total de cajas o bultos en stock.")
    peso_neto_total = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Peso neto total actual (unidades * peso_promedio_unidad).")
    # 3. CONTROL ECONÓMICO (Costo Promedio Ponderado - CPP)
    costo_unitario_promedio = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Costo promedio de adquisición por unidad (Se usa como CMV en egresos).")
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Valor monetario total del stock: cantidad_actual * costo_unitario_promedio.")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'stock'
        # Clave Única: Garantiza la integridad del stock (solo un registro por par)
        unique_together = ('almacen', 'producto_variante')
        verbose_name = 'Stock con Valoración (CPP)'
        verbose_name_plural = 'Inventario y Stock'

    def __str__(self):
        return f"Stock de   {self.producto_variante.nombre_variante} en {self.almacen.nombre}: {self.cantidad_actual} unidades"

#========================================
# Metodo de Pago
#========================================
class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    class Meta:
        db_table = 'metodo_pago'

    def __str__(self):
        
        return self.nombre

# ========================================
# TipoIngreso
# ========================================
class TipoIngreso(models.Model):
    nombre = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'tipo_ingreso'

# ========================================
# Ingreso de Productos y DetalleIngreso
# ========================================
class Ingreso(models.Model):
    tipo = models.ForeignKey(TipoIngreso, on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField()
    motivo_anulacion = models.TextField(blank=True, null=True)  # campo para motivo de anulación
    observaciones = models.TextField(blank=True, null=True)  # campo para observaciones 
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ingreso'

class DetalleIngreso(models.Model):
    ingreso = models.ForeignKey(Ingreso, on_delete=models.CASCADE)
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'detalle_ingreso'
# ========================================
# Turno
# ========================================
class Turno(models.Model):
    nombre = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'turno'
        
# ========================================
# Caja
# ======================================== 
class Caja(models.Model):
    nombre = models.CharField(max_length=50)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'caja'


# ========================================
# CajaTurno
# ========================================    
class CajaTurno(models.Model):

    ESTADOS = (
        ('ABIERTA', 'ABIERTA'),
        ('CERRADA', 'CERRADA'),
    )
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT)
    turno = models.ForeignKey(Turno, on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    cajachica_apertura = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observaciones_apertura = models.TextField(blank=True, null=True)
    monto_efectivo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monto_qr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monto_tarjeta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monto_online = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    monto_cierre = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_teorico = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    diferencia = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20,choices=ESTADOS, default='ABIERTA')
    fecha_apertura = models.DateTimeField()
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    observaciones_cierre = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'caja_turno'
        
# ========================================
# MovimientoCaja
# ========================================
class MovimientoCaja(models.Model):

    TIPOS = (
        ('APERTURA', 'Apertura'),
        ('VENTA', 'Venta'),
        ('INGRESO', 'Ingreso Monetario'),
        ('EGRESO', 'Egreso Monetario'),
        ('CIERRE', 'Cierre'),
    )

    caja_turno = models.ForeignKey(CajaTurno, on_delete=models.PROTECT, related_name='movimientos')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    monto = models.DecimalField(max_digits=12,decimal_places=2)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField( blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    created_at = models.DateTimeField( auto_now_add=True)

    class Meta:
        db_table = 'movimiento_caja'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.tipo} - {self.monto}'

# ========================================
# TipoEgreso
# ========================================
class TipoEgreso(models.Model):
    nombre = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'tipo_egreso'

# ========================================
# Egreso de Productos
# ========================================
class Egreso(models.Model):
    tipo = models.ForeignKey(TipoEgreso, on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    caja_turno = models.ForeignKey(CajaTurno, on_delete=models.PROTECT, related_name='egresos')
    motivo_anulacion = models.TextField(blank=True, null=True)  
    observaciones = models.TextField(blank=True, null=True) 
    class Meta:
        db_table = 'egreso'

# ========================================
# DetalleEgreso
# ========================================
class DetalleEgreso(models.Model):
    egreso = models.ForeignKey(Egreso, on_delete=models.CASCADE)
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'detalle_egreso'

# ========================================
# proveedor
# ========================================
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'proveedor'

#================
# Modelo Auditoria
#================
class Kardex(models.Model):
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    tipo_movimiento = models.CharField(max_length=20)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    referencia = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'kardex'
    def __str__(self):
        return f"Kardex #{self.id} - {self.tipo_movimiento}"

class UserLog(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    accion = models.CharField(max_length=50)  # creacion, edicion, eliminacion, etc.
    tabla = models.CharField(max_length=50)  # nombre de la tabla afectada
    registro_id = models.IntegerField()  # id del registro afectado
    descripcion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_log'
    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.tabla} #{self.registro_id}"

# ========================================
# Compra y DetalleCompra
# ========================================
class Compra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT, null=True,blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null=True, blank=True)
    motivo_anulacion = models.TextField(blank=True, null=True)  # campo para motivo de anulación
    observaciones = models.TextField(blank=True, null=True)  # campo para observaciones
    
    class Meta:
        db_table = 'compra'

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'detalle_compra'

#================
# Modelo Cliente
#================
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True)
    nro_documento = models.CharField(max_length=50, blank=True)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='clientes/', null=True, blank=True)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ========================================
# Venta y DetalleVenta
# ========================================
class Venta(models.Model):
    ESTADO_VENTA_CHOICES = [
         ('registrado',  'Registrado'),
         ('en_proceso', 'En Proceso'),
         ('despachado', 'Despachado'),
     ]
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    canal = models.ForeignKey(CanalVenta, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    direccion_entrega = models.TextField(blank=True, null=True)
    telefono_entrega = models.CharField(max_length=30, blank=True, null=True)
    fecha = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    caja_turno = models.ForeignKey(CajaTurno, on_delete=models.PROTECT, related_name='ventas')
    motivo_anulacion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True) 
    estado_venta = models.CharField(max_length=20, default='Registrado')  # pendiente, pagada, anulada
    class Meta:
        db_table = 'venta'

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto_variante = models.ForeignKey(ProductoVariante, null=True, blank=True, on_delete=models.PROTECT)
    producto_padre = models.ForeignKey(Producto, null=True, blank=True, on_delete=models.PROTECT)
    detalle_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='componentes')
    nombre_producto = models.CharField(max_length=150, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
            # 1. Validar que al menos uno esté presente
            if not self.producto_variante and not self.producto_padre:
                raise ValidationError('Debe existir una variante de producto o un producto padre (Pack).')

            # 2. Validar que NO estén los dos en la misma línea (a menos que sea un componente de pack)
            if self.producto_variante and self.producto_padre and not self.detalle_padre:
                raise ValidationError('Una línea de venta no puede ser producto y pack al mismo tiempo.')

    class Meta:
        db_table = 'detalle_venta'

# ========================================
# Pagos de la Venta (Multimetodo)
# ========================================
class PagoVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='pagos')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    referencia_pago = models.CharField(max_length=100, blank=True, null=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pago_venta'
        
# ========================================
# Traspaso y DetalleTraspaso
# ========================================
class Traspaso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    sucursal_origen = models.ForeignKey(Sucursal, on_delete=models.PROTECT, related_name='traspasos_origen')
    sucursal_destino = models.ForeignKey(Sucursal, on_delete=models.PROTECT, related_name='traspasos_destino')
    almacen_origen = models.ForeignKey(Almacen, on_delete=models.PROTECT, related_name='traspasos_almacen_origen')
    almacen_destino = models.ForeignKey(Almacen, on_delete=models.PROTECT, related_name='traspasos_almacen_destino')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    motivo_anulacion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'traspaso'

class DetalleTraspaso(models.Model):
    traspaso = models.ForeignKey(Traspaso, on_delete=models.CASCADE)
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'detalle_traspaso'

# ========================================
# EgresoMonetario
# ========================================
class EgresoMonetario(models.Model):
    fecha = models.DateTimeField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    motivo = models.ForeignKey(TipoEgreso, on_delete=models.PROTECT)
    observaciones = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    caja_turno = models.ForeignKey(CajaTurno, on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    motivo_anulacion = models.TextField(blank=True, null=True)  
    observaciones = models.TextField(blank=True, null=True) 
    class Meta:
        db_table = 'egreso_monetario'
          
# ========================================
# IngresoMonetario
# ========================================
class IngresoMonetario(models.Model):
    fecha = models.DateTimeField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    motivo = models.ForeignKey(TipoIngreso, on_delete=models.PROTECT)
    observaciones = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    caja_turno = models.ForeignKey(CajaTurno, on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    motivo_anulacion = models.TextField(blank=True, null=True)  
    observaciones = models.TextField(blank=True, null=True) 
    
    class Meta:
        db_table = 'ingreso_monetario'  
        
#================
# Modelo Plan
#================
class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    duracion_dias = models.PositiveIntegerField()
    tarifa = models.DecimalField(max_digits=10, decimal_places=2)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    permite_congelar = models.BooleanField(default=False)
    cantidad_dias_congelamiento = models.IntegerField(default=0)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'plan'

    def __str__(self):
        return self.nombre


#================
# Modelo Membresia
#================
class Membresia(models.Model):

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('activa', 'Activa'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]

    fk_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='membresias')
    fk_plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    dias_congelados = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    class Meta:
        db_table = 'membresia'

    def save(self, *args, **kwargs):
        if not self.fk_empresa:
            self.fk_empresa = self.fk_cliente.fk_empresa

        # solo calcular fechas si está activa
        if self.estado == 'activa' and self.fecha_inicio and not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(days=self.fk_plan.duracion_dias)

        super().save(*args, **kwargs)

    def esta_activa(self):
        hoy = timezone.now().date()
        return self.estado == 'activa' and self.fecha_fin and self.fecha_fin >= hoy

    def __str__(self):
        return f"{self.fk_cliente} - {self.fk_plan}"

#================
# Modelo Pago
#================
class Pago(models.Model):
    nombre_pagador = models.CharField(max_length=150, blank=True)
    fecha_hora_pago = models.DateTimeField()
    descripcion = models.TextField(blank=True)
    cantidad = models.PositiveIntegerField()
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    deuda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fk_metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    fk_membresia = models.ForeignKey(Membresia, on_delete=models.CASCADE, related_name='pagos')
    fk_usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fk_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pago'

    def __str__(self):
        return f"Pago #{self.id}"

#================================
# Modelo Asistencia
#================================
class Asistencia(models.Model):
    fecha_hora_entrada = models.DateTimeField(auto_now_add=True)
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)
    fk_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fk_membresia = models.ForeignKey(Membresia, on_delete=models.CASCADE)
    fk_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fk_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asistencia'

    def save(self, *args, **kwargs):

        if self.fk_membresia.estado != 'activa':
            raise ValueError("Membresía no activa")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Asistencia #{self.id} - {self.fk_cliente}"
