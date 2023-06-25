# Obligatorio Machine Learning en Producción

Este repositorio contiene el Scrapy que corre la Spider sobre la página de inmuebles para casas y apartamentos del Gallito. Para su ejecución, se puede ejecutar localmente con "scrapy crawl gallito", o hacer un build al docker y luego ejecutarlo con los siguientes comandos:

* docker build -t gallito:latest .  
* docker run --rm gallito:latest   

En el archivo "scrapy_logs.log" se registran todos los logs asociados a la Spider y la subida de datos a Azure.

Las imágenes son subidas a un container en Azure en un formato preestablecido donde se guardan con un ID único por imagen, un ID único por propiedad, qué tipo de propiedad es, casa o apartamento, el número de dormitorios y los metros cuadrados.Para confirmar que el container está vacío para poder tener solamente dentro los datos que se quieren, se ejecuta el siguiente comando para borrar todo contenido  dentro colocando el ID del container correspondiente: 

* az storage blob delete-batch --account-name <CONTAINER> --source container-m

El documento "model_obligatorio.ipynb" en la Notebook donde se hace el tratamiento de datos, visualización de los mismos, la creación del modelo, la utilización de diferentes técnicas y registros del entrenamiento mediante herramientas. 

