# Procedimiento para actualizar el repositorio en GitHub

Repositorio objetivo:

```text
https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal
```

Este documento explica cómo subir cambios desde tu computadora al repositorio de GitHub, verificando antes que estás trabajando en la carpeta correcta y validando al final que todo quedó subido correctamente.

## 1. Abrir la terminal en la carpeta correcta

Primero abrí una terminal en la carpeta local del proyecto.

En este caso, la carpeta esperada es:

```powershell
C:\Proyectos\integrador_carrera
```

Para verificar dónde estás parada, ejecutá:

```powershell
Get-Location
```

El resultado debería mostrar:

```text
C:\Proyectos\integrador_carrera
```

Si no estás en esa carpeta, entrá con:

```powershell
cd C:\Proyectos\integrador_carrera
```

## 2. Verificar que la carpeta es un repositorio Git

Ejecutá:

```powershell
git status
```

Si todo está bien, Git va a mostrar información sobre la rama actual y los archivos modificados.

Si aparece un error como:

```text
fatal: not a git repository
```

significa que no estás dentro de la carpeta correcta del proyecto.

## 3. Verificar que el repositorio remoto es el correcto

Antes de subir cambios, confirmá que tu proyecto local está conectado al repositorio correcto de GitHub:

```powershell
git remote -v
```

Deberías ver algo parecido a:

```text
origin  https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal.git (fetch)
origin  https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal.git (push)
```

La parte importante es que el remoto `origin` apunte a:

```text
https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal.git
```

Si apunta a otro repositorio, no hagas `push` todavía.

## 4. Verificar la rama donde estás trabajando

Ejecutá:

```powershell
git branch --show-current
```

En este proyecto, la rama actual esperada es:

```text
main
```

Si aparece otra rama, revisá si realmente querés subir los cambios desde esa rama.

## 5. Ver qué archivos cambiaron

Ejecutá:

```powershell
git status --short
```

Git puede mostrar archivos con letras al inicio:

```text
 M archivo_modificado.md
 D archivo_eliminado.ipynb
?? archivo_nuevo.md
```

Significado:

- `M`: archivo modificado.
- `D`: archivo eliminado.
- `??`: archivo nuevo que Git todavía no está siguiendo.

Este paso es muy importante porque te permite confirmar qué información vas a subir.

## 6. Verificar que los archivos nuevos están en la carpeta correcta

Si querés subir documentación creada en `extras`, verificá que los archivos estén realmente ahí:

```powershell
Get-ChildItem extras
```

Deberías ver archivos como:

```text
00_configuracion_entorno_explicacion.md
01_creador_datos_sinteticos_explicacion.md
02_EDA_nivel_1_explicacion.md
03_EDA_nivel_2_explicacion.md
procedimiento_actualizar_repositorio_github.md
```

También podés verificar un archivo puntual:

```powershell
Test-Path extras\procedimiento_actualizar_repositorio_github.md
```

Si devuelve:

```text
True
```

el archivo existe en la carpeta correcta.

## 7. Revisar el contenido antes de subirlo

Antes de agregar archivos al commit, podés abrirlos desde el explorador, VS Code o verlos desde terminal:

```powershell
Get-Content extras\procedimiento_actualizar_repositorio_github.md -TotalCount 20
```

Esto muestra las primeras líneas del archivo y ayuda a confirmar que no estás subiendo un archivo vacío o equivocado.

## 8. Agregar al commit solo los archivos que querés subir

Si querés subir solamente la documentación de la carpeta `extras`, usá:

```powershell
git add extras
```

Esto agrega todos los archivos nuevos o modificados dentro de `extras`.

Si querés agregar un solo archivo, usá:

```powershell
git add extras\procedimiento_actualizar_repositorio_github.md
```

Evitá usar `git add .` si no estás completamente segura de querer subir todos los cambios del proyecto, porque puede incluir notebooks, datos, eliminaciones u otros archivos modificados.

## 9. Verificar qué quedó preparado para el commit

Ejecutá:

```powershell
git status --short
```

Los archivos preparados para commit aparecen normalmente con letras en verde en muchas terminales, o con estado `A`, `M` o `D` al inicio.

Para revisar con más detalle qué se va a guardar en el commit:

```powershell
git diff --cached --stat
```

Este comando muestra un resumen de los archivos agregados al commit.

Si agregaste algo por error, podés sacarlo del área de commit sin borrar el archivo:

```powershell
git restore --staged ruta\del\archivo
```

Ejemplo:

```powershell
git restore --staged README.md
```

## 10. Crear el commit

Cuando ya verificaste que está todo correcto, creá el commit:

```powershell
git commit -m "Actualización del EDA Nivel 1 y Nivel 2. Creación de archivos informativos en la carpeta extras"
```

El mensaje debe resumir qué cambio estás subiendo.

Otros ejemplos de mensajes válidos:

```powershell
git commit -m "Documentar notebooks del proyecto"
git commit -m "Agregar procedimiento para actualizar repositorio"
```

## 11. Subir los cambios a GitHub

Como la rama local es `main`, subí con:

```powershell
git push origin main
```

Si GitHub te pide autenticación, seguí el flujo que te indique la terminal. En algunos casos puede pedir iniciar sesión o usar un token.

## 12. Validación final desde la terminal

Después del `push`, ejecutá:

```powershell
git status
```

El resultado ideal es algo como:

```text
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

Esto significa que no quedaron cambios locales pendientes y que tu rama local está sincronizada con GitHub.

Si todavía aparecen archivos modificados, no siempre significa que el `push` falló. Puede significar que tenías otros cambios locales que no agregaste al commit. Revisalos con:

```powershell
git status --short
```

## 13. Validación final desde GitHub

Entrá al repositorio:

```text
https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal
```

Luego verificá:

1. Que estás en la rama `main`.
2. Que aparece el último commit con el mensaje que escribiste.
3. Que existe la carpeta `extras`.
4. Que dentro de `extras` están los archivos que subiste.
5. Que podés abrir los archivos `.md` y leer el contenido correctamente.

## 14. Validación opcional comparando local contra remoto

Para confirmar desde terminal que tu rama local no tiene commits pendientes de subir, ejecutá:

```powershell
git log --oneline origin/main..main
```

Si no muestra nada, significa que no hay commits locales pendientes de subir.

También podés verificar si GitHub tiene cambios que vos todavía no descargaste:

```powershell
git fetch origin
git status
```

Si aparece que tu rama está actualizada con `origin/main`, está todo correcto.

## Resumen rápido de comandos

```powershell
cd C:\Proyectos\integrador_carrera
Get-Location
git status
git remote -v
git branch --show-current
git status --short
Get-ChildItem extras
git add extras
git status --short
git diff --cached --stat
git commit -m "Agregar documentacion explicativa en extras"
git push origin main
git status
```

## Recomendación importante

Antes de ejecutar `git add .`, revisá muy bien el resultado de:

```powershell
git status --short
```

En este proyecto puede haber cambios en notebooks, datos, README u otros archivos. Si tu intención es subir solo documentación, lo más seguro es usar:

```powershell
git add extras
```

Así evitás subir cambios que todavía no querías publicar.
