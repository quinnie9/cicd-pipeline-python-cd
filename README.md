# Taller 3: Despliegue continuo con AWS ECS y Terraform

## Integrantes

Quinnie Villarreal | Lina Ballesteros | Alejandro Rios

| Nombre completo | Usuario de GitHub | Rol en este repositorio individual |
| --- | --- | --- |
| Quinnie Villarreal | quinnie9 | Propietaria |
| Lina Ballesteros | linaballesteros | Integrante |
| Alejandro Rios | alejoriosm04 | Integrante |

## Aplicación

Calculadora Flask que parte del repositorio individual del Taller 2. Conserva
las cuatro operaciones, la protección CSRF y las dependencias verificadas por
hash. La imagen ejecuta Gunicorn como un usuario sin privilegios.

`GET /health` devuelve `{"status": "ok", "version": "local"}` al ejecutar sin
`APP_VERSION`. En AWS, Terraform configurará esa variable con el SHA del commit.

## Preparación local

Con Python 3.13 y el entorno virtual activado:

```bash
python -m pip install --only-binary=:all: --require-hashes -r requirements-dev.lock
black app --check
pytest --ignore=tests/test_acceptance_app.py --cov-fail-under=80
python -m app.app
```

Para Docker se mantienen las instrucciones del `Dockerfile` y el puerto 8000.
La clave de sesión puede configurarse con `SECRET_KEY`; si no se proporciona,
se genera al arrancar. Gunicorn usa `--preload` para compartirla entre workers.

## Estado del taller

El proyecto SonarCloud es `quinnie9_cicd-pipeline-python-cd`. La carpeta `infra/`
contiene la configuración del enunciado, validada con Terraform 1.17.1, y el
lock del proveedor AWS. El backend usa el bucket
`tfstate-calculadora-quinnie9-20261115`; ese bucket todavía debe crearse en la
cuenta de AWS Academy antes del primer despliegue.

Pendiente: configurar los secretos y variables de GitHub Actions y las
credenciales temporales de AWS Academy. Staging y Producción todavía no están
desplegados. El workflow actual valida y publica la imagen; se ampliará a CD
en la sección 7.7, después de comprobar el despliegue manual de Staging.

Las evidencias, URLs de los ambientes y respuestas del Taller 3 se agregarán
según la sección 9 del enunciado.
