from rest_marshmallow import  Schema, fields
from marshmallow import validate
from .models import items

class itemsserializer(Schema):
    item = fields.String(validate=validate.OneOf(["book", "pen", "folder","bag"]))
    class Meta:
        model=items
        fields=['id','item','status']
    
    def create(self,validated_data):
        return items.objects.create(**validated_data)
   