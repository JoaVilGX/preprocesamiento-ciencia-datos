# Documentación del proyecto de preprocesamiento

Nombres: Joaquin Villacreses Moreno
Fecha: 10/05/2026
Carrera: Ciencia de Datos
Periodo académico: 2026-1S
Semestre: Tercero "A"

## Introducción
**Objetivo:** Aplicar Git, GitHub y Pandas para gestionar versiones y preprocesar datasets.
**Funcialidades implementadas:**
- Manejo de valores nulos (media, mediana, eliminación)
- Normalización Min-Max
- Codificación one-hot / label
- Eliminación de duplicados

## Comandos Git usados
| Comando | Propósito |
|---------|------------|
| `git config --global user.name` | Configurar nombre de usuario |
| `git config --global user.email` | Configurar correo |
| `git checkout -b` | Crear y cambiar a nueva rama |
| `git add` | Agregar cambios al área de staging |
| `git commit -m` | Confirmar cambios localmente |
| `git push` | Subir cambios a GitHub |
| `git pull` | Traer cambios remotos |
| `git branch -d` | Eliminar rama local |

## Automatización con GitHub Actions
Se creó un workflow (`.github/workflows/preprocesamiento.yml`) que:
- Se ejecuta en cada `push` o `pull request` hacia `main`
- Instala pandas, numpy y scikit-learn
- Corre el script `preprocesamiento.py` para verificar que no haya errores

## Capturas de pantalla

### 1. Comandos iniciales y primer push
![Comandos iniciales](./capturas/Captura1_comandos_iniciales.png)

### 2. Creación de rama y push del script
![Rama feature-preprocesamiento](./capturas/Captura2_creacion_rama_y_push.png)

### 3. Pull request creado en GitHub
![Pull request](./capturas/Captura3_pull_request_creado.png)

### 4. Fusión (merge) exitosa
![Merge exitoso](./capturas/Captura4_merge_exitoso.png)

### 5. Sincronización de main local
![Sincronización](./capturas/Captura5_sincronizacion_main.png)

### 6. Workflow de Actions exitoso (lista)
![Workflow exitoso lista](./capturas/Captura6_workflow_exitoso_lista.png)

### 7. Detalle del job en Actions
![Detalle del job](./capturas/Captura7_detalle_job.png)

## Enlace Repositorio
https://github.com/JoaVilGX/preprocesamiento-ciencia-datos