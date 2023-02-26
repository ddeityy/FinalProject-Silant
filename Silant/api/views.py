from rest_framework import viewsets, permissions
from .serializers import *
from app.models import *
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponseForbidden
from django.http import Http404


# client 7
# c_prhht4azvymvcwe

# all methods
class CarViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    ordering = ["-shipment_date"]

    def retrieve(self, request, pk=None):
        try:
            q = Car.objects.get(serial_number=pk)
            s = None
            if (
                self.request.user.id == (q.buyer.id or q.service_company.id)
            ) or self.request.user.groups.filter(name="manager").exists():
                s = CarSerializer(q)
            else:
                s = LimitedCarSerializer(q)
        except Car.DoesNotExist:
            raise Http404
        return Response(s.data)

    def list(self, request, *args, **kwargs):
        try:
            print(Car.objects.all())
            print(self.request.user.groups.all())
            q = None
            if self.request.user.groups.filter(name="manager").exists():
                q = Car.objects.all().order_by("-shipment_date")
            elif self.request.user.groups.filter(name="client").exists():
                q = Car.objects.filter(buyer__user=request.user.id).order_by(
                    "-shipment_date"
                )
            elif self.request.user.groups.filter(name="service company").exists():
                q = Car.objects.filter(service_company__user=request.user.id).order_by(
                    "-shipment_date"
                )
            else:
                s = LimitedCarSerializer(q, many=True)
            s = CarSerializer(q, many=True)
        except Car.DoesNotExist:
            raise Http404
        return Response(s.data)


class MaitenanceViewSet(viewsets.ModelViewSet):
    queryset = Maitenance.objects.all()
    permission_classes = [permissions.DjangoModelPermissions]
    serializer_class = MaitenanceSerializer
    ordering = ["-date"]

    def retrieve(self, request, pk=None):
        try:
            q = Maitenance.objects.get(id=pk)
            s = None
            if (
                self.request.user.id == (q.car.buyer.id or q.service_company.id)
            ) or self.request.user.groups.filter(name="manager").exists():
                s = CarSerializer(q)
            else:
                Response(status=HttpResponseForbidden)
        except Maitenance.DoesNotExist:
            raise Http404
        return Response(s.data)

    def list(self, request, *args, **kwargs):
        try:
            q = None
            if self.request.user.groups.filter(name="client").exists():
                q = Maitenance.objects.filter(
                    car__buyer__user=request.user.id
                ).order_by("-date")
            elif self.request.user.groups.filter(name="service company").exists():
                q = Maitenance.objects.filter(
                    service_company__user=request.user.id
                ).order_by("-date")
            elif self.request.user.groups.filter(name="manager").exists():
                q = Maitenance.objects.all().order_by("-date")
            else:
                return Response(status=HttpResponseForbidden)
            s = MaitenanceSerializer(q, many=True)
        except Maitenance.DoesNotExist:
            raise Http404
        return Response(s.data)


class RepairViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    ordering = ["-issue_date"]

    def retrieve(self, request, pk=None):
        try:
            q = Repair.objects.get(id=pk)
            s = None
            if (
                self.request.user.id == (q.car.buyer.id or q.service_company.id)
            ) or self.request.user.groups.filter(name="manager").exists():
                s = CarSerializer(q)
            else:
                Response(status=HttpResponseForbidden)
        except Repair.DoesNotExist:
            raise Http404
        return Response(s.data)

    def list(self, request, *args, **kwargs):
        try:
            q = None
            if self.request.user.groups.filter(name="client").exists():
                q = Repair.objects.filter(car__buyer__user=request.user.id).order_by(
                    "-issue_date"
                )
            elif self.request.user.groups.filter(name="service company").exists():
                q = Repair.objects.filter(
                    service_company__user=request.user.id
                ).order_by("-issue_date")
            elif self.request.user.groups.filter(name="manager").exists():
                q = Repair.objects.all().order_by("-issue_date")
            s = RepairSerializer(q, many=True)
        except Repair.DoesNotExist:
            raise Http404
        return Response(s.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    @action(detail=False, methods=["get"])
    def current(self, request):
        try:
            q = None
            s = None
            if self.request.user.groups.filter(name="client").exists():
                q = Client.objects.get(user__id=request.user.id)
                s = ClientSerializer(q, many=False)
            elif self.request.user.groups.filter(name="service company").exists():
                q = ServiceCompany.objects.get(user__id=request.user.id)
                s = ServiceSerializer(q, many=False)
            else:
                q = User.objects.get(id=request.user.id)
                s = UserSerializer(q, many=False)
        except User.DoesNotExist:
            raise Http404
        return Response(s.data)


class ManualViewSet(viewsets.ModelViewSet):
    queryset = Manual.objects.all()
    serializer_class = ManualSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = ServiceCompany.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
