# Guía paso a paso: Crear y actualizar el proyecto en GitHub

## Parte 1 — Configuración inicial (se hace una sola vez)

### Paso 1: Configurar tu identidad en Git

Abre una terminal y ejecuta:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "95697194@ifts24.edu.ar"
```

Verificar que quedó guardado:
```bash
git config --global --list
```

---

### Paso 2: Inicializar el repositorio local

Desde la carpeta del proyecto:

```bash
cd c:/Proyectos/integrador_carrera
git init
```

---

### Paso 3: Conectar con el repositorio remoto en GitHub

```bash
git remote add origin https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal.git
```

Verificar la conexión:
```bash
git remote -v
```

Debe mostrar:
```
origin  https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal.git (fetch)
origin  https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal.git (push)
```

---

### Paso 4: Primer commit y subida inicial

```bash
# Ver qué archivos hay para agregar
git status

# Agregar todos los archivos al área de preparación
git add .

# Crear el primer commit
git commit -m "feat: configuración inicial del proyecto de datos"

# Subir al repositorio remoto (primera vez)
git push -u origin main
```

> Si la rama se llama `master` en lugar de `main`, usá `git push -u origin master`.

---

## Parte 2 — Flujo de trabajo diario

Cada vez que trabajas en el proyecto seguís estos pasos:

### Paso 1: Antes de empezar — traer los últimos cambios

```bash
git pull origin main
```

Esto sincroniza tu copia local con lo que está en GitHub, evitando conflictos.

---

### Paso 2: Trabajar normalmente

Editás notebooks, agregás datos, modificás código. Sin hacer nada especial en git.

---

### Paso 3: Ver qué cambió

```bash
git status
```

Muestra archivos nuevos (en rojo) y modificados. Los archivos en `.gitignore` no aparecen.

---

### Paso 4: Preparar los cambios para el commit

```bash
# Agregar archivos específicos (recomendado)
git add notebooks/01_eda_olist.ipynb
git add src/limpieza.py

# O agregar todo lo que cambió
git add .
```

---

### Paso 5: Crear el commit con un mensaje descriptivo

```bash
git commit -m "tipo: descripción breve de lo que hiciste"
```

**Tipos de commits recomendados:**

| Tipo | Cuándo usarlo |
|---|---|
| `feat:` | Agrega nueva funcionalidad o análisis |
| `fix:` | Corrige un error |
| `data:` | Agrega o actualiza datasets |
| `docs:` | Modifica documentación o README |
| `refactor:` | Reorganiza código sin cambiar lo que hace |
| `viz:` | Agrega o mejora visualizaciones |

**Ejemplos:**
```bash
git commit -m "feat: análisis exploratorio del dataset Olist"
git commit -m "data: agregar dataset CACE fase 2"
git commit -m "viz: gráfico de distribución de ventas por región"
git commit -m "fix: corregir cálculo de tasa de conversión"
```

---

### Paso 6: Subir los cambios a GitHub

```bash
git push origin main
```

---

## Parte 3 — Comandos útiles del día a día

### Ver el historial de commits
```bash
git log --oneline
```

### Ver las diferencias antes de hacer commit
```bash
git diff
```

### Deshacer cambios en un archivo (antes del commit)
```bash
git restore nombre_del_archivo.py
```

### Ver en qué rama estás
```bash
git branch
```

### Crear una rama nueva para un análisis experimental
```bash
git checkout -b fase2-limpieza-datos
```

### Volver a la rama principal
```bash
git checkout main
```

### Fusionar una rama experimental con main
```bash
git checkout main
git merge fase2-limpieza-datos
```

---

## Parte 4 — Manejo de notebooks Jupyter en Git

Los notebooks `.ipynb` guardan outputs (gráficos, tablas) dentro del archivo, lo que genera diffs muy grandes. Buenas prácticas:

1. **Limpiar outputs antes de hacer commit**: en JupyterLab usá `Kernel > Restart & Clear Outputs` antes de guardar.

2. **Nombrar notebooks con numeración**: `01_exploracion.ipynb`, `02_limpieza.ipynb`, `03_analisis.ipynb`

3. **No subir datos grandes** al repo — el `.gitignore` ya está configurado para excluir CSVs pesados. Subí en su lugar una muestra pequeña o una descripción del dataset.

---

## Parte 5 — Solución de problemas frecuentes

### "rejected — non-fast-forward"
Significa que GitHub tiene cambios que no tenés local. Solución:
```bash
git pull origin main
# resolver conflictos si los hay
git push origin main
```

### "Please tell me who you are"
```bash
git config --global user.email "95697194@ifts24.edu.ar"
git config --global user.name "Tu Nombre"
```

### Subir un archivo que estaba en .gitignore
```bash
git add -f nombre_del_archivo.csv
git commit -m "data: agregar muestra del dataset"
```

### Ver qué está siendo ignorado por .gitignore
```bash
git status --ignored
```
