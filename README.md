# Airflow demo

__Autor:__ Kevin Alan Martínez Virgen 219294382

__Clase:__ Computación tolerante a fallas

### Introducción
Esta es una breve prueba de como utilizar airflow para automatizar y programar
un flujo de trabajo o en terminología de Airflow, un DAG. Un grafo que se 
compone de tareas y que puede monitorear el estado entre ellas

### Desarollo
Una vez instalado airflow mediante el comando 
```
pip install "apache-airflow[celery]==2.5.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.1/constraints-3.7.txt"
```

Ejecuté el comando 
`airflow standalone`
para iniciar el entorno visual y poder ejecutar el flujo de trabajo

El código no funcionó de inmediato por lo que tuve que relizar múltiples 
pruebas y después de un tiempo pude hacer que las tareas se ejecutaran correctamente

![calendar]
