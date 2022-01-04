from threading import Thread, Lock
from django.db import models

lock = Lock()


class ThreadWithReturnValue(Thread):
    def __init__(
        self,
        group=None,
        target=None,
        name=None,
        args=(),
        kwargs={},
        Verbose=None
    ):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        self.exc = None

    def run(self):
        lock.acquire()
        print('running')
        if self._target is not None:
            try:
                self._return = self._target(
                    *self._args,
                    **self._kwargs
                )
            except Exception as e:
                self.exc = e

    def join(self, *args):
        print('joining')
        Thread.join(self, *args)
        print('joined')
        lock.release()
        if self.exc:
            raise self.exc
        return self._return


class BaseQuerySet(models.query.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Iterate in a thread-safe manner
    def __iter__(self):
        thread = ThreadWithReturnValue(target=super().__iter__)
        thread.start()
        return thread.join()


class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(model=self.model)

    # Get in a thread-safe manner
    def get(self, *args, **kwargs):
        thread = ThreadWithReturnValue(target=super().get,
                                       args=args, kwargs=kwargs)
        thread.start()
        return thread.join()


class BaseModel(models.Model):
    objects = BaseManager()

    # Save in a thread-safe manner
    def save(self, *args, **kwargs):
        thread = ThreadWithReturnValue(
            target=super().save,
            args=args,
            kwargs=kwargs
        )
        thread.start()
        return thread.join()

    # Delete in a thread-safe manner
    def delete(self, *args, **kwargs):
        thread = ThreadWithReturnValue(
            target=super().delete,
            args=args,
            kwargs=kwargs
        )
        thread.start()
        return thread.join()

    class Meta:
        abstract = True


class Example(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
