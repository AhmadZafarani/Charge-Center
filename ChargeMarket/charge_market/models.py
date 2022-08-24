from abc import abstractmethod

from django.core.validators import RegexValidator
from django.db import IntegrityError, models
from django.http import HttpResponseBadRequest


class Vendor(models.Model):
    identifier = models.AutoField(primary_key=True)
    _credit = models.PositiveIntegerField(null=False, default=0)

    def set_credit(self, credit: int):
        self._credit = credit

    def get_credit(self) -> int:
        return self._credit

    def __str__(self):
        return f"vendor with id: {self.identifier} and credit: {self._credit}"


class PhoneNumber(models.Model):
    _phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message="Phone number must be entered in the format: '09123456789'.")
    phone_number = models.CharField(
        validators=[_phone_regex], max_length=11, primary_key=True)
    charge = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"phone number with number: {self.phone_number} and charge: {self.charge}"


class Transaction(models.Model):
    identifier = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(
        to=Vendor, on_delete=models.DO_NOTHING, blank=False, null=False)
    amount = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        abstract = True

    @abstractmethod
    def charge(self, amount: int):
        pass


class ChargeTransaction(Transaction):
    def charge(self, amount: int):
        assert isinstance(amount, int)
        assert amount > 0

        new_amount = self.vendor.get_credit() + amount
        Vendor.objects.filter(identifier=self.vendor.identifier).update(
            _credit=new_amount)

    @staticmethod
    def save_model(vendor: Vendor, charge: str):
        transaction = ChargeTransaction()
        transaction.vendor = vendor
        try:
            charge = int(charge)
            assert charge >= 0
        except (ValueError, AssertionError):
            return HttpResponseBadRequest("charge must be a Positive Integer!")
        transaction.amount = charge

        return transaction.save()

    def save(self, *args, **kwargs):
        if not ChargeTransaction.objects.filter(identifier=self.identifier).exists():
            self.charge(self.amount)
        return super().save(*args, **kwargs)


class SellTransaction(Transaction):
    phone_number = models.ForeignKey(
        to=PhoneNumber, on_delete=models.DO_NOTHING, blank=False, null=False)

    def charge(self, amount: int):
        assert isinstance(amount, int)
        assert amount > 0

        new_amount = self.vendor.get_credit() - amount
        if new_amount < 0:
            raise IntegrityError("not enough credit to sell this charge")
        Vendor.objects.filter(identifier=self.vendor.identifier).update(
            _credit=new_amount)

        new_charge = self.phone_number.charge + amount
        PhoneNumber.objects.filter(phone_number=self.phone_number.phone_number).update(
            charge=new_charge)

    @staticmethod
    def save_model(vendor: Vendor, phone_number: PhoneNumber, charge: str):
        transaction = SellTransaction()
        transaction.vendor = vendor
        transaction.phone_number = phone_number
        try:
            charge = int(charge)
            assert charge >= 0
        except (ValueError, AssertionError):
            return HttpResponseBadRequest("charge must be a Positive Integer!")
        transaction.amount = charge

        return transaction.save()

    def save(self, *args, **kwargs):
        if not SellTransaction.objects.filter(identifier=self.identifier).exists():
            try:
                self.charge(self.amount)
            except IntegrityError as e:
                return HttpResponseBadRequest(e.with_traceback(None))
        return super().save(*args, **kwargs)
