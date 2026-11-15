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
pytest --ignore=tests/test_acceptance_app.py --ignore=tests/test_smoke_app.py --cov-fail-under=80
python -m app.app
```

Para Docker se mantienen las instrucciones del `Dockerfile` y el puerto 8000.
La clave de sesión puede configurarse con `SECRET_KEY`; si no se proporciona,
se genera al arrancar. Gunicorn usa `--preload` para compartirla entre workers.

## Estado del taller

El proyecto SonarCloud es `quinnie9_cicd-pipeline-python-cd`. La carpeta `infra/`
contiene la configuración del enunciado, validada con Terraform 1.17.1, y el
lock del proveedor AWS. El backend usa el bucket
`tfstate-calculadora-quinnie9-20261115`, ya creado con versionado en AWS Academy.

El despliegue manual de Staging se verificó con dos pruebas de humo y el target
del balanceador en estado `healthy`:

http://calculadora-staging-alb-690024253.us-east-1.elb.amazonaws.com

El workflow `ci-cd.yml` encadena `build-and-test`, `deploy-staging`,
`test-staging`, `deploy-production` y `smoke-test-production`. Las pruebas y el
workflow se publican juntos para excluir las pruebas de humo de las unitarias.
Los secretos y variables están configurados; las credenciales de AWS Academy
deben renovarse cuando expire la sesión.

La [ejecución completa](https://github.com/quinnie9/cicd-pipeline-python-cd/actions/runs/43741383852)
terminó con los cinco jobs aprobados, seis pruebas de aceptación en Staging y
dos pruebas de humo en Producción. SonarCloud confirmó el Quality Gate aprobado
y cobertura del 100%.

Producción: http://calculadora-production-alb-1605318996.us-east-1.elb.amazonaws.com

Los dos ambientes responden en `/health` con `status=ok` y la versión desplegada
`6a51a819f1ec40955ddb3d0247c076486c9ca8b2`. Los cambios posteriores que solo
modifican documentación no generan otro despliegue.

Chrome bloqueaba el HTTP externo del ALB en las pruebas de aceptación. Se
reprodujo el error `ERR_BLOCKED_BY_CLIENT` y se ajustó el navegador temporal de
pruebas para el HTTP definido en el taller.

La fase individual llega hasta la sección 7.9. La protección de `main` y la
aprobación manual de Producción se configuran en el repositorio elegido por el
equipo, en las secciones 7.10 y 7.11.

Las evidencias, URLs de los ambientes y respuestas del Taller 3 se agregarán
según la sección 9 del enunciado.
