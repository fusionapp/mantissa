
"""
An interactive demonstration of L{xmantissa.liveform.LiveForm} and
L{xmantissa.liveform.ListChangeParameter}.

Run this test like this::
    $ twistd -n athena-widget --element=xmantissa.test.acceptance.liveform.testname
    $ firefox http://localhost:8080/
    (where testname is one of "coerce", "inputerrors",
     "listChangeParameter", "listChangeParameterCompact",
     "listChangeParameterNoDefaults")

This will display a form which rejects most inputs.
"""

from xmantissa.liveform import (TEXT_INPUT, InputError, Parameter, LiveForm,
    ListChangeParameter)


def coerce(theText):
    """
    Reject all values of C{theText} except C{'hello, world'}.
    """
    if theText != u'hello, world':
        raise InputError(u"Try entering 'hello, world'")


def inputerrors():
    """
    Create a L{LiveForm} which rejects most inputs in order to demonstrate how
    L{InputError} is handled in the browser.
    """
    form = LiveForm(
        lambda theText: None,
        [Parameter(u'theText', TEXT_INPUT, coerce, 'Some Text')],
        u'LiveForm input errors acceptance test',
        )
    return form


_parameterDefaults = [{u'foo': 1,  u'bar': 2},
                      {u'foo': 10, u'bar': 20}]


def _listChangeParameter(**parameterKwargs):
    counter = [0]
    def theCallable(repeatableFoo):
        for create in repeatableFoo.create:
            create.setter(u'other thing %d' % (counter[0],))
            counter[0] += 1
        return u'Created %s, edited %s, deleted %s' % (repeatableFoo.create,
                                                       repeatableFoo.edit,
                                                       repeatableFoo.delete)
    form = LiveForm(
        theCallable,
        [ListChangeParameter(
            u'repeatableFoo',
            [Parameter('foo', TEXT_INPUT, int, 'Enter a number'),
             Parameter('bar', TEXT_INPUT, int, 'And another')],
            **parameterKwargs)])
    form.jsClass = u'Mantissa.Test.EchoingFormWidget'
    return form



def listChangeParameter():
    """
    Create a L{LiveForm} with a L{ListChangeParameter}.
    """
    return _listChangeParameter(
        defaults=_parameterDefaults,
        modelObjects=(u'the first thing', u'the second thing'))



def listChangeParameterCompact():
    """
    Create a compact L{LiveForm} with a L{ListChangeParameter}.
    """
    liveForm = listChangeParameter()
    liveForm.compact()
    return liveForm



def listChangeParameterNoDefaults():
    """
    Create a L{LiveForm} with a L{ListChangeParameter} and no defaults.
    """
    return _listChangeParameter(defaults=[], modelObjects=[])
