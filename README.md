## Descripción

**net-visualizer** es una herramienta diseñada para visualizar el estado de una red de manera sencilla y eficiente. Permite identificar los hosts reservados y disponibles dentro de una red y visualizar su distribución en un formato de fácil interpretación. Es ideal para administradores de redes que necesitan tener una vista rápida y clara del estado de su red.

## Características

- **Visualización de hosts:** Muestra los hosts reservados y disponibles en la red.
- **Detección de superposición:** Identifica subredes que se superponen o están fuera de la red principal.
- **Expansión de subredes:** Permite expandir subredes en formato corto a su forma completa.

## Instalación

Para utilizar **net-visualizer**, primero necesitas instalar Python y el paquete `colorama`:

1. **Instalar Python:** Puedes descargar Python desde [python.org](https://www.python.org/).
2. **Instalar colorama:** Ejecuta el siguiente comando en tu terminal:
```bash
   pip install colorama
```
## Uso
Para ejecutar net-visualizer, utiliza el siguiente comando:
```bash
python3 net-visualizer.py <red> <subred> <subred> ... [-v|--visualizer]
```
## Ejemplo
```bash
python3 net-visualizer.py 192.168.1.0/24 192.168.1.0/28 192.168.1.16/28 -v
```
### Parámetros
- `<red>`: La red principal en formato CIDR (ej. 192.168.1.0/24).
- `<subred>`: Una o más subredes dentro de la red principal.
- `-v | --visualizer`: (Opcional) Muestra una visualización gráfica de los hosts.

## Salida
### Sin visualización
Si no se utiliza el flag -v o --visualizer, la herramienta mostrará los segmentos reservados y disponibles:

![dIasXKK](https://github.com/user-attachments/assets/cbcb7074-1998-4fb1-91a8-248b2eb7ad15)

### Con visualización

<img width="797" alt="ezgif-1-d345af0e32" src="https://github.com/user-attachments/assets/a25a280e-39f0-4e8f-9eb6-2d3117ae555a">



