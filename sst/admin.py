from django.contrib import admin
from .models import Usuario, Perfil
from .models import RecursoSSTAdmin, RecursoSSTEmpleado
from .models import Rol, Permiso
from .forms import RolForm, PermisoForm
from django import forms

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'  # <- aquí va el nombre correcto del campo en Perfil

class UsuarioAdmin(admin.ModelAdmin):
    inlines = (PerfilInline,)
    list_display = (
        'first_name', 
        'last_name', 
        'cedula_display', 
        'email', 
        'rol_display',  
        'telefono_display', 
        'departamento_display', 
        'ciudad_display'
    )

    # Campos que aparecerán en el formulario del admin
    fields = ('first_name', 'last_name', 'email', 'rol', 'password', 'is_active', 'is_staff', 'is_superuser')

    def cedula_display(self, obj):
        return obj.perfil.cedula if hasattr(obj, 'perfil') else '-'
    cedula_display.short_description = 'Cédula'

    def rol_display(self, obj):
        return obj.rol.nombre if obj.rol else '-'
    rol_display.short_description = 'Rol'

    def telefono_display(self, obj):
        return obj.perfil.telefono if hasattr(obj, 'perfil') else '-'
    telefono_display.short_description = 'Teléfono'

    def departamento_display(self, obj):
        return obj.perfil.departamento if hasattr(obj, 'perfil') else '-'
    departamento_display.short_description = 'Departamento'

    def ciudad_display(self, obj):
        return obj.perfil.ciudad if hasattr(obj, 'perfil') else '-'
    ciudad_display.short_description = 'Ciudad'

admin.site.register(Usuario, UsuarioAdmin)
@admin.register(RecursoSSTAdmin)
class RecursoSSTAdminAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'fecha_subida')
    list_filter = ('tipo', 'fecha_subida')
    search_fields = ('titulo', 'descripcion')

@admin.register(RecursoSSTEmpleado)
class RecursoSSTEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('recurso', 'visible')
    list_filter = ('visible',)

class RolForm(forms.ModelForm):
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permiso.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Muestra todos los permisos como checkboxes
        required=False
    )

    class Meta:
        model = Rol
        fields = ['nombre', 'permisos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }