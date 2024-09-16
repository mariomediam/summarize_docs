from rest_framework import serializers
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

class UploadFilePDFSerializer(serializers.Serializer):
    # max_length => indica el maximo de caracteres en el nombre de un archivo
    # use_url => si es True, el valor de la url sera usado para mostrar la ubicacion del archivo. si es False entonces se usara el nombre del archivo  (False es su valor x defecto)
    archivo = serializers.FileField(max_length=200, use_url=True)
    location = serializers.CharField(max_length=200)
    file_name = serializers.CharField(max_length=200)


    def validate_archivo(self, value):
        """
        Valida que solo se puedan cargar archivos PDF
        """
        archivo: InMemoryUploadedFile = value

        if archivo.content_type != "application/pdf":
            raise serializers.ValidationError(
                "Solo se pueden cargar archivos en formato PDF"
            )

        # """
        # Valida tamaño máximo del archivo 10Mb
        # """
        # if archivo.size > 10485760:
        #     raise serializers.ValidationError("El tamaño máximo del archivo es de 10Mb")

        return value
    
    def save(self):
        archivo: InMemoryUploadedFile = self.validated_data.get("archivo")

        fs = FileSystemStorage(self.validated_data.get("location"))
        file = fs.save(self.validated_data.get("file_name"), archivo)
        fileurl = fs.generate_filename(file)
        return fileurl    
    

class UploadFileWordSerializer(serializers.Serializer)    :
    archivo = serializers.FileField(max_length=200, use_url=True)
    location = serializers.CharField(max_length=200)
    file_name = serializers.CharField(max_length=200)

    def validate_archivo(self, value):
        """
        Valida que solo se puedan cargar archivos Word
        """
        archivo: InMemoryUploadedFile = value

        if archivo.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            raise serializers.ValidationError(
                "Solo se pueden cargar archivos en formato Word"
            )

        return value
    
    def save(self):
        archivo: InMemoryUploadedFile = self.validated_data.get("archivo")

        fs = FileSystemStorage(self.validated_data.get("location"))
        file = fs.save(self.validated_data.get("file_name"), archivo)
        fileurl = fs.generate_filename(file)
        return fileurl