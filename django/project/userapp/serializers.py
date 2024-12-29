from rest_framework import serializers
from .models import CustomUser
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from userapp.utils import Util

class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username','email', 'password', 'password2']
        # fields = '__all__'
        extra_kwargs ={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password doesnot match.')
        return attrs
    def create(self, validated_data):
        validated_data.pop('password2') # no column for password2 in custom user table
        return CustomUser.objects.create_user(**validated_data)
                

class LoginUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

#     def create(self, validated_data):
#         return validated_data
# class LoginUserSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(
#         style={'input_type': 'password'},
#         # trim_whitespace=False
#     )

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username']

class ChangeUserPasswordSerializer(serializers.Serializer):
    password0 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    # class Meta:
    #     fields = ['password', 'password2']
    
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if not user.check_password(attrs.get('password0')):
            raise serializers.ValidationError({'msg':'Enter your old password correctly'})
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password doesnot match.')
        
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(smart_bytes(user.id))
            # print('//Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            # print('//Password Reset Token', token)
            link = 'http://localhost:8000/user/reset-password/'+uid+'/'+token+'/'
            # print('//Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password with in 15 minutes.'+link
            
            # With Util
            email_data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(email_data)

            # Without Util
            # from django.core.mail import EmailMessage

            # email_data = EmailMessage(
            #     subject='Reset Your Password',
            #     body=body,
            #     from_email=None,
            #     to=[user.email]
            # )
            # email_data.send()
            # print('****')
            # print(email_data)
            # print(f"\nEmail Details: To={email_data.to}, From={email_data.from_email}, Subject='{email_data.subject}', Body='{email_data.body}'")
            return attrs
        else:
            raise serializers.ValidationError('Provided Email doesnot exist')

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')