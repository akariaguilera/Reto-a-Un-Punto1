[app]
title = A Un Punto
package.name = aunpunto
package.domain = org.nextlevel
source.dir = .
source.include_exts = py,png,xlsx,csv,json
source.exclude_dirs = pruebas,herramientas,bin,docs
version = 1.0.0
requirements = python3,kivy==2.3.1,matplotlib,numpy,pillow,openpyxl,et_xmlfile,plyer
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/datos/icono.png
presplash.filename = %(source.dir)s/datos/presentacion.png
android.presplash_color = #141414
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 34
android.minapi = 24
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
