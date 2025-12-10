from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Campaña, Encuesta, Feedback, CodigoCampaña, CampanaAsignada  
from .models import Grupo
from .models import Notificacion
from .models import Usuario, Perfil, EvidenciaCampaña
from .models import RecursoSSTAdmin, RecursoSSTEmpleado
from .models import Mensaje
from .models import Rol, Permiso 




Usuario = get_user_model()

# Ciudades organizadas por departamento
CIUDADES_POR_DEPARTAMENTO = {
    'Cundinamarca': ['Girardot', 'Soacha', 'Fusagasugá', 'Zipaquirá', 'Ricaurte'],
    'Antioquia': ['Medellín', 'Envigado', 'Bello', 'Itagüí'],
    'Valle del Cauca': ['Cali', 'Palmira', 'Buenaventura', 'Tuluá'],
    'Bogotá': ['Bogotá'],
}

DEPARTAMENTOS = [('', 'Seleccione un departamento')] + [(dep, dep) for dep in CIUDADES_POR_DEPARTAMENTO.keys()]
TODAS_CIUDADES = [('', 'Seleccione una ciudad')] + [(ciudad, ciudad) for ciudades in CIUDADES_POR_DEPARTAMENTO.values() for ciudad in ciudades]

# -----------------------
# Registro de Usuario
# -----------------------

class RegistroUsuarioForm(UserCreationForm):
    cedula = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Cédula' }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'}))
    departamento = forms.ChoiceField(choices=DEPARTAMENTOS, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_departamento'}))
    ciudad = forms.ChoiceField(choices=TODAS_CIUDADES, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_ciudad', 'disabled': 'disabled'}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña',
        'autocomplete': 'new-password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirmar contraseña',
        'autocomplete': 'new-password'
    }))
    terminos = forms.BooleanField(required=True)

    class Meta:
        model = Usuario
        fields = [
            'cedula', 'first_name', 'last_name', 'telefono',
            'departamento', 'ciudad', 'direccion',
            'email', 'password1', 'password2'
        ]

# -----------------------
# Crear Usuario Admin
# -----------------------

