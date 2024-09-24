from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegistarionSerializer(serializers.ModelSerializer):
    class Meta:
     model=User
     fields = ['username', 'password']
     
    

    def validate(self, data):
       username=data['username']
       if User.objects.filter(username=username).exists():
          raise serializers.ValidationError("User already exits......")
       return data
    


    def create(self, validated_data):
        user=User(
            username=validated_data['username'],
            
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

        


class Loginserializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        try:
            user = User.objects.get(username=username)
            
            
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username..")

        # Check the provided password
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid  password.")
        # create the token
        refresh = RefreshToken.for_user(user)
        return {
           "refresh": str(refresh),
            "access": str(refresh.access_token),
            
        }
        

     