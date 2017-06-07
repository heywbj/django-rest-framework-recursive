from django.db import models
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField


class LinkSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    next = RecursiveField(allow_null=True)


class NodeSerializer(serializers.Serializer):
    name = serializers.CharField()
    children = serializers.ListField(child=RecursiveField())


class ManyNullSerializer(serializers.Serializer):
    name = serializers.CharField()
    children = RecursiveField(required=False, allow_null=True, many=True)


class PingSerializer(serializers.Serializer):
    ping_id = serializers.IntegerField()
    pong = RecursiveField('PongSerializer', required=False)


class PongSerializer(serializers.Serializer):
    pong_id = serializers.IntegerField()
    ping = PingSerializer()


class SillySerializer(serializers.Serializer):
    name = RecursiveField(
        'rest_framework.fields.CharField', max_length=5)
    blankable = RecursiveField(
        'rest_framework.fields.CharField', allow_blank=True)
    nullable = RecursiveField(
        'rest_framework.fields.CharField', allow_null=True)
    links = RecursiveField('LinkSerializer')
    self = RecursiveField(required=False)


class RecursiveModel(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True)


class RecursiveModelSerializer(serializers.ModelSerializer):
    parent = RecursiveField(allow_null=True)

    class Meta:
        model = RecursiveModel
        fields = ('name', 'parent')


class TestRecursiveField:
    @staticmethod
    def serialize(serializer_class, value):
        serializer = serializer_class(value)

        assert serializer.data == value, \
            'serialized data does not match input'

    @staticmethod
    def deserialize(serializer_class, data):
        serializer = serializer_class(data=data)

        assert serializer.is_valid(), \
            'cannot validate on deserialization: %s' % dict(serializer.errors)
        assert serializer.validated_data == data, \
            'deserialized data does not match input'

    def test_link_serializer(self):
        value = {
            'name': 'first',
            'next': {
                'name': 'second',
                'next': {
                    'name': 'third',
                    'next': None,
                }
            }
        }

        self.serialize(LinkSerializer, value)
        self.deserialize(LinkSerializer, value)

    def test_node_serializer(self):
        value = {
            'name': 'root',
            'children': [{
                'name': 'first child',
                'children': [],
            }, {
                'name': 'second child',
                'children': [],
            }]
        }

        self.serialize(NodeSerializer, value)
        self.deserialize(NodeSerializer, value)

    def test_many_null_serializer(self):
        """Test that allow_null is propagated when many=True"""

        # Children is omitted from the root node
        value = {
            'name': 'root'
        }

        self.serialize(ManyNullSerializer, value)
        self.deserialize(ManyNullSerializer, value)

        # Children is omitted from the child nodes
        value2 = {
            'name': 'root',
            'children':[
                {'name': 'child1'},
                {'name': 'child2'},
            ]
        }

        self.serialize(ManyNullSerializer, value2)
        self.deserialize(ManyNullSerializer, value2)

    def test_ping_pong(self):
        pong = {
            'pong_id': 4,
            'ping': {
                'ping_id': 3,
                'pong': {
                    'pong_id': 2,
                    'ping': {
                        'ping_id': 1,
                    },
                },
            },
        }
        self.serialize(PongSerializer, pong)
        self.deserialize(PongSerializer, pong)

    def test_validation(self):
        value = {
            'name': 'good',
            'blankable': '',
            'nullable': None,
            'links': {
                'name': 'something',
                'next': {
                    'name': 'inner something',
                    'next': None,
                }
            }
        }
        self.serialize(SillySerializer, value)
        self.deserialize(SillySerializer, value)

        max_length = {
            'name': 'too long',
            'blankable': 'not blank',
            'nullable': 'not null',
            'links': {
                'name': 'something',
                'next': None,
            }
        }
        serializer = SillySerializer(data=max_length)
        assert not serializer.is_valid(), \
            'validation should fail due to name too long'

        nulled_out = {
            'name': 'good',
            'blankable': None,
            'nullable': 'not null',
            'links': {
                'name': 'something',
                'next': None,
            }
        }
        serializer = SillySerializer(data=nulled_out)
        assert not serializer.is_valid(), \
            'validation should fail due to null field'

        way_too_long = {
            'name': 'good',
            'blankable': '',
            'nullable': None,
            'links': {
                'name': 'something',
                'next': {
                    'name': 'inner something that is much too long',
                    'next': None,
                }
            }
        }
        serializer = SillySerializer(data=way_too_long)
        assert not serializer.is_valid(), \
            'validation should fail on inner link validation'

    def test_model_serializer(self):
        one = RecursiveModel(name='one')
        two = RecursiveModel(name='two', parent=one)

        # serialization
        representation = {
            'name': 'two',
            'parent': {
                'name': 'one',
                'parent': None,
            }
        }

        s = RecursiveModelSerializer(two)
        assert s.data == representation

        # deserialization
        self.deserialize(RecursiveModelSerializer, representation)

    def test_super_kwargs(self):
        """RecursiveField.__init__ introspect the parent constructor to pass
        kwargs properly. read_only is used used here to verify that the
        argument is properly passed to the super Field."""
        field = RecursiveField(default='a default value')
        assert field.default == 'a default value'
