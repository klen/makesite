import operator

from django.db.models import signals
from django.db.models.expressions import F, ExpressionNode


EXPRESSION_NODE_CALLBACKS = {
    ExpressionNode.ADD: operator.add,
    ExpressionNode.SUB: operator.sub,
    ExpressionNode.MUL: operator.mul,
    ExpressionNode.DIV: operator.div,
    ExpressionNode.MOD: operator.mod,
    ExpressionNode.AND: operator.and_,
    ExpressionNode.OR: operator.or_,
}


class CannotResolve(Exception):
    pass


def _resolve(instance, node):
    if isinstance(node, F):
        return getattr(instance, node.name)
    elif isinstance(node, ExpressionNode):
        return _resolve(instance, node)
    return node


def resolve_expression_node(instance, node):
    op = EXPRESSION_NODE_CALLBACKS.get(node.connector, None)
    if not op:
        raise CannotResolve
    runner = _resolve(instance, node.children[0])
    for n in node.children[1:]:
        runner = op(runner, _resolve(instance, n))
    return runner


def update(instance, full_clean=True, post_save=False, **kwargs):
    "Atomically update instance, setting field/value pairs from kwargs"

    # apply the updated args to the instance to mimic the change
    # note that these might slightly differ from the true database values
    # as the DB could have been updated by another thread. callers should
    # retrieve a new copy of the object if up-to-date values are required
    for k, v in kwargs.iteritems():
        if isinstance(v, ExpressionNode):
            v = resolve_expression_node(instance, v)
        setattr(instance, k, v)

    # clean instance before update
    if full_clean:
        instance.full_clean()

    # fields that use auto_now=True should be updated corrected, too!
    for field in instance._meta.fields:
        if hasattr(field, 'auto_now') and field.auto_now and field.name not in kwargs:
            kwargs[field.name] = field.pre_save(instance, False)

    rows_affected = instance.__class__._default_manager.filter(
        pk=instance.pk).update(**kwargs)

    if post_save:
        signals.post_save.send(sender=instance.__class__, instance=instance)

    return rows_affected


class Choices(object):

    def __init__(self, *choices):
        self._choices = []
        self._choice_dict = {}
        self._labels = {}

        for choice in choices:
            if isinstance(choice, (list, tuple)):
                if len(choice) == 2:
                    choice = (choice[0], choice[0], choice[1])

                elif len(choice) != 3:
                    raise ValueError("Choices can't handle a list/tuple of length %s, only 2 or 3" % len(choice))
            else:
                choice = (choice, choice, choice)

            self._choices.append((choice[0], choice[2]))
            self._choice_dict[choice[1]] = choice[0]

    def __getattr__(self, attname):
        try:
            return self._choice_dict[attname]
        except KeyError:
            raise AttributeError(attname)

    def __iter__(self):
        return iter(self._choices)

    def __getitem__(self, index):
        return self._choices[index]

    def __repr__(self):
        values, names = zip(*self._choices)
        labels = self._labels.itervalues()
        return '%s(%s)' % (self.__class__.__name__,
                           repr(zip(values, labels, names)))
