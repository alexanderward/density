from collections import namedtuple

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class NoSQLCreateMixin(object):
    def create(self, request, *args, **kwargs):
        # instance = self.serializer().create(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NoSQLListMixin(object):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(*args, **kwargs)
        if not queryset:
            return Response([])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FakeQueryset(object):
    # This fakes DRF to allow NoSQL Models for their routers
    class Model:
        class Meta:
            import uuid
            object_name = uuid.uuid4().hex

        _meta = Meta()

    model = Model()


class BaseNoSQL(GenericViewSet):
    queryset = FakeQueryset
    # This tells DRF routers to capture ALL on path detailed objects
    lookup_value_regex = '[^/]+'

    def __init__(self, **kwargs):
        self.queryset = namedtuple('queryset', ['model'])(self.serializer_class.Meta.model)
        super().__init__(**kwargs)

    def perform_create(self, serializer):
        serializer.save()

    def filter_results(self, model):
        raise NotImplementedError()

    def get_queryset(self, *args, **kwargs):
        model = self.serializer_class.Meta.model
        hash_key = self.request.query_params.get(model._hash_keyname)
        range_key = self.request.query_params.get(model._range_keyname)
        if not hash_key:
            data = model.scan()  # Not recommended....costs a lot of money with big datasets
        else:
            try:
                data = model.query(hash_key, self.filter_results(model))
            except NotImplementedError:
                data = model.query(hash_key)
        return data