class AdminCrearUsuarioForm(UserCreationForm):
    cedula = forms.CharField(label='Cédula', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Apellidos', widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label='Celular', widget=forms.TextInput(attrs={'class': 'form-control'}))
    departamento = forms.ChoiceField(label='Departamento', choices=DEPARTAMENTOS,
                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_departamento'}))
    ciudad = forms.ChoiceField(label='Ciudad', choices=TODAS_CIUDADES,
                               widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_ciudad'}))
    direccion = forms.CharField(label='Dirección', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Correo', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    rol = forms.ModelChoiceField(
        label='Rol',
        queryset=Rol.objects.none(),  # inicialmente vacío
        empty_label="Seleccione un rol",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ['cedula', 'first_name', 'last_name', 'telefono', 'departamento',
                  'ciudad', 'direccion', 'email', 'rol', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar dinámicamente todos los roles
        self.fields['rol'].queryset = Rol.objects.all()

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data['email']
        usuario.cedula = self.cleaned_data['cedula']
        usuario.rol = self.cleaned_data['rol']

        if commit:
            usuario.save()
            perfil, created = Perfil.objects.get_or_create(user=usuario)
            perfil.telefono = self.cleaned_data['telefono']
            perfil.departamento = self.cleaned_data['departamento']
            perfil.ciudad = self.cleaned_data['ciudad']
            perfil.direccion = self.cleaned_data['direccion']
            perfil.save()

        return usuario
    
# -----------------------
# Editar Usuario Admin
# -----------------------
class AdminEditarUsuarioForm(forms.ModelForm):
    telefono = forms.CharField(required=False)
    direccion = forms.CharField(required=False)   
    departamento = forms.CharField(required=False)
    ciudad = forms.CharField(required=False)
    cedula = forms.CharField(required=False)
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=False, empty_label="Seleccione un rol")

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'rol', 'telefono', 'departamento', 'ciudad', 'direccion', 'cedula']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            perfil = getattr(self.instance, 'perfil', None)
            self.fields['telefono'].initial = perfil.telefono if perfil else ''
            self.fields['departamento'].initial = perfil.departamento if perfil else ''
            self.fields['ciudad'].initial = perfil.ciudad if perfil else ''
            self.fields['cedula'].initial = self.instance.cedula
            self.fields['direccion'].initial = self.instance.direccion
            self.fields['rol'].initial = self.instance.rol

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.direccion = self.cleaned_data['direccion']
        usuario.rol = self.cleaned_data['rol']
        if commit:
            usuario.save()
        perfil, created = Perfil.objects.get_or_create(user=usuario)
        perfil.telefono = self.cleaned_data['telefono']
        perfil.departamento = self.cleaned_data['departamento']
        perfil.ciudad = self.cleaned_data['ciudad']
        perfil.save()
        return usuario
    
#-------------------------
#EDITAR PERFIL EMPLEADO
#-------------------------

class EditarEmpleadoForm(forms.ModelForm):
    telefono = forms.CharField(required=False)
    direccion = forms.CharField(required=False)
    departamento = forms.CharField(required=False)
    ciudad = forms.CharField(required=False)

    class Meta:
        model = Usuario
        fields = ['email', 'direccion', 'telefono', 'departamento', 'ciudad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        perfil = getattr(self.instance, 'perfil', None)
        if perfil:
            self.fields['telefono'].initial = perfil.telefono
            self.fields['departamento'].initial = perfil.departamento
            self.fields['ciudad'].initial = perfil.ciudad
            self.fields['direccion'].initial = self.instance.direccion

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if commit:
            usuario.save()
        perfil, created = Perfil.objects.get_or_create(user=usuario)
        perfil.telefono = self.cleaned_data['telefono']
        perfil.departamento = self.cleaned_data['departamento']
        perfil.ciudad = self.cleaned_data['ciudad']
        perfil.save()
        return usuario
# -----------------------
# Campaña
# -----------------------
class CampañaForm(forms.ModelForm):
    codigo = forms.ModelChoiceField(
        queryset=CodigoCampaña.objects.all(),
        empty_label="Seleccione un código",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Código"
    )

    empleado = forms.ModelChoiceField(
        queryset=Usuario.objects.none(),  # Inicialmente vacío; se llenará en __init__
        empty_label="Seleccione un empleado",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label="Asignar a empleado"
    )

    grupos = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        empty_label="Seleccione un grupo",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label="Asignar a grupo"
    )

    periodicidad = forms.ChoiceField(
        choices=[
            ('', 'Seleccione un periodo'),
            ('Diaria', 'Diaria'),
            ('Semanal', 'Semanal'),
            ('Mensual', 'Mensual'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Periodicidad'
    )

    class Meta:
        model = Campaña
        fields = [
            'codigo', 'detalle', 'estado', 'periodicidad',
            'multimedia', 'empleado', 'grupos', 'evidencia_requerida',
        ]
        widgets = {
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'multimedia': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'evidencia_requerida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Queryset dinámico: solo usuarios activos con rol 'Empleado'
        self.fields['empleado'].queryset = Usuario.objects.filter(
            rol__nombre__iexact='Empleado',
            is_active=True
        )
        self.fields['empleado'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

        # Etiqueta para códigos
        self.fields['codigo'].label_from_instance = lambda obj: f"{obj.codigo} - {obj.nombre}"

        # Ajustar estados
        ESTADOS = [('', 'Seleccione un estado')] + list(self.fields['estado'].choices[1:])
        self.fields['estado'].choices = ESTADOS

    def clean(self):
        cleaned_data = super().clean()
        empleado = cleaned_data.get('empleado')
        grupo = cleaned_data.get('grupos')

        # Validación: solo un empleado o un grupo, no ambos
        if empleado and grupo:
            raise forms.ValidationError("Debe seleccionar un empleado o un grupo, no ambos.")
        if not empleado and not grupo:
            raise forms.ValidationError("Debe seleccionar un empleado o un grupo.")
        return cleaned_data
# -----------------------
# Campaña Asignada
# -----------------------

class CampanaAsignadaForm(forms.ModelForm):  
    class Meta:
        model = CampanaAsignada  
        fields = ['campaña', 'empleado']
        widgets = {
            'campaña': forms.Select(attrs={'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
        }

# -----------------------
# Código Campaña
# -----------------------

class CodigoCampañaForm(forms.ModelForm):
    class Meta:
        model = CodigoCampaña
        fields = ['codigo', 'nombre']


#grupos
class GrupoForm(forms.ModelForm):
    usuarios = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False, 
        label="Asignar usuarios al grupo"
    )

    class Meta:
        model = Grupo
        fields = ['nombre', 'descripcion', 'usuarios']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
       
        if not cleaned_data.get('nombre'):
            self.add_error('nombre', 'Este campo es obligatorio.')
        if not cleaned_data.get('descripcion'):
            self.add_error('descripcion', 'Este campo es obligatorio.')
        return cleaned_data
#----------------------------------------------------#
class NotificacionForm(forms.ModelForm):
    campaña = forms.ModelChoiceField(
        queryset=Campaña.objects.all(),
        empty_label="Seleccione una campaña",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_campaña'})
    )
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(is_active=True, rol__nombre="empleado"),
        empty_label="Seleccione un usuario",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_usuario'})
)

    class Meta:
        model = Notificacion
        fields = ['campaña', 'usuario', 'cedula', 'titulo', 'mensaje', 'tipo']
        widgets = {
            'cedula': forms.TextInput(attrs={'readonly': 'readonly', 'id': 'id_cedula'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        usuario = getattr(getattr(self, 'instance', None), 'usuario', None)
        if usuario:
            self.fields['cedula'].initial = usuario.cedula

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.usuario:
            instance.cedula = instance.usuario.cedula
        if commit:
            instance.save()
        return instance

class EditarUsuarioForm(forms.ModelForm):
    telefono = forms.CharField(required=False)
    departamento = forms.CharField(required=False)
    ciudad = forms.CharField(required=False)
    direccion = forms.CharField(required=False)
    cedula = forms.CharField(required=False)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Dejar en blanco si no desea cambiar'}),
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email']  # SOLO campos del usuario

    def __init__(self, *args, **kwargs):
        perfil = kwargs.pop('perfil', None)
        super().__init__(*args, **kwargs)

        # inicializar datos del perfil
        if perfil:
            self.fields['telefono'].initial = perfil.telefono
            self.fields['departamento'].initial = perfil.departamento
            self.fields['ciudad'].initial = perfil.ciudad
            self.fields['direccion'].initial = perfil.direccion
            self.fields['cedula'].initial = perfil.cedula

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        # Guardar perfil
        perfil = user.perfil
        perfil.telefono = self.cleaned_data.get('telefono')
        perfil.departamento = self.cleaned_data.get('departamento')
        perfil.ciudad = self.cleaned_data.get('ciudad')
        perfil.direccion = self.cleaned_data.get('direccion')
        perfil.cedula = self.cleaned_data.get('cedula')
        perfil.save()

        return user
    
#evidencia campaña
class RegistrarEvidenciaCampañaForm(forms.ModelForm):
    class Meta:
        model = EvidenciaCampaña
        fields = ['archivo']
        widgets = {
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class RecursoSSTAdminForm(forms.ModelForm):
    class Meta:
        model = RecursoSSTAdmin
        fields = ['titulo', 'archivo', 'tipo', 'descripcion']

class MensajeForm(forms.ModelForm):
    fecha_evento = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        ),
        label="Fecha y hora del evento"
    )

    class Meta:
        model = Mensaje
        fields = ['titulo', 'contenido', 'fecha_evento']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class RolForm(forms.ModelForm):
    # Permite seleccionar múltiples permisos para un rol
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permiso.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Rol
        fields = ['nombre', 'permisos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
        

class RolForm(forms.ModelForm):
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permiso.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Rol
        fields = ['nombre', 'permisos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del rol'}),
        }

class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# -----------------------
# Encuesta
# -----------------------

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['respuestas', 'evidencia']
        widgets = {
            'respuestas': forms.Textarea(attrs={'class': 'form-control'}),
            'evidencia': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# -----------------------
# Feedback
# -----------------------

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['calificacion', 'comentarios']
        widgets = {
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control'}),
        }