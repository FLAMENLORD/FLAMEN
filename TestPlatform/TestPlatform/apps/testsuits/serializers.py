from rest_framework import serializers
import re

from utils import common
from .models import Testsuits
from projects.models import Projects
from interfaces.models import Interfaces
from utils import validates


def validate_include(value):
    obj = re.match(r'^\[\d+(,\s\d+)*\]$', value)
    if obj is None:
        raise serializers.ValidationError('参数格式有误')
    else:
        res = obj.group()
        try:
            data = eval(res)
        except:
            raise serializers.ValidationError('参数格式有误')

        for item in data:
            if not Interfaces.objects.filter(id=item).exists():
                raise serializers.ValidationError(f'接口ID【{item}】不存在')


class TestsuitsModelSerializer(serializers.ModelSerializer):
	project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
	project_id = serializers.PrimaryKeyRelatedField(label='所属项目ID', help_text='所属项目ID', queryset=Projects.objects.all(), write_only=True)

	class Meta:
		model = Testsuits
		fields = ('id', 'name', 'project', 'project_id', 'include', 'create_time', 'update_time')

		extra_kwargs = {
			'create_time': {
				'read_only': True,
				'format': common.datetime_fmt()
			},
			'update_time': {
				'read_only': True,
				'format': common.datetime_fmt()
			},
			'include': {
				# 'write_only': True,
				'validators': [validate_include]
			}
		}

	def create(self, validated_data):
		if 'project_id' in validated_data:
			project = validated_data.pop('project_id')
			validated_data['project'] = project
			return super().create(validated_data)

	def update(self, instance, validated_data):
		if 'project_id' in validated_data:
			project = validated_data.pop('project_id')
			validated_data['project'] = project
			return super().update(instance, validated_data)


class TestsuitsRunModelSerializer(serializers.ModelSerializer):
	env_id = serializers.IntegerField(label='环境变量ID', help_text='环境变量ID', write_only=True, validators=[validates.is_existed_env_id])

	class Meta:
		model = Testsuits
		fields = ('id', 'env_id')
